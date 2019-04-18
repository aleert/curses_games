"""Functions responsible for running corutines."""
from itertools import cycle, islice
from typing import Sequence, Deque

from .registry import get_registered_animations



def run_coros(scr, coroutines: Sequence) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    registered_animations: Deque = get_registered_animations()
    while registered_animations:
        try:
            coro = registered_animations[0]
            coro.send(None)
            registered_animations.rotate(1)
            scr.refresh()
        except StopIteration:
            registered_animations.remove(coro)
