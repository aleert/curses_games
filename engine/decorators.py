"""Useful decorators to work with animations."""
import asyncio
import time
from functools import wraps
from typing import Callable


def delay_animation_frames_in_coro(delay: float) -> Callable:
    """Specify delay between frames of animation."""
    def _delay_animation(coro):
        @wraps(coro)
        async def _wrapper(*args, **kwargs):
            start_time = time.time()
            coroutine = coro(*args, **kwargs)
            while True:
                if time.time() > start_time + delay:
                    try:
                        coroutine.send(None)
                    # reraising exceptions in decorators can be tricky
                    # just raise wont work there, we have to return
                    # to be able to catch it in event_loop.run_coros
                    except StopIteration:
                        return StopIteration
                    await asyncio.sleep(0)
                    start_time = time.time()
                await asyncio.sleep(0)
        return _wrapper
    return _delay_animation
