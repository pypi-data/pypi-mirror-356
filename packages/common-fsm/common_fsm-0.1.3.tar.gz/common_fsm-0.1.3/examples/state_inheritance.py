from enum import Enum
from common_fsm import FSM, State, Event, Transition

# Definiera states och events
class States(Enum):
    IDLE = "idle"
    WORKING = "working"
    PAUSED = "paused"
    ERROR = "error"

class Events(Enum):
    START = "start"
    STOP = "stop"
    PAUSE = "pause"
    RESUME = "resume"
    RESET = "reset"
    ERROR = "error"

# Skapa en basstate-klass som hanterar gemensamma events
class BaseState(State):
    def __init__(self, verbose=False):
        super().__init__(verbose)
        
        # Lägg till gemensamma handlers för alla states
        self.add_handler(Events.RESET, self.handle_reset)
        self.add_handler(Events.ERROR, self.handle_error)
    
    def handle_reset(self, event):
        print("Resetting to IDLE state")
        return Transition(States.IDLE)
    
    def handle_error(self, event):
        print("Error occurred, transitioning to ERROR state")
        return Transition(States.ERROR)

# Skapa specifika states som ärver från BaseState
class IdleState(BaseState):
    def __init__(self):
        super().__init__(verbose=True)
        
        # Lägg till state-specifika handlers
        self.add_handler(Events.START, self.handle_start)
    
    def handle_start(self, event):
        print("Starting work")
        return Transition(States.WORKING)

class WorkingState(BaseState):
    def __init__(self):
        super().__init__(verbose=True)
        
        # Lägg till state-specifika handlers
        self.add_handler(Events.STOP, self.handle_stop)
        self.add_handler(Events.PAUSE, self.handle_pause)
    
    def handle_stop(self, event):
        print("Stopping work")
        return Transition(States.IDLE)
    
    def handle_pause(self, event):
        print("Pausing work")
        return Transition(States.PAUSED)

class PausedState(BaseState):
    def __init__(self):
        super().__init__(verbose=True)
        
        # Lägg till state-specifika handlers
        self.add_handler(Events.RESUME, self.handle_resume)
        self.add_handler(Events.STOP, self.handle_stop)
    
    def handle_resume(self, event):
        print("Resuming work")
        return Transition(States.WORKING)
    
    def handle_stop(self, event):
        print("Stopping work")
        return Transition(States.IDLE)

class ErrorState(BaseState):
    def __init__(self):
        super().__init__(verbose=True)
        
        # I error-state vill vi bara hantera reset
        # Vi behöver inte lägga till någon ny handler eftersom BaseState redan har reset

# Skapa FSM
def create_fsm():
    return FSM(
        initial_state=States.IDLE,
        state_objects={
            States.IDLE: IdleState(),
            States.WORKING: WorkingState(),
            States.PAUSED: PausedState(),
            States.ERROR: ErrorState()
        },
        error_state=States.ERROR,
        verbose=True
    )

# Testa FSM
def test_fsm():
    fsm = create_fsm()
    
    print(f"Initial state: {fsm.current_state.name}")
    
    # Testa några transitions
    fsm.handle_event(Event(Events.START))
    print(f"Current state: {fsm.current_state.name}")
    
    fsm.handle_event(Event(Events.PAUSE))
    print(f"Current state: {fsm.current_state.name}")
    
    fsm.handle_event(Event(Events.RESUME))
    print(f"Current state: {fsm.current_state.name}")
    
    # Testa gemensam handler (reset)
    fsm.handle_event(Event(Events.RESET))
    print(f"Current state: {fsm.current_state.name}")
    
    # Testa error-hantering
    fsm.handle_event(Event(Events.START))
    fsm.handle_event(Event(Events.ERROR))
    print(f"Current state: {fsm.current_state.name}")

if __name__ == "__main__":
    test_fsm() 