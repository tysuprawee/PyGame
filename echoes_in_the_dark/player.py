"""Player module for Echoes in the Dark."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple

import pygame


@dataclass
class Player:
    """Represents the player character and handles movement and the flashlight."""

    position: pygame.math.Vector2
    speed: float = 150.0
    size: Tuple[int, int] = (24, 24)
    color: Tuple[int, int, int] = (200, 200, 200)
    flashlight_length: float = 140.0
    flashlight_width: float = 90.0
    flashlight_falloff: int = 210
    direction: pygame.math.Vector2 = field(default_factory=lambda: pygame.math.Vector2(1, 0))

    def __post_init__(self) -> None:
        self.rect = pygame.Rect(self.position.x, self.position.y, *self.size)

    def handle_input(self) -> pygame.math.Vector2:
        keys = pygame.key.get_pressed()
        move = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1
        if move.length_squared() > 0:
            move = move.normalize()
            self.direction = move
        return move

    def update(self, dt: float, colliders: list[pygame.Rect]) -> None:
        velocity = self.handle_input() * self.speed * dt
        self._move_axis(velocity.x, 0, colliders)
        self._move_axis(0, velocity.y, colliders)
        self.rect.topleft = self.position.xy

    def _move_axis(self, dx: float, dy: float, colliders: list[pygame.Rect]) -> None:
        if dx:
            self.position.x += dx
            self.rect.x = int(self.position.x)
            for collider in colliders:
                if self.rect.colliderect(collider):
                    if dx > 0:
                        self.rect.right = collider.left
                    elif dx < 0:
                        self.rect.left = collider.right
                    self.position.x = self.rect.x
        if dy:
            self.position.y += dy
            self.rect.y = int(self.position.y)
            for collider in colliders:
                if self.rect.colliderect(collider):
                    if dy > 0:
                        self.rect.bottom = collider.top
                    elif dy < 0:
                        self.rect.top = collider.bottom
                    self.position.y = self.rect.y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)

    def draw_flashlight(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.flashlight_falloff))

        center = pygame.math.Vector2(self.rect.center)
        forward = self.direction.normalize() if self.direction.length_squared() else pygame.math.Vector2(1, 0)
        perpendicular = pygame.math.Vector2(-forward.y, forward.x)

        tip = center + forward * self.flashlight_length
        left = center + forward * (self.flashlight_length * 0.6) + perpendicular * (self.flashlight_width / 2)
        right = center + forward * (self.flashlight_length * 0.6) - perpendicular * (self.flashlight_width / 2)

        pygame.draw.polygon(overlay, (0, 0, 0, 0), [center, left, tip, right])
        surface.blit(overlay, (0, 0))
