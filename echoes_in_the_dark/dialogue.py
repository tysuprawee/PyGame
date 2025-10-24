"""Dialogue management placeholder."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class DialogueNode:
    text: str
    choices: Dict[str, str] = field(default_factory=dict)


class DialogueManager:
    """Handles loading and presenting dialogue trees (placeholder implementation)."""

    def __init__(self) -> None:
        self.dialogues: Dict[str, DialogueNode] = {}

    def load_from_dict(self, data: Dict[str, Dict[str, List[str]]]) -> None:
        self.dialogues = {key: DialogueNode(text=value.get("text", ""), choices=value.get("choices", {})) for key, value in data.items()}

    def get_dialogue(self, key: str) -> DialogueNode | None:
        return self.dialogues.get(key)
