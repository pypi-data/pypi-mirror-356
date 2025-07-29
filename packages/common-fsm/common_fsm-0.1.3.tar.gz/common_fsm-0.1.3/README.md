# Common-FSM

A simple and flexible Finite State Machine implementation in Python.

## Features

- Simple and intuitive API
- Type-safe with generics support
- Optional state timeouts
- Enter/exit hooks for states
- Verbose mode for debugging
- Fully tested

## Installation

```bash
pip install common-fsm
```

## Quick Start

```python
from enum import Enum
from common_fsm import FSM, State, Event, Transition

# Define your states and events
class States(Enum):
    OFF = "off"
    ON = "on"

class Events(Enum):
    POWER_ON = "power_on"
    POWER_OFF = "power_off"

# Create states with handlers
off_state = State()
off_state.add_handler(
    Events.POWER_ON,
    lambda event: Transition(States.ON)
)

on_state = State()
on_state.add_handler(
    Events.POWER_OFF,
    lambda event: Transition(States.OFF)
)

# Create FSM
fsm = FSM(
    States.OFF,  # Initial state
    {
        States.OFF: off_state,
        States.ON: on_state
    }
)

# Use the FSM
fsm.handle_event(Event(Events.POWER_ON))  # Transitions to ON
fsm.handle_event(Event(Events.POWER_OFF)) # Transitions to OFF
```

## Advanced Features

### State Timeouts

States can have automatic timeouts:

```python
# State with 5 second timeout
on_state = State(timeout=5.0)
on_state.add_handler(
    Events.TIMEOUT,
    lambda event: Transition(States.OFF)
)

fsm = FSM(
    States.OFF,
    {
        States.OFF: off_state,
        States.ON: on_state
    },
    timeout_event=Events.TIMEOUT
)
```

### State Hooks

Add hooks for state transitions:

```python
on_state.add_enter_hook(lambda s: print("Entering ON state"))
on_state.add_exit_hook(lambda s: print("Exiting ON state"))
```

## Examples

See the `examples/` directory for more detailed examples, including:
- Basic state machine
- Speaker with volume control
- Traffic light controller

## Development

Clone the repository:
```bash
git clone https://github.com/commonai/python-fsm.git
cd python-fsm
```

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
