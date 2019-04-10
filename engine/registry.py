"""Registries that keep all global items such as animations."""
from typing import Coroutine


class AnimationRegistry:
    """Class that allow to register animations to global registry and retrieve them."""

    _registry = []

    @property
    def registered(self):
        """Return copy of all registered animations."""
        return list(self._registry)

    @classmethod
    def register(cls, new_animation: Coroutine):
        """Add new animation to registry."""
        cls._registry.append(new_animation)
        return new_animation

