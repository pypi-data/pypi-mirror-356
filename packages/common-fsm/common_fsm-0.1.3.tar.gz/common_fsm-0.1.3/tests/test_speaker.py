import pytest
from enum import Enum
from common_fsm import FSM, State, Event, Transition
import time

# Test enums for the speaker example
class SpeakerStates(Enum):
    OFF = "off"
    ON = "on"

class SpeakerEvents(Enum):
    POWER_ON = "power_on"
    POWER_OFF = "power_off"
    SET_VOLUME = "set_volume"
    TIMEOUT = "timeout"  # Ny event för timeout

class Speaker:
    def __init__(self):
        self.volume = 0
        
        # Create states
        off_state = State()
        off_state.add_handler(
            SpeakerEvents.POWER_ON,
            lambda event: Transition(SpeakerStates.ON)
        )
        off_state.add_exit_hook(lambda s: print("Powering up..."))

        # ON state med 5 sekunders timeout
        on_state = State(timeout=5.0)  
        on_state.add_handler(
            SpeakerEvents.POWER_OFF,
            lambda event: Transition(SpeakerStates.OFF)
        )
        on_state.add_handler(
            SpeakerEvents.SET_VOLUME,
            lambda event: self.set_volume_internal(event.args[0]) or None
        )
        on_state.add_handler(
            SpeakerEvents.TIMEOUT,
            lambda event: Transition(SpeakerStates.OFF)  # Stäng av vid timeout
        )
        on_state.add_enter_hook(lambda s: print("Speaker is now active!"))
        on_state.add_exit_hook(lambda s: print("Powering down..."))

        # Create FSM with timeout support
        self._fsm = FSM(
            SpeakerStates.OFF,
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
        if self.state == SpeakerStates.OFF:
            raise RuntimeError("Cannot set volume while speaker is off")
        if not 0 <= volume <= 100:
            raise ValueError("Volume must be between 0 and 100")
        self._fsm.handle_event(Event(SpeakerEvents.SET_VOLUME, args=(volume,)))

    def set_volume_internal(self, volume: int) -> None:
        """Internal method to actually set the volume, called by state handler"""
        self.volume = volume

    @property
    def state(self) -> SpeakerStates:
        """Get the current state of the speaker"""
        return self._fsm.current_state

# Tests
def test_speaker_initial_state():
    speaker = Speaker()
    assert speaker.state == SpeakerStates.OFF
    assert speaker.volume == 0

def test_speaker_power_cycle():
    speaker = Speaker()
    speaker.power_on()
    assert speaker.state == SpeakerStates.ON
    speaker.power_off()
    assert speaker.state == SpeakerStates.OFF

def test_volume_control():
    speaker = Speaker()
    speaker.power_on()
    speaker.set_volume(50)
    assert speaker.volume == 50

def test_volume_validation():
    speaker = Speaker()
    speaker.power_on()
    
    with pytest.raises(ValueError):
        speaker.set_volume(101)
    
    with pytest.raises(ValueError):
        speaker.set_volume(-1)

def test_volume_while_off():
    speaker = Speaker()
    with pytest.raises(RuntimeError):
        speaker.set_volume(50)

def test_speaker_timeout():
    speaker = Speaker()
    speaker.power_on()
    assert speaker.state == SpeakerStates.ON
    time.sleep(5.1)  # Vänta lite längre än timeout
    assert speaker.state == SpeakerStates.OFF 