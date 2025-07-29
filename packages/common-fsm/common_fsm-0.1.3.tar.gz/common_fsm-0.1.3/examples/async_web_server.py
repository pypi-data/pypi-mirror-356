import asyncio
import logging
from enum import Enum
from common_fsm import AsyncFSM, AsyncState, Event, Transition
import aiohttp
from aiohttp import web
import json

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# States for a simple order processing system
class OrderStates(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    ERROR = "error"

# Events for order processing
class OrderEvents(Enum):
    PROCESS = "process"
    SHIP = "ship"
    DELIVER = "deliver"
    CANCEL = "cancel"
    TIMEOUT = "timeout"

class OrderManager:
    def __init__(self):
        self.orders = {}  # order_id -> FSM
    
    async def create_order(self, order_id, items):
        """Create a new order with the given ID and items"""
        # Create states
        pending_state = AsyncState(timeout=5.0, verbose=True)  # 5 sekunder istället för 60
        pending_state.add_handler(
            OrderEvents.PROCESS,
            lambda e: None if e.kwargs and e.kwargs.get("dummy") else Transition(OrderStates.PROCESSING)
        )
        pending_state.add_handler(
            OrderEvents.CANCEL,
            lambda e: Transition(OrderStates.CANCELLED)
        )
        pending_state.add_handler(
            OrderEvents.TIMEOUT,
            lambda e: Transition(OrderStates.PROCESSING)
        )
        
        processing_state = AsyncState(timeout=10.0, verbose=True)  # 10 sekunder istället för 120
        processing_state.add_handler(
            OrderEvents.SHIP,
            lambda e: Transition(OrderStates.SHIPPED)
        )
        processing_state.add_handler(
            OrderEvents.CANCEL,
            lambda e: Transition(OrderStates.CANCELLED)
        )
        processing_state.add_handler(
            OrderEvents.TIMEOUT,
            lambda e: Transition(OrderStates.SHIPPED)
        )
        
        shipped_state = AsyncState(timeout=15.0, verbose=True)  # 15 sekunder istället för 300
        shipped_state.add_handler(
            OrderEvents.DELIVER,
            lambda e: Transition(OrderStates.DELIVERED)
        )
        shipped_state.add_handler(
            OrderEvents.TIMEOUT,
            lambda e: Transition(OrderStates.DELIVERED)
        )
        
        delivered_state = AsyncState(verbose=True)
        cancelled_state = AsyncState(verbose=True)
        error_state = AsyncState(verbose=True)
        
        # Add async hooks for database updates
        pending_state.add_enter_hook(
            lambda s: self.log_state_change(order_id, s)
        )
        processing_state.add_enter_hook(
            lambda s: self.log_state_change(order_id, s)
        )
        shipped_state.add_enter_hook(
            lambda s: self.log_state_change(order_id, s)
        )
        delivered_state.add_enter_hook(
            lambda s: self.log_state_change(order_id, s)
        )
        cancelled_state.add_enter_hook(
            lambda s: self.log_state_change(order_id, s)
        )
        
        # Create FSM
        fsm = AsyncFSM(
            OrderStates.PENDING,
            {
                OrderStates.PENDING: pending_state,
                OrderStates.PROCESSING: processing_state,
                OrderStates.SHIPPED: shipped_state,
                OrderStates.DELIVERED: delivered_state,
                OrderStates.CANCELLED: cancelled_state,
                OrderStates.ERROR: error_state
            },
            timeout_event=OrderEvents.TIMEOUT,
            error_state=OrderStates.ERROR,
            verbose=True
        )
        
        # Store the FSM
        self.orders[order_id] = {
            "fsm": fsm,
            "items": items,
            "history": []
        }
        
        # Reset state to PENDING (since the PROCESS event would have changed it)
        fsm.current_state = OrderStates.PENDING
        
        # Add initial state to history
        await self.log_state_change(order_id, OrderStates.PENDING)
        
        return {"order_id": order_id, "status": OrderStates.PENDING.value}
    
    async def log_state_change(self, order_id, state):
        """Log a state change to the order history"""
        if order_id in self.orders:
            self.orders[order_id]["history"].append({
                "state": state.value,
                "timestamp": asyncio.get_event_loop().time()
            })
            logging.info(f"Order {order_id} changed to state {state.name}")
            print(f"Order {order_id} changed to state {state.name}")
    
    async def get_order(self, order_id):
        """Get the current state of an order"""
        if order_id not in self.orders:
            return None
        
        order = self.orders[order_id]
        return {
            "order_id": order_id,
            "status": order["fsm"].current_state.value,
            "items": order["items"],
            "history": order["history"]
        }
    
    async def update_order(self, order_id, event_name):
        """Update an order by triggering an event"""
        if order_id not in self.orders:
            return None
        
        try:
            event = OrderEvents[event_name.upper()]
        except KeyError:
            return {"error": f"Invalid event: {event_name}"}
        
        order = self.orders[order_id]
        await order["fsm"].handle_event(Event(event))
        
        return {
            "order_id": order_id,
            "status": order["fsm"].current_state.value
        }
    
    async def shutdown(self):
        """Shutdown all FSMs"""
        for order_id, order in self.orders.items():
            await order["fsm"].shutdown()

# Create a web application
async def create_app():
    app = web.Application()
    order_manager = OrderManager()
    
    # Store the order manager in the app
    app["order_manager"] = order_manager
    
    # Define routes
    app.router.add_post('/orders', create_order_handler)
    app.router.add_get('/orders/{order_id}', get_order_handler)
    app.router.add_post('/orders/{order_id}/events', update_order_handler)
    
    # Add cleanup
    app.on_cleanup.append(cleanup_handler)
    
    return app

async def create_order_handler(request):
    """Handle POST /orders"""
    order_manager = request.app["order_manager"]
    
    try:
        data = await request.json()
        order_id = data.get("order_id", f"order-{len(order_manager.orders) + 1}")
        items = data.get("items", [])
        
        result = await order_manager.create_order(order_id, items)
        return web.json_response(result)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

async def get_order_handler(request):
    """Handle GET /orders/{order_id}"""
    order_manager = request.app["order_manager"]
    order_id = request.match_info["order_id"]
    
    result = await order_manager.get_order(order_id)
    if result is None:
        return web.json_response({"error": "Order not found"}, status=404)
    
    return web.json_response(result)

async def update_order_handler(request):
    """Handle POST /orders/{order_id}/events"""
    order_manager = request.app["order_manager"]
    order_id = request.match_info["order_id"]
    
    try:
        data = await request.json()
        event_name = data.get("event")
        
        if not event_name:
            return web.json_response({"error": "Event name is required"}, status=400)
        
        result = await order_manager.update_order(order_id, event_name)
        if result is None:
            return web.json_response({"error": "Order not found"}, status=404)
        
        return web.json_response(result)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=400)

async def cleanup_handler(app):
    """Clean up resources when the app is shutting down"""
    order_manager = app["order_manager"]
    await order_manager.shutdown()

if __name__ == "__main__":
    app = asyncio.run(create_app())
    web.run_app(app, port=8080) 