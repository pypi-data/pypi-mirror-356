"""
PyFSM - A simple and flexible Finite State Machine implementation in Python.
"""

from .fsm import FSM, State, Event, Transition
from .async_fsm import AsyncFSM, AsyncState

__version__ = "0.1.2"
__all__ = ['FSM', 'State', 'Event', 'Transition', 'AsyncFSM', 'AsyncState'] 