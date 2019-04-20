"""Useful utils for curses."""
import curses
from itertools import zip_longest
from typing import Tuple, NewType, Iterator, Container, Iterable
from pathlib import Path


SPACE_KEY_CODE = 32
LEFT_KEY_CODE = 260
RIGHT_KEY_CODE = 261
UP_KEY_CODE = 259
DOWN_KEY_CODE = 258


def read_controls(canvas):
    """Read keys pressed and returns tuple witl controls state."""

    rows_direction = columns_direction = 0
    space_pressed = False

    while True:
        pressed_key_code = canvas.getch()

        if pressed_key_code == -1:
            # https://docs.python.org/3/library/curses.html#curses.window.getch
            break

        if pressed_key_code == UP_KEY_CODE:
            rows_direction = -1

        if pressed_key_code == DOWN_KEY_CODE:
            rows_direction = 1

        if pressed_key_code == RIGHT_KEY_CODE:
            columns_direction = 1

        if pressed_key_code == LEFT_KEY_CODE:
            columns_direction = -1

        if pressed_key_code == SPACE_KEY_CODE:
            space_pressed = True

    return rows_direction, columns_direction, space_pressed


def draw_frame(canvas, start_row: int, start_column: int, text: str, negative=False):
    """
    Draw multiline text fragment on canvas.

     Erase text instead of drawing if negative=True is specified.
     """

    rows_number, columns_number = canvas.getmaxyx()

    for row, line in enumerate(text.splitlines(), round(start_row)):
        if row < 0:
            continue

        if row >= rows_number:
            break

        for column, symbol in enumerate(line, round(start_column)):
            if column < 0:
                continue

            if column >= columns_number:
                break

            if symbol == ' ':
                continue

            # Check that current position it is not in a lower right corner of the window
            # Curses will raise exception in that case. Don`t ask why…
            # https://docs.python.org/3/library/curses.html#curses.window.addch
            if row == rows_number - 1 and column == columns_number - 1:
                continue

            symbol = symbol if not negative else ' '
            canvas.addch(row, column, symbol)


StartPos = NewType('StartPos', int)
Length = NewType('Length', int)
Row_Nonempty_Symbols = Tuple[StartPos, Length]


def get_frame_shape(text: str) -> Tuple[Tuple[StartPos, Length], ...]:
    """
    Calculate sizes of multiline text fragment.

     For every nonempty frame line tuple(first_nonempty_char, nonempty_chars_len)
     calculated.
     Return tuple with results for every line in frame.

     eg: frame='  *\n * \n***\n'
     get_frame_shape(frame)
     will result in ((2,1), (1, 1), (0, 3))
     """
    lines = text.splitlines()
    start_pos = lambda line: StartPos(len(line) - len(line.lstrip()))
    size = lambda line: Length(len(line.strip()))
    sizes = tuple((start_pos(l), size(l)) for l in lines)
    return sizes


def get_frames_shape(frames: Iterable[str]) -> Tuple[Row_Nonempty_Symbols, ...]:
    """
    Return frame shape as in get_frame_shape, but will pick rows with max width among frames.
    """
    # tuple of first rows sizes, second rows sizes etc
    rows_among_frames = zip_longest(*(get_frame_shape(frame) for frame in frames))
    # get row with maximum length
    row_with_max_length = lambda row_of_rows: max(row_of_rows, key=lambda row: row[1])
    return tuple(row_with_max_length(row_of_rows)
                 for row_of_rows in rows_among_frames)


def load_frame_from_file(path: str) -> str:
    """Load multiline frame from a text file."""
    try:
        file = Path(path)
        frame = file.read_text()
        return frame
    except OSError:
        raise OSError('your file {0} cannot be loaded'.format(path))


def prepare_screen(scr):
    """Draw border, make async key input and other prep."""
    scr.border()
    scr.nodelay(True)
    curses.curs_set(False)
    curses.update_lines_cols()
    # needed to get black character background for terminals with color support
    # https://stackoverflow.com/questions/18551558/how-to-use-terminal-color-palette-with-curses
    if curses.can_change_color():
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, getattr(curses, 'COLORS')):
            curses.init_pair(i + 1, i, -1)
