import pytest
from enum import Enum
from src.common_fsm import FSM, State, Event, Transition

# Test enums
class States(Enum):
    STATE_A = "state_a"
    STATE_B = "state_b"

class Events(Enum):
    EVENT_1 = "event_1"
    EVENT_2 = "event_2"
    EVENT_WITH_DATA = "event_with_data"

# Test fixture for basic FSM setup
@pytest.fixture
def basic_fsm():
    # Create states
    state_a = State()
    state_b = State()
    
    # Add handlers
    state_a.add_handler(
        Events.EVENT_1,
        lambda e: Transition(States.STATE_B)
    )
    
    state_b.add_handler(
        Events.EVENT_2,
        lambda e: Transition(States.STATE_A)
    )

    # Create and return FSM
    return FSM(
        States.STATE_A,
        {
            States.STATE_A: state_a,
            States.STATE_B: state_b
        }
    )

def test_initial_state(basic_fsm):
    assert basic_fsm.current_state == States.STATE_A

def test_state_transition(basic_fsm):
    # Test transition from A to B
    basic_fsm.handle_event(Event(Events.EVENT_1))
    assert basic_fsm.current_state == States.STATE_B
    
    # Test transition back to A
    basic_fsm.handle_event(Event(Events.EVENT_2))
    assert basic_fsm.current_state == States.STATE_A

def test_unhandled_event(basic_fsm):
    # Event that isn't handled shouldn't change state
    initial_state = basic_fsm.current_state
    basic_fsm.handle_event(Event(Events.EVENT_WITH_DATA))
    assert basic_fsm.current_state == initial_state

def test_hooks():
    # Create states
    state_a = State()
    state_b = State()
    
    # Track hook calls
    enter_calls = []
    exit_calls = []
    
    # Add handlers and hooks
    state_a.add_handler(
        Events.EVENT_1,
        lambda e: Transition(States.STATE_B)
    )
    state_a.add_exit_hook(lambda s: exit_calls.append(("A", s)))
    state_b.add_enter_hook(lambda s: enter_calls.append(("B", s)))
    
    # Create FSM
    fsm = FSM(
        States.STATE_A,
        {
            States.STATE_A: state_a,
            States.STATE_B: state_b
        }
    )
    
    # Test transition and hooks
    fsm.handle_event(Event(Events.EVENT_1))
    assert exit_calls == [("A", States.STATE_A)]
    assert enter_calls == [("B", States.STATE_B)]

def test_event_with_data():
    # Create state with handler that uses event data
    state_a = State()
    received_data = []
    
    state_a.add_handler(
        Events.EVENT_WITH_DATA,
        lambda e: received_data.extend(e.args) or None
    )
    
    # Create FSM
    fsm = FSM(
        States.STATE_A,
        {States.STATE_A: state_a}
    )
    
    # Test event with data
    test_data = (42, "test")
    fsm.handle_event(Event(Events.EVENT_WITH_DATA, args=test_data))
    assert received_data == list(test_data)
