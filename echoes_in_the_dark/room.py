"""Room module for Echoes in the Dark."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

import pygame


@dataclass
class Room:
    """Represents a tiled room loaded from JSON."""

    map_path: Path
    tile_size: int = field(init=False)
    width: int = field(init=False)
    height: int = field(init=False)
    tiles: List[List[int]] = field(init=False)
    wall_color: pygame.Color = pygame.Color(40, 40, 40)
    floor_color: pygame.Color = pygame.Color(70, 70, 70)
    background_surface: pygame.Surface = field(init=False)
    colliders: List[pygame.Rect] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self._load_map()
        self._build_surfaces()

    def _load_map(self) -> None:
        with open(self.map_path, "r", encoding="utf8") as map_file:
            data = json.load(map_file)
        self.tile_size = data["tile_size"]
        self.width = data["width"]
        self.height = data["height"]
        self.tiles = data["tiles"]

    def _build_surfaces(self) -> None:
        self.background_surface = pygame.Surface((self.width * self.tile_size, self.height * self.tile_size))
        self.background_surface.fill(self.floor_color)
        self.colliders.clear()

        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
                if tile == 1:
                    pygame.draw.rect(self.background_surface, self.wall_color, rect)
                    self.colliders.append(rect)
                else:
                    pygame.draw.rect(self.background_surface, self.floor_color, rect)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.background_surface, (0, 0))
