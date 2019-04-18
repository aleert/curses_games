"""Run your game with python main.py."""
import asyncio
import curses

from engine.decorators import delay_animation_frames_in_coro
from game.prepare_game import prepare_animations
from engine.registry import get_registered_animations, register_animation
from engine.event_loop import run_coros
from engine.utils import prepare_screen


try:
    from game.prepare_game import FRAME_RATE
except ImportError:
    FRAME_RATE = 30


@delay_animation_frames_in_coro(1/FRAME_RATE)
async def refresh_screen(scr):
    scr.refresh()
    await asyncio.sleep(0)


def run_animations(scr):
    """Run all registered animations."""
    register_animation(refresh_screen(scr))
    prepare_animations(scr)
    coros = get_registered_animations()
    run_coros(scr, coros)


def main():
    """Create screen and do all the drawing."""
    stdscr = curses.initscr()
    prepare_screen(stdscr)
    curses.wrapper(run_animations)


if __name__ == '__main__':
    main()
