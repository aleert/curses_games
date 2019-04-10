"""Functions responsible for running corutines."""
from itertools import cycle, islice
from typing import Sequence

from .registry import AnimationRegistry

r = AnimationRegistry()


def run_coros(scr, coroutines: Sequence) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    num_active = len(coroutines)
    nexts = cycle(coroutines)
    while num_active:
        try:
            coro = next(nexts)
            coro.send(None)
            scr.refresh()
        except StopIteration:
            num_active -= 1
            nexts = cycle(islice(nexts, num_active))
