import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from common_fsm import FSM, State, Event, Transition  # Importera direkt från modulen
from enum import Enum

class SpeakerStates(Enum):
    OFF = "off"
    ON = "on"

class SpeakerEvents(Enum):
    POWER_ON = "power_on"
    POWER_OFF = "power_off"
    SET_VOLUME = "set_volume"
    TIMEOUT = "timeout"

class Speaker:
    def __init__(self):
        self.volume = 0
        
        # Create states
        off_state = State(verbose=True)
        off_state.add_handler(
            SpeakerEvents.POWER_ON,
            lambda event: Transition(SpeakerStates.ON)
        )
        off_state.add_exit_hook(lambda s: print("off_state exit hook: Powering up..."))

        on_state = State(timeout=5, verbose=True)
        on_state.add_handler(
            SpeakerEvents.POWER_OFF,
            lambda event: Transition(SpeakerStates.OFF)
        )
        on_state.add_handler(
            SpeakerEvents.SET_VOLUME,
            lambda event: self.set_volume_internal(event.args[0])  # Direkt anrop här
        )
        on_state.add_handler(
            SpeakerEvents.TIMEOUT,
            lambda event: print("on_state timeout handler: Powering down...") or Transition(SpeakerStates.OFF)
        )
        on_state.add_enter_hook(lambda s: print("on_state enter hook: Speaker is now active!"))
        on_state.add_exit_hook(lambda s: print("on_state exit hook: Powering down..."))

        # Create FSM
        self._fsm = FSM(
            SpeakerStates.OFF,  # Initial state
            # State objects:
            {
                SpeakerStates.OFF: off_state,
                SpeakerStates.ON: on_state
            },
            timeout_event=SpeakerEvents.TIMEOUT,
            verbose=True
        )

    def power_on(self) -> None:
        """Turn the speaker on"""
        self._fsm.handle_event(Event(SpeakerEvents.POWER_ON))

    def power_off(self) -> None:
        """Turn the speaker off"""
        self._fsm.handle_event(Event(SpeakerEvents.POWER_OFF))

    def set_volume(self, volume: int) -> None:
        """Request to set the speaker volume"""
        self._fsm.handle_event(Event(SpeakerEvents.SET_VOLUME, args=(volume,)))

    def set_volume_internal(self, volume: int) -> None:
        """Internal method to actually set the volume, called by state handler"""
        print(f"Setting volume (internal) to {volume}")
        self.volume = volume

    @property
    def state(self) -> SpeakerStates:
        """Get the current state of the speaker"""
        return self._fsm.current_state

def runSpeakerExample1():
    speaker = Speaker()

    # Test the FSM
    speaker.set_volume(10) # This should not be handled
    speaker.power_on()
    speaker.set_volume(10)
    speaker.power_off()

def runSpeakerExample2():
    speaker = Speaker()

    # Test the FSM
    speaker.power_on()
    speaker.set_volume(10)
    # After 5 seconds, the speaker should power off

if __name__ == "__main__":
    while True:
        choice = input("Run example 1 or 2? (1/2) (other to exit)")
        if choice == "1":
            runSpeakerExample1()
        elif choice == "2":
            runSpeakerExample2()
        else:
            print("Thanks for running the speaker example!")
            break
