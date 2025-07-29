import logging
from enum import Enum
from common_fsm import FSM, State, Event, Transition
import time

logging.basicConfig(level=logging.INFO)

# ANSI färgkoder
RED = '\033[91m'      # Ljusröd
YELLOW = '\033[93m'   # Ljusgul
GREEN = '\033[92m'    # Ljusgrön
RESET = '\033[0m'     # Återställ färg

class States(Enum):
    RED = "red"
    YELLOW = "yellow"
    GREEN = "green"

class Events(Enum):
    START = "start"
    TIMEOUT = "timeout"

class TrafficLight:
    def __init__(self):
        # Red light: Timeout -> Green
        red_state = State(timeout=2.0, verbose=True)
        red_state.add_handler(
            Events.TIMEOUT,
            lambda event: print(f"{RED}Red timeout -> Green{RESET}") or Transition(States.GREEN)
        )
        red_state.add_enter_hook(lambda s: print(f"{RED}🔴 Red Light - STOP!{RESET}"))

        # Green light: Timeout -> Yellow
        green_state = State(timeout=2.0, verbose=True)
        green_state.add_handler(
            Events.TIMEOUT,
            lambda event: print(f"{GREEN}Green timeout -> Yellow{RESET}") or Transition(States.YELLOW)
        )
        green_state.add_enter_hook(lambda s: print(f"{GREEN}🟢 Green Light - GO!{RESET}"))

        # Yellow light: Timeout -> Red
        yellow_state = State(timeout=2.0, verbose=True)
        yellow_state.add_handler(
            Events.TIMEOUT,
            lambda event: print(f"{YELLOW}Yellow timeout -> Red{RESET}") or Transition(States.RED)
        )
        yellow_state.add_enter_hook(lambda s: print(f"{YELLOW}🟡 Yellow Light - PREPARE TO STOP!{RESET}"))

        # Create FSM
        self._fsm = FSM(
            States.RED,  # Initial state
            {
                States.RED: red_state,
                States.YELLOW: yellow_state,
                States.GREEN: green_state
            },
            timeout_event=Events.TIMEOUT,
            verbose=True
        )

    def start(self):
        """Start the traffic light sequence"""
        print("🚦 Starting traffic light sequence...")

    def shutdown(self):
        """Cleanup and stop the traffic light"""
        self._fsm.shutdown()

def run_traffic_light():
    light = TrafficLight()
    light.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nTraffic light stopping...")
        light.shutdown()
        print("Traffic light stopped")

if __name__ == "__main__":
    run_traffic_light() 