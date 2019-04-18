# Cursing games

---
## About
This is a very small game engine implemented with curses.
It is asynchrounous though doesn't use asyncio event loop,
rather implementing its own.

## Requirements

* Linux/Unix flavour with ncurses
* Python 3.5+ with curses module

## How to use

### Animation

Animations are coroutines that should recieve curses screen object
as one of the arguments and draw on them. To pass control to next animation
you should call `await asyncio.sleep(0)` between frames and `engine` will do the rest.

### Check out an example
As this is just a small study project it somewhat lacks documentation (and test, pls tell me how to test asynchronous code).
So if you learn how to work with this project you better study example game implementation
in `game` branch. From there run `python main.py` and move a starship around with arrow keys.
Note that your terminal window vertical size should be at least couple dozens of lines or you'll get an error
that engine cannot fit spaceship animation to screen.

This demo game implements different animations, load animation frames from files,
detects object overlapping (for spaceship and stars).
Fell free to change animation frames in `static`, add new animations or alter existing ones.

### Running animations
To run your animations you should create ***game*** module that should have prepare_game.py file 
implementing `prepare_game(stdscr)` function that is responsible for
registering all of your animations.

Your helpers will be:
 
 * `engine.decorators.delay_animation_frame_in_coros(delay)`,
that will allow you to specify delay in second for every `await asyncio.sleep(0)`
call in you animation (and you cant specify other timeout than 0 for `asyncio.sleep` because,
well, no asyncio compatible event loop is used).

* `engine.registry.register_animation` class to register you animations in game.


* `engine.utils.draw_frames` to draw miltiline string with curses

and other helpful functions from `engine.utils`. It's quite tiny so check it out!

To regitster you animation do the following in `game.prepare_game`:
```python
from engine.registry import register_animation


def prepare_animations(scr):
    animations = list(generate_animations(scr=scr, n=50))
    [register_animation(animation) for animation in animations]
```

And after that just run `python main.py` and enjoy.


