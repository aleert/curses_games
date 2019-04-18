"""Registries that keep all global items such as animations."""
from collections import deque
from typing import Coroutine, Deque

_registry = deque()


def register_animation(new_animation: Coroutine):
    """Add new animation to registry."""
    _registry.append(new_animation)
    return new_animation


def get_registered_animations() -> Deque[Coroutine]:
    """Return deque with all animations."""
    return _registry

