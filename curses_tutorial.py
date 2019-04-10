import curses
import time


def draw(canvas):
    row, column = (15, 2)
    canvas.addstr(column, row, 'a')
    canvas.refresh()
    time.sleep(3)


if __name__ == '__main__':
    canvas = curses.initscr()
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas.border()
    canvas.refresh()
    curses.update_lines_cols()
    curses.wrapper(draw)
