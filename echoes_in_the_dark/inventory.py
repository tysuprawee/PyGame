"""Inventory module placeholder."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Inventory:
    """Tracks player items such as keys and consumables."""

    items: Dict[str, int] = field(default_factory=dict)

    def add_item(self, name: str, count: int = 1) -> None:
        self.items[name] = self.items.get(name, 0) + count

    def remove_item(self, name: str, count: int = 1) -> None:
        if name in self.items:
            self.items[name] -= count
            if self.items[name] <= 0:
                del self.items[name]

    def has_item(self, name: str) -> bool:
        return name in self.items
