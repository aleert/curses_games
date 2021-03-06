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
 
 * `engine.utils.delay(delay_seconds)`,
that will allow you to specify delay in seconds inside your animations.

* `engine.utils.draw_frames` to draw miltiline string with curses

and other helpful functions from `engine.utils`. It's quite tiny so check it out!


To load your animation frames from external file and register them do following:
```python
from engine.registry import register_frame
from engine.utils import load_frame_from_file

fr1 = load_frame_from_file('path/to/frame1.txt')
fr2 = load_frame_from_file('path/to/frame2.txt')
register_frame('ship_frames', fr1)
register_frame('ship_frames', fr2)
```
You can access your frames later:
```python
from engine.registry import get_frames

fr1, fr2 = get_frames('ship_frames')
```

To regitster you animation do the following in `game.prepare_game`:
```python
from engine.registry import animation_registry


def prepare_animations(scr):
    animations = list(generate_animations(scr=scr, n=50))
    [animation_registry.append(animation) for animation in animations]
```

And after that just run `python main.py` and enjoy.

### Controlling frame rate.

You can specify screen update frequency by setting `FRAME_RATE` in `game.prepare_game`:
```python
FRAME_RATE: float = 15
```
If not specified, `FRAME_RATE` defaults to 30.
