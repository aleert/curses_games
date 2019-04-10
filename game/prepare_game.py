"""
Provide prepare_animation(curses_screen) callable.

That callable should register all animations you need when invoked.
"""
from engine.registry import AnimationRegistry
from engine.utils import load_frame_from_file
from game.animations import fire, get_random_blinks, ship


r = AnimationRegistry()


def prepare_animations(scr) -> None:
    max_y, max_x = scr.getmaxyx()
    center_col, center_row = max_x // 2, max_y // 2
    stars = [r.register(blink) for blink in get_random_blinks(scr, n=130)]
    bullet = r.register(fire(scr, center_row-1, center_col, rows_speed=0, columns_speed=-2))
    ship_frames = [load_frame_from_file('./game/static/animations/rocket_frame_1.txt'),
                   load_frame_from_file('./game/static/animations/rocket_frame_2.txt')]
    spaceship = r.register(ship(scr, center_row-1, center_col-1, ship_frames))
