"""Entry point and main game loop for Echoes in the Dark."""
from __future__ import annotations

from pathlib import Path
from typing import List

import pygame

from enemy import Enemy
from player import Player
from room import Room


class Game:
    """Manages the core game loop, state, and scene transitions."""

    def __init__(self) -> None:
        pygame.init()
        self._load_room()
        self.screen = pygame.display.set_mode((self.room.width * self.room.tile_size, self.room.height * self.room.tile_size))
        pygame.display.set_caption("Echoes in the Dark")
        self.clock = pygame.time.Clock()
        self.running = True

        start_position = pygame.math.Vector2(self.room.tile_size * 2, self.room.tile_size * 2)
        self.player = Player(start_position)
        enemy_start = pygame.math.Vector2(self.room.tile_size * (self.room.width - 4), self.room.tile_size * (self.room.height - 4))
        patrol_points = [enemy_start, pygame.math.Vector2(self.room.tile_size * (self.room.width - 6), enemy_start.y)]
        self.enemies: List[Enemy] = [Enemy(enemy_start, patrol_points)]

    def _load_room(self) -> None:
        data_path = Path(__file__).resolve().parent / "data" / "map1.json"
        self.room = Room(data_path)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self._handle_events()
            self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, dt: float) -> None:
        self.player.update(dt, self.room.colliders)
        for enemy in self.enemies:
            enemy.update(dt, pygame.math.Vector2(self.player.rect.center), self.room.colliders)

    def _draw(self) -> None:
        self.room.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        self.player.draw(self.screen)
        self.player.draw_flashlight(self.screen)
        pygame.display.flip()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
