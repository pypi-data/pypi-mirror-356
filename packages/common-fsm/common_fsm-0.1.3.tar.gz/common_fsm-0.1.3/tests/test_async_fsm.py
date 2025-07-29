import unittest
import asyncio
from enum import Enum
from common_fsm import AsyncFSM, AsyncState, Event, Transition

class TestAsyncFSM(unittest.TestCase):
    """Test the asynchronous FSM implementation"""
    
    def setUp(self):
        """Set up test states and FSM"""
        class States(Enum):
            OFF = "off"
            ON = "on"
            ERROR = "error"
        
        class Events(Enum):
            POWER_ON = "power_on"
            POWER_OFF = "power_off"
            TIMEOUT = "timeout"
            TRIGGER_ERROR = "trigger_error"
        
        self.States = States
        self.Events = Events
        
        # Track state transitions
        self.transitions = []
        
        # Create states
        self.off_state = AsyncState(verbose=True)
        self.off_state.add_handler(
            Events.POWER_ON,
            lambda e: Transition(States.ON)
        )
        self.off_state.add_exit_hook(
            lambda s: self.transitions.append(f"Exiting {s.name}")
        )
        
        self.on_state = AsyncState(timeout=0.1, verbose=True)
        self.on_state.add_handler(
            Events.POWER_OFF,
            lambda e: Transition(States.OFF)
        )
        self.on_state.add_handler(
            Events.TIMEOUT,
            lambda e: Transition(States.OFF)
        )
        self.on_state.add_enter_hook(
            lambda s: self.transitions.append(f"Entering {s.name}")
        )
        
        # Error state
        self.error_state = AsyncState()
        
        # Create FSM
        self.fsm = AsyncFSM(
            initial_state=States.OFF,
            state_objects={
                States.OFF: self.off_state,
                States.ON: self.on_state,
                States.ERROR: self.error_state
            },
            timeout_event=Events.TIMEOUT,
            error_state=States.ERROR,
            verbose=True
        )
        
        # Set testing mode for tests
        self.fsm._testing_mode = True
    
    def test_initial_state(self):
        """Test that the FSM starts in the initial state"""
        self.assertEqual(self.fsm.current_state, self.States.OFF)
    
    def run_async_test(self, coro):
        """Helper to run async tests"""
        return asyncio.run(coro)
    
    def test_sync_transition(self):
        """Test a synchronous transition"""
        async def test_coro():
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
            self.assertIn("Entering ON", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_async_handler(self):
        """Test an asynchronous handler"""
        async def async_handler(event):
            await asyncio.sleep(0.1)  # Simulate async work
            return Transition(self.States.ON)
        
        self.off_state.add_handler(self.Events.POWER_ON, async_handler)
        
        async def test_coro():
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
        
        self.run_async_test(test_coro())
    
    def test_async_hook(self):
        """Test an asynchronous hook"""
        async def async_hook(state):
            await asyncio.sleep(0.1)  # Simulate async work
            self.transitions.append(f"Async hook for {state.name}")
        
        self.on_state.add_enter_hook(async_hook)
        
        async def test_coro():
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
            self.assertIn("Async hook for ON", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_timeout(self):
        """Test that timeouts work correctly"""
        async def test_coro():
            # Trigger an event to transition to ON state
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
            
            # Wait for timeout
            await asyncio.sleep(0.2)
            
            # Should have transitioned back to OFF
            self.assertEqual(self.fsm.current_state, self.States.OFF)
        
        self.run_async_test(test_coro())
    
    def test_error_handling(self):
        """Test error handling with async handlers"""
        async def error_handler(event):
            raise ValueError("Test error")
        
        self.on_state.add_handler(self.Events.TRIGGER_ERROR, error_handler)
        
        async def test_coro():
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
            
            # Trigger error
            await self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            
            # Should transition to error state
            self.assertEqual(self.fsm.current_state, self.States.ERROR)
        
        self.run_async_test(test_coro())
    
    def test_debug_mode(self):
        """Test that debug mode disables timeouts"""
        # Create a new FSM with debug mode
        debug_fsm = AsyncFSM(
            initial_state=self.States.OFF,
            state_objects={
                self.States.OFF: self.off_state,
                self.States.ON: self.on_state
            },
            timeout_event=self.Events.TIMEOUT,
            verbose=True,
            debug_mode=True
        )
        
        async def test_coro():
            await debug_fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(debug_fsm.current_state, self.States.ON)
            
            # Wait for what would be a timeout
            await asyncio.sleep(0.2)
            
            # Should still be in ON state because debug mode disables timeouts
            self.assertEqual(debug_fsm.current_state, self.States.ON)
            
            # Clean up
            await debug_fsm.shutdown()
        
        self.run_async_test(test_coro())
    
    def test_shutdown(self):
        """Test that shutdown cancels all timers"""
        async def test_coro():
            await self.fsm.handle_event(Event(self.Events.POWER_ON))
            self.assertEqual(self.fsm.current_state, self.States.ON)
            
            # Shutdown
            await self.fsm.shutdown()
            
            # Wait for what would be a timeout
            await asyncio.sleep(0.2)
            
            # Should still be in ON state because shutdown cancelled the timer
            self.assertEqual(self.fsm.current_state, self.States.ON)
        
        self.run_async_test(test_coro())

if __name__ == '__main__':
    unittest.main() 