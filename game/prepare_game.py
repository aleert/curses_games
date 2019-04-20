"""
Provide prepare_animation(curses_screen) callable.

That callable should register all animations you need when invoked.
"""
from engine.registry import register_animation, register_frame
from engine.utils import load_frame_from_file
from game.animations import fire, get_random_blinks, ship


# default FRAME_RATE is 50
# FRAME_RATE = 15


def prepare_frames():
    """Load frames from file and register them."""
    ship_f1 = load_frame_from_file('./game/assets/animations/rocket_frame_1.txt')
    ship_f2 = load_frame_from_file('./game/assets/animations/rocket_frame_2.txt')
    register_frame('ship', ship_f1)
    register_frame('ship', ship_f2)


def prepare_animations(scr) -> None:
    """Call prepare_frames and then register your animations."""
    prepare_frames()

    max_y, max_x = scr.getmaxyx()
    center_col, center_row = max_x // 2, max_y // 2
    stars = [register_animation(blink) for blink in get_random_blinks(scr, n=130)]
    bullet = register_animation(fire(
        scr, center_row - 1, center_col, rows_speed=0, columns_speed=-5))
    spaceship = register_animation(ship(scr,
                                        start_row=center_row - 1,
                                        start_column=center_col - 1,
                                        frames_name='ship'))

