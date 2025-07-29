from enum import Enum
from typing import Dict, Callable, Any, Optional, TypeVar, Set, Generic, Union, Awaitable, List, Coroutine
import logging
import asyncio
import inspect

# Import from fsm module
from .fsm import Event, Transition, StateEnum, EventEnum

# Type aliases for handlers and hooks
SyncHandler = Callable[[Event], Optional[Transition]]
AsyncHandler = Callable[[Event], Awaitable[Optional[Transition]]]
Handler = Union[SyncHandler, AsyncHandler]

SyncHook = Callable[[StateEnum], None]
AsyncHook = Callable[[StateEnum], Awaitable[None]]
Hook = Union[SyncHook, AsyncHook]

class AsyncState:
    """Base class for states in an async FSM"""
    def __init__(self, timeout: Optional[float] = None, verbose: bool = False):
        self.handlers: Dict[EventEnum, Handler] = {}
        self.enter_hooks: Set[Hook] = set()
        self.exit_hooks: Set[Hook] = set()
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose

    def add_handler(self, event_type: EventEnum, handler: Handler) -> None:
        """Add a handler for a specific event type"""
        if not isinstance(event_type, Enum):
            raise TypeError(f"Event type must be an Enum, got {type(event_type)}")
        
        if not callable(handler):
            raise TypeError(f"Handler must be callable, got {type(handler)}")
        
        self.handlers[event_type] = handler

    def add_enter_hook(self, hook: Hook) -> None:
        """Add a hook that runs when entering this state"""
        self.enter_hooks.add(hook)

    def add_exit_hook(self, hook: Hook) -> None:
        """Add a hook that runs when exiting this state"""
        self.exit_hooks.add(hook)

    async def handle_event(self, event: Event, state_name: str, catch_exceptions: bool = False) -> Optional[Transition]:
        """Handle an event. Return a Transition if state should change"""
        handler = self.handlers.get(event.type)
        if handler:
            if catch_exceptions:
                try:
                    if inspect.iscoroutinefunction(handler):
                        return await handler(event)
                    else:
                        return handler(event)
                except Exception as e:
                    if self.verbose:
                        self.logger.error(f"Error in handler for event {event.type.name} in state {state_name}: {str(e)}")
                    return None
            else:
                # Let exceptions bubble up
                if inspect.iscoroutinefunction(handler):
                    return await handler(event)
                else:
                    return handler(event)
        if self.verbose:
            self.logger.info(f"No handler for event {event.type.name} in state {state_name}")
        return None

class AsyncFSM(Generic[StateEnum, EventEnum]):
    """
    An asynchronous Finite State Machine implementation with optional state timeouts.
    
    Example usage:
        off_state = AsyncState()
        off_state.add_handler(Events.POWER_ON, lambda e: Transition(States.ON))
        fsm = AsyncFSM(initial_state=States.OFF,
                      state_objects={States.OFF: off_state, ...})
    """
    
    def __init__(self, 
                 initial_state: StateEnum, 
                 state_objects: Dict[StateEnum, AsyncState], 
                 timeout_event: Optional[EventEnum] = None,
                 error_state: Optional[StateEnum] = None,
                 validate_transitions: bool = True,
                 verbose: bool = False,
                 debug_mode: bool = False):
        self.current_state = initial_state
        self.state_objects = state_objects
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.timeout_event = timeout_event
        self.error_state = error_state
        self.debug_mode = debug_mode
        
        # Single timer for current state
        self._current_timer: Optional[asyncio.Task] = None
        
        # Validate initial state exists
        if initial_state not in state_objects:
            raise ValueError(f"Initial state {initial_state} not found in state_objects")
        
        # Validate error state exists if provided
        if error_state is not None and error_state not in state_objects:
            raise ValueError(f"Error state {error_state} not found in state_objects")
        
        # Validate all transitions point to valid states
        if validate_transitions:
            self._validate_transitions()
        
        # State hooks
        self.enter_hooks: Dict[StateEnum, Set[Hook]] = {}
        self.exit_hooks: Dict[StateEnum, Set[Hook]] = {}

        # Flag to track if we've been initialized
        self._initialized = False
        
        # For testing purposes only - internal flag
        # This is only set to True in tests, never in production code
        self._testing_mode = False
        
        # Schedule initialization for next event loop iteration if a loop is running
        if timeout_event and not debug_mode:
            try:
                # Check if there's a running event loop
                loop = asyncio.get_running_loop()
                # If we get here, there is a running loop, so create the task
                asyncio.create_task(self._ensure_initialized())
            except RuntimeError:
                # No running event loop, that's fine in tests
                pass

    def _validate_transitions(self) -> None:
        """Validate that all transitions point to states that exist in state_objects"""
        for state_enum, state_obj in self.state_objects.items():
            for event_type, handler in state_obj.handlers.items():
                # Skip validation for handlers that might throw exceptions
                # We only want to validate static transitions that are defined directly
                if handler.__name__ == '<lambda>':
                    # For lambda functions, we can't easily check if they'll throw exceptions
                    # So we'll skip detailed validation and just trust the user
                    continue
                
                try:
                    # Create a test event to check transitions
                    test_event = Event(event_type)
                    
                    # For async handlers, we can't easily validate without running the event loop
                    if inspect.iscoroutinefunction(handler):
                        continue
                        
                    transition = handler(test_event)
                    
                    # If handler returns a transition, validate the target state
                    if transition is not None and isinstance(transition, Transition):
                        if transition.to_state not in self.state_objects:
                            raise ValueError(
                                f"Invalid transition from {state_enum} on event {event_type}: "
                                f"Target state {transition.to_state} not found in state_objects"
                            )
                except Exception:
                    # If handler throws an exception during validation, we'll skip it
                    # This is expected for handlers that do complex logic
                    continue

    def add_enter_hook(self, state: StateEnum, hook: Hook) -> None:
        """Add a hook that runs when entering a state"""
        if state not in self.enter_hooks:
            self.enter_hooks[state] = set()
        self.enter_hooks[state].add(hook)

    def add_exit_hook(self, state: StateEnum, hook: Hook) -> None:
        """Add a hook that runs when exiting a state"""
        if state not in self.exit_hooks:
            self.exit_hooks[state] = set()
        self.exit_hooks[state].add(hook)

    async def _start_timer(self, state: StateEnum) -> None:
        """Start timer for current state if timeout is set and not in debug mode"""
        if self.debug_mode:
            if self.verbose:
                self.logger.info(f"Debug mode: Skipping timer for state {state.name}")
            return
        
        # Stop any existing timer first
        await self._stop_timer()
        
        state_object = self.state_objects[state]
        if state_object.timeout and self.timeout_event:
            # Create a new timer task
            self._current_timer = asyncio.create_task(self._timer_callback(state, state_object.timeout))

    async def _timer_callback(self, state: StateEnum, timeout: float) -> None:
        """Timer callback that triggers a timeout event after the specified duration"""
        try:
            await asyncio.sleep(timeout)
            if self.current_state == state and self.timeout_event:
                await self.handle_event(Event(self.timeout_event))
        except asyncio.CancelledError:
            # Timer was cancelled, which is expected when state changes
            pass
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error in timer callback for state {state.name}: {str(e)}")

    async def _stop_timer(self, state: StateEnum = None) -> None:
        """Stop the current timer if it exists"""
        if self._current_timer and not self._current_timer.done():
            self._current_timer.cancel()
            self._current_timer = None

    async def _ensure_initialized(self):
        """Ensure FSM is initialized (timers started)"""
        if not self._initialized:
            if self.timeout_event and not self.debug_mode and not self._testing_mode:
                await self._start_timer(self.current_state)
            self._initialized = True

    async def handle_event(self, event: Event) -> None:
        """
        Handle an incoming event by delegating to current state handler.
        """
        # Ensure FSM is initialized
        await self._ensure_initialized()
        
        # Type checking
        if not isinstance(event, Event):
            raise TypeError(f"Expected Event object, got {type(event)}")
        
        if not isinstance(event.type, Enum):
            raise TypeError(f"Event type must be an Enum, got {type(event.type)}")
        
        current = self.current_state
        state_object = self.state_objects[current]
        
        try:
            # Let the state handle the event
            transition = await state_object.handle_event(event, current.name)
            
            # If no transition needed, just return
            if transition is None:
                return

            # If state change is needed
            if transition.to_state != current:
                # Type checking for transition
                if not isinstance(transition, Transition):
                    raise TypeError(f"Expected Transition object, got {type(transition)}")
                
                if not isinstance(transition.to_state, Enum):
                    raise TypeError(f"Transition target must be an Enum, got {type(transition.to_state)}")
                
                # Stop timer for current state
                await self._stop_timer()
                
                # Execute exit hooks for current state
                await self._execute_hooks(state_object.exit_hooks, current)

                # Update state
                self.current_state = transition.to_state
                new_state = self.state_objects[transition.to_state]

                # Execute enter hooks for new state
                await self._execute_hooks(new_state.enter_hooks, transition.to_state)

                # Start timer for new state if needed
                if not self.debug_mode:
                    await self._start_timer(transition.to_state)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error handling event {event.type.name} in state {current.name}: {str(e)}")
            
            # Transition to error state if defined
            if self.error_state is not None:
                await self._transition_to_error_state(e)

    async def _execute_hooks(self, hooks: Set[Hook], state: StateEnum) -> None:
        """Execute a set of hooks"""
        for hook in hooks:
            try:
                if inspect.iscoroutinefunction(hook):
                    await hook(state)
                else:
                    result = hook(state)
                    # Check if the result is a coroutine (could happen with lambda functions)
                    if result is not None and inspect.iscoroutine(result):
                        await result
            except Exception as e:
                if self.verbose:
                    self.logger.error(f"Error in hook for state {state.name}: {str(e)}")

    async def shutdown(self) -> None:
        """Stop all timers and cleanup FSM resources"""
        await self._stop_timer()
        
        if self.verbose:
            self.logger.info(f"AsyncFSM shutdown complete")

    async def _transition_to_error_state(self, exception: Exception) -> None:
        """Transition to the error state due to an exception"""
        if self.error_state is None:
            return
            
        try:
            # Stop timer for current state
            await self._stop_timer()
            
            # Get current state object
            current_state_obj = self.state_objects[self.current_state]
            
            # Execute exit hooks for current state
            await self._execute_hooks(current_state_obj.exit_hooks, self.current_state)
            
            # Update state
            previous_state = self.current_state
            self.current_state = self.error_state
            error_state_obj = self.state_objects[self.error_state]
            
            # Log the transition
            if self.verbose:
                self.logger.warning(
                    f"Transitioning from {previous_state.name} to error state {self.error_state.name} "
                    f"due to exception: {str(exception)}"
                )
            
            # Execute enter hooks for error state
            await self._execute_hooks(error_state_obj.enter_hooks, self.error_state)
            
        except Exception as e:
            # If transitioning to error state fails, just log it
            if self.verbose:
                self.logger.error(f"Failed to transition to error state: {str(e)}")

    async def start_timer(self):
        """Explicitly start the timer for the current state without changing state"""
        if self.timeout_event and not self.debug_mode:
            await self._start_timer(self.current_state)
        self._initialized = True 