import unittest
import asyncio
from enum import Enum
from common_fsm import AsyncFSM, AsyncState, Event, Transition

class TestAsyncErrorHandling(unittest.TestCase):
    """Test error handling in the asynchronous FSM"""
    
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
        self.normal_state = AsyncState()
        
        # Sync handler that throws exception
        self.normal_state.add_handler(
            Events.TRIGGER_ERROR,
            lambda e: 1/0  # ZeroDivisionError
        )
        
        # Error state
        self.error_state = AsyncState()
        self.error_state.add_handler(
            Events.RECOVER,
            lambda e: Transition(States.RECOVERED)
        )
        
        # Recovered state
        self.recovered_state = AsyncState()
        
        # Track state transitions
        self.transitions = []
        
        # Add hooks to track transitions
        self.error_state.add_enter_hook(
            lambda s: self.transitions.append(f"Entered {s.name.lower()}")
        )
        self.recovered_state.add_enter_hook(
            lambda s: self.transitions.append(f"Entered {s.name.lower()}")
        )
        
        # Create FSM with error state
        self.fsm = AsyncFSM(
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
    
    def run_async_test(self, coro):
        """Helper to run async tests"""
        return asyncio.run(coro)
    
    def test_sync_error_transition(self):
        """Test that sync exceptions trigger transition to error state"""
        async def test_coro():
            # Trigger an error
            await self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            
            # Should transition to error state
            self.assertEqual(self.fsm.current_state, self.States.ERROR)
            self.assertIn("Entered error", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_async_error_transition(self):
        """Test that async exceptions trigger transition to error state"""
        async def async_error_handler(event):
            await asyncio.sleep(0.1)  # Simulate async work
            raise ValueError("Async error")
        
        # Replace the handler with an async one
        self.normal_state.add_handler(self.Events.TRIGGER_ERROR, async_error_handler)
        
        async def test_coro():
            # Trigger an error
            await self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            
            # Should transition to error state
            self.assertEqual(self.fsm.current_state, self.States.ERROR)
            self.assertIn("Entered error", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_recovery(self):
        """Test recovery from error state"""
        async def test_coro():
            # First trigger an error
            await self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            
            # Then recover
            await self.fsm.handle_event(Event(self.Events.RECOVER))
            
            # Should transition to recovered state
            self.assertEqual(self.fsm.current_state, self.States.RECOVERED)
            self.assertIn("Entered recovered", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_async_recovery(self):
        """Test async recovery from error state"""
        async def async_recover_handler(event):
            await asyncio.sleep(0.1)  # Simulate async work
            return Transition(self.States.RECOVERED)
        
        # Replace the handler with an async one
        self.error_state.add_handler(self.Events.RECOVER, async_recover_handler)
        
        async def test_coro():
            # First trigger an error
            await self.fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
            
            # Then recover
            await self.fsm.handle_event(Event(self.Events.RECOVER))
            
            # Should transition to recovered state
            self.assertEqual(self.fsm.current_state, self.States.RECOVERED)
            self.assertIn("Entered recovered", self.transitions)
        
        self.run_async_test(test_coro())
    
    def test_fsm_without_error_state(self):
        """Test FSM behavior without error state"""
        # Create FSM without error state
        fsm = AsyncFSM(
            initial_state=self.States.NORMAL,
            state_objects={
                self.States.NORMAL: self.normal_state,
                self.States.RECOVERED: self.recovered_state
            },
            verbose=True
        )
        
        async def test_coro():
            try:
                # This should not crash the test, just log the error
                await fsm.handle_event(Event(self.Events.TRIGGER_ERROR))
                # Should still be in NORMAL state
                self.assertEqual(fsm.current_state, self.States.NORMAL)
            except ZeroDivisionError:
                self.fail("AsyncFSM should catch exceptions when no error_state is defined")
        
        self.run_async_test(test_coro())

if __name__ == '__main__':
    unittest.main() 