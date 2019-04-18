"""Registries that keep all global items such as animations and frames."""
from collections import deque, defaultdict
from typing import Coroutine, Deque, List

_registry = deque()


_animation_frame_registry = defaultdict(list)


def register_animation(new_animation: Coroutine):
    """Add new animation to registry."""
    _registry.append(new_animation)
    return new_animation


def get_registered_animations() -> Deque[Coroutine]:
    """Return deque with all animations."""
    return _registry


def register_frame(name: str, frame: str) -> None:
    """Register multiline frame that perhaps is loaded from file."""
    _animation_frame_registry[name].append(frame)


def get_frames(name: str) -> List[str]:
    """Get all frames registered for given `name`."""
    return list(_animation_frame_registry[name])

