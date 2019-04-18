"""Functions responsible for running corutines."""
import asyncio
from itertools import cycle, islice
from typing import Sequence, Deque

from engine.decorators import delay_animation_frames_in_coro
from .registry import get_registered_animations, register_animation


def run_coros(scr, animations: Deque) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    while animations:
        coro = animations[0]
        try:
            coro.send(None)
            animations.rotate(1)
        except StopIteration:
            animations.remove(coro)
