"""Functions responsible for running corutines."""
from typing import Deque


def run_coros(scr, animations: Deque) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    while animations:
        coro = animations[0]
        try:
            coro.send(None)
            animations.rotate(1)
        except StopIteration:
            animations.remove(coro)

