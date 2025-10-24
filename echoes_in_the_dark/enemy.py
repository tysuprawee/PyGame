"""Enemy module for Echoes in the Dark."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

import pygame


@dataclass
class Enemy:
    """Base enemy with placeholder patrol/chase logic."""

    position: pygame.math.Vector2
    patrol_points: List[pygame.math.Vector2]
    speed: float = 80.0
    chase_speed: float = 120.0
    detection_radius: float = 120.0
    size: Tuple[int, int] = (24, 24)
    color: Tuple[int, int, int] = (200, 60, 60)
    _target_index: int = 0
    _state: str = field(default="patrol", init=False)

    def __post_init__(self) -> None:
        self.rect = pygame.Rect(self.position.x, self.position.y, *self.size)

    def update(self, dt: float, player_pos: pygame.math.Vector2, colliders: List[pygame.Rect]) -> None:
        distance_to_player = player_pos.distance_to(self.position)
        if distance_to_player <= self.detection_radius:
            self._state = "chase"
            target = player_pos
            speed = self.chase_speed
        else:
            self._state = "patrol"
            target = self.patrol_points[self._target_index]
            speed = self.speed
            if self.position.distance_to(target) < 4:
                self._target_index = (self._target_index + 1) % len(self.patrol_points)
                target = self.patrol_points[self._target_index]

        direction = (target - self.position)
        if direction.length_squared() > 0:
            direction = direction.normalize()
        movement = direction * speed * dt
        self._move(movement, colliders)
        self.rect.topleft = self.position.xy

    def _move(self, movement: pygame.math.Vector2, colliders: List[pygame.Rect]) -> None:
        self.position.x += movement.x
        self.rect.x = int(self.position.x)
        for collider in colliders:
            if self.rect.colliderect(collider):
                if movement.x > 0:
                    self.rect.right = collider.left
                elif movement.x < 0:
                    self.rect.left = collider.right
                self.position.x = self.rect.x
        self.position.y += movement.y
        self.rect.y = int(self.position.y)
        for collider in colliders:
            if self.rect.colliderect(collider):
                if movement.y > 0:
                    self.rect.bottom = collider.top
                elif movement.y < 0:
                    self.rect.top = collider.bottom
                self.position.y = self.rect.y

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
