import unittest
from enum import Enum
from common_fsm import FSM, State, Event, Transition

class TestErrorHandling(unittest.TestCase):
    """Test error handling and error state functionality"""
    
    def setUp(self):
        """Set up test states and FSM"""
        class States(Enum):
            NORMAL = "normal"
            ERROR = "error"
            RECOVERED = "recovered"
        
        class Events(Enum):
            TRIGGER_ERROR = "trigger_error"
            RECOVER = "recover"
        
        self.States = States
        self.Events = Events
        
        # Normal state with handler that throws exception
        self.normal_state = State()
        self.normal_state.add_handler(
            Events.TRIGGER_ERROR,
            lambda e: 1/0  # ZeroDivisionError
        )
        
        # Error state
        self.error_state = State()
        self.error_state.add_handler(
            Events.RECOVER,
            lambda e: Transition(States.RECOVERED)
        )
        
        # Recovered state
        self.recovered_state = State()
        
        # Track state transitions
        self.transitions = []
        
        # Create FSM with error state
        self.fsm = FSM(
            initial_state=States.NORMAL,
            state_objects={
                States.NORMAL: self.normal_state,
                States.ERROR: self.error_state,
                States.RECOVERED: self.recovered_state
            },
            error_state=States.ERROR,
            validate_transitions=False,
            verbose=True
        )
        
        # Add hooks to track transitions
        self.error_state.add_enter_hook(
            lambda s: self.transitions.append(f"Entered {s.name.lower()}")
        )
        self.recovered_state.add_enter_hook(
            lambda s: self.transitions.append(f"Entered {s.name.lower()}")
        )
    
    def test_error_transition(self):
        """Test that exceptions trigger transition to error state"""
        # Trigger an error
        self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
        
        # Print for debugging
        print(f"Transitions: {self.transitions}")
        
        # Should transition to error state
        self.assertEqual(self.fsm.current_state, self.States.ERROR)
        self.assertIn("Entered error", self.transitions)
    
    def test_recovery(self):
        """Test recovery from error state"""
        # First trigger an error
        self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
        
        # Then recover
        self.fsm.handle_event(Event(self.Events.RECOVER))
        
        # Should transition to recovered state
        self.assertEqual(self.fsm.current_state, self.States.RECOVERED)
        self.assertIn("Entered recovered", self.transitions)
    
    def test_fsm_without_error_state(self):
        """Test FSM behavior without error state"""
        # Create FSM without error state
        fsm = FSM(
            initial_state=self.States.NORMAL,
            state_objects={
                self.States.NORMAL: self.normal_state,
                self.States.RECOVERED: self.recovered_state
            },
            verbose=True
        )
        
        # This should not crash the test, just log the error
        try:
            fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            # Should still be in NORMAL state
            self.assertEqual(fsm.current_state, self.States.NORMAL)
        except ZeroDivisionError:
            self.fail("FSM should catch exceptions when no error_state is defined")

if __name__ == '__main__':
    unittest.main() 