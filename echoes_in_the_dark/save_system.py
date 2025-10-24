"""Save system placeholder."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict


@dataclass
class SaveSystem:
    """Handles saving and loading JSON game state."""

    path: Path

    def save(self, data: Dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", encoding="utf8") as save_file:
            json.dump(data, save_file, indent=4)

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {}
        with open(self.path, "r", encoding="utf8") as save_file:
            return json.load(save_file)
