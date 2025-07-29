from enum import Enum
from typing import Dict, Callable, Any, Optional, TypeVar, Set, Generic
from dataclasses import dataclass
import logging
import threading
import time

# Generic types for state and event enums
StateEnum = TypeVar('StateEnum', bound=Enum)
EventEnum = TypeVar('EventEnum', bound=Enum)

@dataclass
class Event:
    """Represents an event with optional arguments"""
    type: EventEnum
    args: tuple = ()
    kwargs: dict = None

    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}

@dataclass
class Transition:
    """Represents a state transition"""
    to_state: StateEnum

class State:
    """Base class for states"""
    def __init__(self, timeout: Optional[float] = None, verbose: bool = False):
        self.handlers: Dict[EventEnum, Callable[[Event], Optional[Transition]]] = {}
        self.enter_hooks: Set[Callable[[StateEnum], None]] = set()
        self.exit_hooks: Set[Callable[[StateEnum], None]] = set()
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)
        self.verbose = verbose

    def add_handler(self, event_type: EventEnum, 
                   handler: Callable[[Event], Optional[Transition]]) -> None:
        """Add a handler for a specific event type"""
        if not isinstance(event_type, Enum):
            raise TypeError(f"Event type must be an Enum, got {type(event_type)}")
        
        if not callable(handler):
            raise TypeError(f"Handler must be callable, got {type(handler)}")
        
        self.handlers[event_type] = handler

    def add_enter_hook(self, hook: Callable[[StateEnum], None]) -> None:
        """Add a hook that runs when entering this state"""
        self.enter_hooks.add(hook)

    def add_exit_hook(self, hook: Callable[[StateEnum], None]) -> None:
        """Add a hook that runs when exiting this state"""
        self.exit_hooks.add(hook)

    def handle_event(self, event: Event, state_name: str, catch_exceptions: bool = False) -> Optional[Transition]:
        """Handle an event. Return a Transition if state should change"""
        handler = self.handlers.get(event.type)
        if handler:
            if catch_exceptions:
                try:
                    return handler(event)
                except Exception as e:
                    if self.verbose:
                        self.logger.error(f"Error in handler for event {event.type.name} in state {state_name}: {str(e)}")
                    return None
            else:
                # Låt exceptions bubbla upp
                return handler(event)
        if self.verbose:
            self.logger.info(f"No handler for event {event.type.name} in state {state_name}")
        return None

class FSM(Generic[StateEnum, EventEnum]):
    """
    A generic Finite State Machine implementation with optional state timeouts.
    
    Example usage:
        off_state = State()
        off_state.add_handler(Events.POWER_ON, lambda e: Transition(States.ON))
        fsm = FSM(initial_state=States.OFF,
                 state_objects={States.OFF: off_state, ...})
    """
    
    def __init__(
        self,
        initial_state: StateEnum,
        state_objects: Dict[StateEnum, State],
        timeout_event: Optional[EventEnum] = None,
        error_state: Optional[StateEnum] = None,
        validate_transitions: bool = True,
        verbose: bool = False,
        debug_mode: bool = False
    ):
        # Validera att initial_state är av rätt typ
        if not isinstance(initial_state, Enum):
            raise TypeError(f"Initial state must be an Enum, got {type(initial_state)}")

        # Validera att alla states i state_objects är av rätt typ
        expected_type = type(initial_state)
        
        for state, state_obj in state_objects.items():
            if type(state) != expected_type:
                raise TypeError(f"All states must be of type {expected_type.__name__}, got {type(state).__name__}")

        # Validera error_state om det finns
        if error_state is not None and type(error_state) != expected_type:
            raise TypeError(f"Error state must be of type {expected_type.__name__}")

        self.current_state = initial_state
        self.state_objects = state_objects
        self.verbose = verbose
        self.logger = logging.getLogger(__name__)
        self.timeout_event = timeout_event
        self.error_state = error_state
        self.debug_mode = debug_mode
        
        # Single timer for current state
        self._current_timer: Optional[threading.Timer] = None
        
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
        self.enter_hooks: Dict[StateEnum, Set[Callable]] = {}
        self.exit_hooks: Dict[StateEnum, Set[Callable]] = {}

        # Start timer for initial state if needed (unless in debug mode)
        if timeout_event and not debug_mode:
            self._start_timer(initial_state)
    
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

    def add_enter_hook(self, state: StateEnum, hook: Callable[[StateEnum], None]) -> None:
        """Add a hook that runs when entering a state"""
        if state not in self.enter_hooks:
            self.enter_hooks[state] = set()
        self.enter_hooks[state].add(hook)

    def add_exit_hook(self, state: StateEnum, hook: Callable[[StateEnum], None]) -> None:
        """Add a hook that runs when exiting a state"""
        if state not in self.exit_hooks:
            self.exit_hooks[state] = set()
        self.exit_hooks[state].add(hook)

    def _start_timer(self, state: StateEnum) -> None:
        """Start timer for current state if timeout is set and not in debug mode"""
        if self.debug_mode:
            if self.verbose:
                self.logger.info(f"Debug mode: Skipping timer for state {state.name}")
            return
        
        # Stop any existing timer first
        self._stop_timer()
        
        state_object = self.state_objects[state]
        if state_object.timeout and self.timeout_event:
            self._current_timer = threading.Timer(
                state_object.timeout,
                lambda: self.handle_event(Event(self.timeout_event))
            )
            self._current_timer.start()

    def _stop_timer(self, state: StateEnum = None) -> None:
        """Stop the current timer if it exists"""
        if self._current_timer:
            self._current_timer.cancel()
            self._current_timer = None

    def handle_event(self, event: Event) -> None:
        """
        Handle an incoming event by delegating to current state handler.
        """
        # Type checking
        if not isinstance(event, Event):
            raise TypeError(f"Expected Event object, got {type(event)}")
        
        if not isinstance(event.type, Enum):
            raise TypeError(f"Event type must be an Enum, got {type(event.type)}")
        
        current = self.current_state
        state_object = self.state_objects[current]
        
        try:
            # Let the state handle the event
            transition = state_object.handle_event(event, current.name)
            
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
                self._stop_timer()
                
                # Execute exit hooks for current state
                self._execute_hooks(state_object.exit_hooks, current)

                # Update state
                self.current_state = transition.to_state
                new_state = self.state_objects[transition.to_state]

                # Execute enter hooks for new state
                self._execute_hooks(new_state.enter_hooks, transition.to_state)

                # Start timer for new state if needed
                if not self.debug_mode:
                    self._start_timer(transition.to_state)
        except Exception as e:
            if self.verbose:
                self.logger.error(f"Error handling event {event.type.name} in state {current.name}: {str(e)}")
            
            # Transition to error state if defined
            if self.error_state is not None:
                self._transition_to_error_state(e)

    def _execute_hooks(self, hooks: Set[Callable], state: StateEnum) -> None:
        """Execute hooks safely, catching and logging any exceptions"""
        for hook in hooks:
            try:
                hook(state)
            except Exception as e:
                if self.verbose:
                    self.logger.error(f"Error in hook for state {state.name}: {str(e)}")

    def shutdown(self) -> None:
        """Stop all timers and cleanup FSM resources"""
        self._stop_timer()
        if self.verbose:
            self.logger.info(f"FSM shutdown complete")

    def _transition_to_error_state(self, exception: Exception) -> None:
        """Transition to the error state due to an exception"""
        if self.error_state is None:
            return
            
        try:
            # Stop timer for current state
            self._stop_timer()
            
            # Get current state object
            current_state_obj = self.state_objects[self.current_state]
            
            # Execute exit hooks for current state
            self._execute_hooks(current_state_obj.exit_hooks, self.current_state)
            
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
            self._execute_hooks(error_state_obj.enter_hooks, self.error_state)
            
        except Exception as e:
            # If transitioning to error state fails, just log it
            if self.verbose:
                self.logger.error(f"Failed to transition to error state: {str(e)}")