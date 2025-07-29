from enum import Enum
from common_fsm import FSM, State, Event, Transition

class States(Enum):
    NORMAL = "normal"
    ERROR = "error"

class Events(Enum):
    DO_SOMETHING = "do_something"
    RECOVER = "recover"
    
# Normal state with a handler that will throw an exception
normal_state = State()
normal_state.add_handler(
    Events.DO_SOMETHING,
    lambda e: 1/0  # This will raise a ZeroDivisionError
)

# Error state that can recover
error_state = State()
error_state.add_handler(
    Events.RECOVER,
    lambda e: Transition(States.NORMAL)
)
error_state.add_enter_hook(
    lambda s: print("Entered error state due to an exception")
)

# Create FSM with error state
fsm = FSM(
    initial_state=States.NORMAL,
    state_objects={
        States.NORMAL: normal_state,
        States.ERROR: error_state
    },
    error_state=States.ERROR,
    verbose=True
)


# This will cause an exception and transition to error state
fsm.handle_event(Event(Events.DO_SOMETHING))

# Now we're in error state
print(f"Current state: {fsm.current_state}")

# We can recover
fsm.handle_event(Event(Events.RECOVER))
print(f"Current state after recovery: {fsm.current_state}") 