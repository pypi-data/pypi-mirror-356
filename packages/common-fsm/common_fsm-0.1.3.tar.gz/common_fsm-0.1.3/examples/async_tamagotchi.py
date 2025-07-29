import asyncio
import logging
from enum import Enum
from common_fsm import AsyncFSM, AsyncState, Event, Transition
import random

# Konfigurera logging
logging.basicConfig(
    level=logging.INFO,
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

class AsyncPet:
    def __init__(self, name: str, debug_mode=False):
        self.name = name
        
        # Happy state - gets hungry after a while
        happy_state = AsyncState(timeout=5.0, verbose=True)
        happy_state.add_handler(
            Events.TIMEOUT,
            lambda e: self._print_message(f"{YELLOW}*{self.name} starts looking hungry*{RESET}") or Transition(States.HUNGRY)
        )
        happy_state.add_handler(
            Events.PLAY,
            lambda e: self._print_message(f"{GREEN}*{self.name} plays happily!*{RESET}") or None
        )
        happy_state.add_handler(
            Events.FEED,
            lambda e: self._print_message(f"{GREEN}*{self.name} doesn't want food right now*{RESET}") or None
        )
        happy_state.add_handler(
            Events.MEDICINE,
            lambda e: self._print_message(f"{GREEN}*{self.name} says 'yuck!'*{RESET}") or None
        )
        happy_state.add_enter_hook(
            lambda s: self._print_message(f"{GREEN}*{self.name} looks happy!*{RESET}")
        )

        # Hungry state - can get sick if not fed
        hungry_state = AsyncState(timeout=3.0, verbose=True)
        hungry_state.add_handler(
            Events.FEED,
            lambda e: self._print_message(f"{GREEN}*{self.name} eats contentedly*{RESET}") or Transition(States.HAPPY)
        )
        hungry_state.add_handler(
            Events.TIMEOUT,
            lambda e: self._print_message(f"{RED}*{self.name} got sick from hunger!*{RESET}") or Transition(States.SICK)
        )
        hungry_state.add_enter_hook(
            lambda s: self._print_message(f"{YELLOW}*{self.name} is hungry!*{RESET}")
        )

        # Sick state - needs medicine
        sick_state = AsyncState(verbose=True)
        sick_state.add_handler(
            Events.MEDICINE,
            lambda e: self._print_message(f"{GREEN}*{self.name} feels better*{RESET}") or Transition(States.HAPPY)
        )
        sick_state.add_handler(
            Events.FEED,
            lambda e: self._print_message(f"{RED}*Don't feed {self.name} when sick! Give medicine!*{RESET}") or None
        )
        sick_state.add_handler(
            Events.PLAY,
            lambda e: self._print_message(f"{RED}*{self.name} is too sick to play! Give medicine first!*{RESET}") or None
        )
        sick_state.add_enter_hook(
            lambda s: self._print_message(f"{RED}*{self.name} is sick!*{RESET}")
        )

        # Create FSM
        self._fsm = AsyncFSM(
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
        
        # For async operations
        self._queue = asyncio.Queue()
        self._running = False
        self._task = None
    
    def _print_message(self, message):
        """Helper to print messages (returns None for use in lambda)"""
        print(message)
        return None
    
    async def feed(self):
        """Feed the pet"""
        await self._fsm.handle_event(Event(Events.FEED))

    async def play(self):
        """Play with the pet"""
        await self._fsm.handle_event(Event(Events.PLAY))

    async def give_medicine(self):
        """Give medicine to the pet"""
        await self._fsm.handle_event(Event(Events.MEDICINE))
    
    async def start(self):
        """Start the pet's event loop"""
        self._running = True
        self._task = asyncio.create_task(self._event_loop())
        return self._task
    
    async def stop(self):
        """Stop the pet's event loop"""
        self._running = False
        if self._task:
            await self._task
        await self._fsm.shutdown()
    
    async def _event_loop(self):
        """Main event loop for processing commands"""
        try:
            while self._running:
                try:
                    # Wait for a command with a timeout
                    command = await asyncio.wait_for(self._queue.get(), 0.1)
                    
                    if command == "feed":
                        await self.feed()
                    elif command == "play":
                        await self.play()
                    elif command == "medicine":
                        await self.give_medicine()
                    
                    self._queue.task_done()
                except asyncio.TimeoutError:
                    # Just continue the loop
                    pass
        except asyncio.CancelledError:
            # Task was cancelled, clean up
            await self._fsm.shutdown()
            raise
    
    async def queue_command(self, command):
        """Queue a command to be processed"""
        await self._queue.put(command)

async def show_commands():
    """Display available commands"""
    print("\nCommands:")
    print("1: Feed")
    print("2: Play")
    print("3: Give medicine")
    print("q: Quit")
    print("\nWhat would you like to do?")

async def run_async_tamagotchi(debug_mode=False):
    """Run the async Tamagotchi game"""
    name = input("What would you like to name your pet? ")
    pet = AsyncPet(name, debug_mode)
    
    # Start the pet's event loop
    await pet.start()
    
    try:
        while True:
            await show_commands()
            cmd = await asyncio.get_event_loop().run_in_executor(None, input)
            
            if cmd.strip().lower() == 'q':
                print(f"\nGoodbye {name}!")
                break
            elif cmd == '1':
                await pet.queue_command("feed")
            elif cmd == '2':
                await pet.queue_command("play")
            elif cmd == '3':
                await pet.queue_command("medicine")
            else:
                print("Unknown command!")
    finally:
        # Make sure to stop the pet's event loop
        await pet.stop()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Run Async Tamagotchi game')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode (no timeouts)')
    args = parser.parse_args()
    
    asyncio.run(run_async_tamagotchi(debug_mode=False))#args.debug)) 