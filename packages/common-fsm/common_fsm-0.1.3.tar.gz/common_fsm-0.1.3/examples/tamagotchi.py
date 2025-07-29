import logging
from enum import Enum
from common_fsm import FSM, State, Event, Transition
import time
import random
import argparse

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,  # Eller logging.DEBUG för ännu mer detaljer
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# ANSI color codes for different states
GREEN = '\033[92m'    # Happy
YELLOW = '\033[93m'   # Hungry
BLUE = '\033[94m'     # Sleeping
RED = '\033[91m'      # Sick
RESET = '\033[0m'

class States(Enum):
    HAPPY = "happy"
    HUNGRY = "hungry"
    SLEEPING = "sleeping"
    SICK = "sick"

class Events(Enum):
    FEED = "feed"
    PLAY = "play"
    CLEAN = "clean"
    MEDICINE = "medicine"
    TIMEOUT = "timeout"

class Pet:
    def __init__(self, name: str, debug_mode=False):
        self.name = name
        
        # Happy state - gets hungry after a while
        happy_state = State(timeout=5.0, verbose=True)
        happy_state.add_handler(
            Events.TIMEOUT,
            lambda e: print(f"{YELLOW}*{self.name} starts looking hungry*{RESET}") or Transition(States.HUNGRY)
        )
        happy_state.add_handler(
            Events.PLAY,
            lambda e: print(f"{GREEN}*{self.name} plays happily!*{RESET}") or None
        )
        happy_state.add_handler(
            Events.FEED,
            lambda e: print(f"{GREEN}*{self.name} doesn't want food right now*{RESET}") or None
        )
        happy_state.add_handler(
            Events.MEDICINE,
            lambda e: print(f"{GREEN}*{self.name} says 'yuck!'*{RESET}") or None
        )
        happy_state.add_enter_hook(
            lambda s: print(f"{GREEN}*{self.name} looks happy!*{RESET}")
        )

        # Hungry state - can get sick if not fed
        hungry_state = State(timeout=3.0, verbose=True)
        hungry_state.add_handler(
            Events.FEED,
            lambda e: print(f"{GREEN}*{self.name} eats contentedly*{RESET}") or Transition(States.HAPPY)
        )
        hungry_state.add_handler(
            Events.TIMEOUT,
            lambda e: print(f"{RED}*{self.name} got sick from hunger!*{RESET}") or Transition(States.SICK)
        )
        hungry_state.add_enter_hook(
            lambda s: print(f"{YELLOW}*{self.name} is hungry!*{RESET}")
        )

        # Sick state - needs medicine
        sick_state = State(verbose=True)
        sick_state.add_handler(
            Events.MEDICINE,
            lambda e: print(f"{GREEN}*{self.name} feels better*{RESET}") or Transition(States.HAPPY)
        )
        sick_state.add_handler(
            Events.FEED,
            lambda e: print(f"{RED}*Don't feed {self.name} when sick! Give medicine!*{RESET}") or None
        )
        sick_state.add_handler(
            Events.PLAY,
            lambda e: print(f"{RED}*{self.name} is too sick to play! Give medicine first!*{RESET}") or None
        )
        sick_state.add_enter_hook(
            lambda s: print(f"{RED}*{self.name} is sick!*{RESET}")
        )

        # Create FSM
        self._fsm = FSM(
            States.HAPPY,
            {
                States.HAPPY: happy_state,
                States.HUNGRY: hungry_state,
                States.SICK: sick_state,
            },
            timeout_event=Events.TIMEOUT,
            verbose=True,
            debug_mode=debug_mode
        )
    
    def bye(self):
        self._fsm.shutdown()

    def feed(self):
        self._fsm.handle_event(Event(Events.FEED))

    def play(self):
        self._fsm.handle_event(Event(Events.PLAY))

    def give_medicine(self):
        self._fsm.handle_event(Event(Events.MEDICINE))

def show_commands():
    print("\nCommands:")
    print("1: Feed")
    print("2: Play")
    print("3: Give medicine")
    print("q: Quit")
    print("\nWhat would you like to do?")

def run_tamagotchi(debug_mode=False):
    name = input("What would you like to name your pet? ")
    pet = Pet(name, debug_mode)
    
    while True:
        show_commands()
        cmd = input().strip().lower()
        
        if cmd == 'q':
            print(f"\nGoodbye {name}!")
            pet.bye()
            break
        elif cmd == '1':
            pet.feed()
        elif cmd == '2':
            pet.play()
        elif cmd == '3':
            pet.give_medicine()
        else:
            print("Unknown command!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Tamagotchi game')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode (no timeouts)')
    args = parser.parse_args()
    
    run_tamagotchi(debug_mode=False) 