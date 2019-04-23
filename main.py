# -*- coding: utf-8 -*-

"""Run your game with python main.py."""
import curses

from engine.event_loop import run_coros
from engine.registry import FRAME_RATE, animation_registry
from engine.utils import prepare_screen
from game.prepare_game import prepare_animations


def run_animations(scr):
    """Run all registered animations."""
    prepare_animations(scr)
    coros = animation_registry
    run_coros(coros, FRAME_RATE)


def main():
    """Create screen and do all the drawing."""
    stdscr = curses.initscr()
    prepare_screen(stdscr)
    curses.wrapper(run_animations)


if __name__ == '__main__':
    main()
