"""Functions responsible for running corutines."""
import time
from typing import List, Coroutine


def run_coros(animations: List[Coroutine], frame_rate: float = 50) -> None:
    """Run coroutines in roundrobin, removing exhausted ones."""
    while animations:
        for animation in animations:
            try:
                animation.send(None)
            except StopIteration:
                animations.remove(animation)

        time.sleep(1/frame_rate)


