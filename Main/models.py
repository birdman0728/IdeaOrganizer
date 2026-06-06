"""Document and Tag models for the map app.

Provides `Document` (a simple text item with tags) and a minimal `Tag` holder.
"""
from __future__ import annotations
import uuid
from typing import Set, Optional


class Document:
    """Represents a text document that can carry multiple tag names.

    Attributes:
        id: stable identifier (UUID string)
        title: short title
        content: text content
        tags: set of tag names (strings)
    """

    def __init__(self, title: str, content: str = "", id: Optional[str] = None) -> None:
        self.id: str = id or str(uuid.uuid4())
        self.title: str = title
        self.content: str = content
        self.tags: Set[str] = set()

    def add_tag(self, tag_name: str) -> None:
        self.tags.add(tag_name)

    def remove_tag(self, tag_name: str) -> None:
        self.tags.discard(tag_name)

    def edit(self, title: Optional[str] = None, content: Optional[str] = None) -> None:
        if title is not None:
            self.title = title
        if content is not None:
            self.content = content

    def as_dict(self) -> dict:
        return {"id": self.id, "title": self.title, "content": self.content, "tags": list(self.tags)}

    def __repr__(self) -> str:
        return f"Document(id={self.id!r}, title={self.title!r}, tags={sorted(self.tags)})"


class Tag:
    """Lightweight Tag holder. Tags are identified by name."""

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Tag({self.name!r})"
