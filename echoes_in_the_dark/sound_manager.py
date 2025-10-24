"""Sound manager placeholder."""
from __future__ import annotations

from typing import Dict

import pygame


class SoundManager:
    """Handles loading and playing ambient and effect sounds."""

    def __init__(self) -> None:
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.ambient_channel = None

    def load_sound(self, key: str, path: str) -> None:
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.sounds[key] = pygame.mixer.Sound(path)

    def play_sound(self, key: str) -> None:
        sound = self.sounds.get(key)
        if sound:
            sound.play()

    def play_ambient_loop(self, key: str, volume: float = 0.5) -> None:
        sound = self.sounds.get(key)
        if sound:
            if self.ambient_channel is None:
                self.ambient_channel = pygame.mixer.Channel(0)
            self.ambient_channel.play(sound, loops=-1)
            self.ambient_channel.set_volume(volume)

    def stop_ambient(self) -> None:
        if self.ambient_channel:
            self.ambient_channel.stop()
