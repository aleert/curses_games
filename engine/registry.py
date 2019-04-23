# -*- coding: utf-8 -*-

"""Registries that keep all global items such as animations and frames."""
from collections import defaultdict
from typing import Coroutine, List

try:
    from game.prepare_game import FRAME_RATE  # noqa: Z435
except ImportError:
    FRAME_RATE = 30

animation_registry: List[Coroutine] = []


_animation_frame_registry = defaultdict(list)


def register_frame(name: str, frame: str) -> None:
    """Register multiline frame that perhaps is loaded from file."""
    _animation_frame_registry[name].append(frame)


def get_frames(name: str) -> List[str]:
    """Get all frames registered for given `name`."""
    return list(_animation_frame_registry[name])
