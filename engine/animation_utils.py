import asyncio
from typing import Sequence

from .utils import get_frame_size, draw_frame


async def animate_frames(scr, frames: Sequence, start_row, start_column, in_cycle=True):
    """
    Animate sequence of string frames in cycle or once.

    To specify delay between frames use:
     decorators.delay_animation_frames_in_coro(delay=seconds)(animate_frames(*params))
     To delete frame use negative=True.
     """
    # yields (frame_rows, frame_columns) tuples
    frame_sizes = (get_frame_size(frame) for frame in frames)
    max_cols, max_rows = scr.getmaxyx()
    # TODO better value message (frame_name mb?)
    if any((1 > start_column+col > max_cols-2) or
           (1 > start_row+row > max_rows-2)
           for (col, row) in frame_sizes):
        raise ValueError('One of your frames too big to be fit at that position')

    # wonder if this is a good idea
    if not in_cycle:
        cycle = lambda x: x

    for frame in cycle(frames):
        draw_frame(scr, start_row, start_column, frame, negative=True)
        draw_frame(scr, start_row, start_column, frame)
        await asyncio.sleep(0)
