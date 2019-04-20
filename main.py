"""Run your game with python main.py."""
import curses

from game.prepare_game import prepare_animations
from engine.registry import get_registered_animations
from engine.event_loop import run_coros
from engine.utils import prepare_screen


def run_animations(scr):
    """Run all registered animations."""
    prepare_animations(scr)
    coros = get_registered_animations()
    run_coros(coros)


def main():
    """Create screen and do all the drawing."""
    stdscr = curses.initscr()
    prepare_screen(stdscr)
    curses.wrapper(run_animations)


if __name__ == '__main__':
    main()

