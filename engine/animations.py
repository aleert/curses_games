"""Animations schemes used in project."""
import asyncio
import curses
import random
import time

from .decorators import delay_animation_frames_in_coro


@delay_animation_frames_in_coro(0.5)
async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
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


async def blink(scr, row, column, symbol='*'):
    """Display blinking `symbol`."""
    animation = [(curses.A_DIM, 0.3), (curses.A_NORMAL, 2),
                 (curses.A_BOLD, 0.3), (curses.A_NORMAL, 0.5)]

    flicker = random.random()*5
    # duration = lambda frame: frame[1]
    # frame_duration = lambda frame_num: sum((duration(frame) for frame in animation[:frame_num]))+flicker

    blinks = [False, False, False, False]
    # delays = [frame_duration(f) for f in range(len(animation))]

    start_time = time.time()
    while True:
        if not blinks[0]:
            scr.addstr(row, column, symbol, curses.A_DIM)
            blinks[0] = True
            await asyncio.sleep(0)

        if not blinks[1] and time.time() > start_time + .3 + flicker:
            scr.addstr(row, column, symbol)
            blinks[1] = True
            await asyncio.sleep(0)

        if not blinks[2] and time.time() > start_time + 2.3 + flicker:
            scr.addstr(row, column, symbol, curses.A_BOLD)
            blinks[2] = True
            await asyncio.sleep(0)

        if not blinks[3] and time.time() > start_time + 2.6 + flicker:
            scr.addstr(row, column, symbol)
            blinks[3] = True
            await asyncio.sleep(0)

        if time.time() > start_time + 3.1 + flicker:
            start_time = time.time()
            blinks = [False, False, False, False]
        await asyncio.sleep(0)


def get_random_blinks(scr, n=55):
    """Get blinks coroutines with randomised position."""
    symbols = ('*', ':', '+', '.')
    max_y, max_x = scr.getmaxyx()
    max_stars = (max_x - 2) * (max_y - 2)
    if n > max_stars:
        raise ValueError('too many stars for this screen, please use no more than ', max_stars)
    occupied_positions = set()
    while len(occupied_positions) < n:
        row = random.randint(1, max_y-2)
        col = random.randint(1, max_x-2)
        if (row, col) in occupied_positions:
            continue

        symbol = random.choice(symbols)
        occupied_positions.add((row, col))
        yield blink(scr, row, col, symbol=symbol)
