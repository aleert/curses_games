"""Run your game with python main.py."""
import curses

from game.prepare_game import prepare_animations
from engine.registry import AnimationRegistry
from engine.event_loop import run_coros
from engine.utils import prepare_screen


r = AnimationRegistry()


def run_animations(scr):
    """Run all registered animations."""
    prepare_animations(scr)
    coros = r.registered
    run_coros(scr, coros)


def main():
    """Create screen and do all the drawing."""
    stdscr = curses.initscr()
    prepare_screen(stdscr)
    curses.wrapper(run_animations)


if __name__ == '__main__':
    main()
