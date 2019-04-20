"""Functions responsible for running corutines."""
import time
from typing import List, Coroutine


try:
    from game.prepare_game import FRAME_RATE
except ImportError:
    FRAME_RATE = 50


def run_coros(animations: List[Coroutine]) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    while animations:
        for animation in animations:
            try:
                animation.send(None)
            except StopIteration:
                animations.remove(animation)

        time.sleep(1/FRAME_RATE)


