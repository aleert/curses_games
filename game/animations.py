# -*- coding: utf-8 -*-

"""Animations schemes used in project."""
import asyncio
import curses
import random
from itertools import cycle

from engine.registry import get_frames
from engine.utils import delay, draw_frame, get_frames_shape, read_controls
from game.ship_state import Spaceship

# set it's properties in ship animation so stars will be aware
# of positions occupied by ship
ship_state = Spaceship(row=0, column=0, sizes=(), rows=0, cols=0)


async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):  # noqa: Z210
    """Display animation of gun shot. Direction and speed can be specified."""
    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(scr, row: int, column: int, symbol: str = '*') -> None:  # noqa: Z213
    """Display blinking `symbol`."""
    flicker = random.random() * 5

    scr.addstr(row, column, symbol, curses.A_DIM)
    await delay(flicker)

    while True:
        # stars shouldn't blink through our ship
        if (row, column) in ship_state.occupied_positions:
            await asyncio.sleep(0)
            continue

        scr.addstr(row, column, symbol, curses.A_DIM)
        await delay(2)

        scr.addstr(row, column, symbol)
        await delay(0.3)  # noqa: Z432

        scr.addstr(row, column, symbol, curses.A_BOLD)
        await delay(0.5)

        scr.addstr(row, column, symbol)
        await delay(0.3)


def get_random_blinks(scr, n_blinks=55):  # noqa: Z210
    """Get blinks coroutines with randomised position."""
    symbols = ('*', ':', '+', '.')
    max_y, max_x = scr.getmaxyx()
    max_stars = (max_x - 2) * (max_y - 2)
    if n_blinks > max_stars:
        raise ValueError('too many stars for this screen, please use no more than ', max_stars)
    occupied_positions = set()
    while len(occupied_positions) < n_blinks:
        row = random.randint(1, max_y - 2)
        col = random.randint(1, max_x - 2)
        if (row, col) in occupied_positions:
            continue

        symbol = random.choice(symbols)
        occupied_positions.add((row, col))
        yield blink(scr, row, col, symbol=symbol)


async def ship(  # noqa: Z210
    scr,
    start_row: int,
    start_column: int,
    frames_name: str,
    updates_per_second: int = 10,
) -> None:
    """Draw ship animation and move it with arrows."""
    # set ship state to keep track of positions it occupies
    frames = get_frames(frames_name)
    frame_sizes = get_frames_shape(frames)
    ship_state.sizes = frame_sizes

    # check our ship fits into terminal window
    max_frame_rows = len(frame_sizes)
    max_frame_cols = sum(
        max(frame_sizes, key=lambda frame: frame[0] + frame[1]),
    )
    max_rows, max_cols = scr.getmaxyx()
    if (start_row + ship_state.rows >= max_rows
            or start_column + ship_state.cols >= max_cols):  # noqa: Z318, Z319, W503
        raise RuntimeError(
            'Your terminal window is too small for a ship to fit in. '
            'Please increase your terminal window.',  # noqa: Z326
        )

    # update state if everything is fine
    ship_state.row, ship_state.col = start_row, start_column  # noqa: Z446
    ship_state.rows, ship_state.cols = max_frame_rows, max_frame_cols  # noqa: Z446

    # have to start frame_loop outside of for loop as we should change frames inside
    frame_loop = cycle(frames)

    for frame in frame_loop:
        rows_direction, columns_direction, space_pressed = read_controls(scr)

        prev_frame = next(frame_loop)
        draw_frame(scr, start_row, start_column, prev_frame, negative=True)
        # have to rotate one more time there
        next(frame_loop)
        draw_frame(scr, start_row, start_column, frame)
        await delay(1 / updates_per_second)

        if rows_direction:
            draw_frame(scr, start_row, start_column, frame, negative=True)
            new_row = start_row + rows_direction

            start_row = new_row \
                if 0 < new_row and new_row + max_frame_rows < max_rows \
                else start_row
            ship_state.row = start_row
            # redraw to avoid ship flickering when moving
            draw_frame(scr, start_row, start_column, frame)

        if columns_direction:
            draw_frame(scr, start_row, start_column, frame, negative=True)
            new_col = start_column + columns_direction

            start_column = new_col \
                if 0 < new_col and new_col + max_frame_cols < max_cols \
                else start_column
            ship_state.col = start_column
            # redraw to avoid ship flickering when moving
            draw_frame(scr, start_row, start_column, frame)
