"""MapManager: manage named maps (collections) of `Document` items and tags.

Features:
- Create / delete maps
- Rename maps (by creating a new map and transferring items)
- Add, remove, move documents between maps
- Create, rename, delete tags and attach tags to documents
"""
from typing import Dict, List, Optional
from models import Document, Tag


class MapManager:
    def __init__(self) -> None:
        # map title -> list of document ids (order-preserving)
        self.maps: Dict[str, List[str]] = {}
        # document id -> Document
        self.documents: Dict[str, Document] = {}
        # tag name set
        self.tags: Dict[str, Tag] = {}

    # Map operations
    def create_map(self, title: str) -> None:
        if title in self.maps:
            raise ValueError(f"Map {title!r} already exists")
        self.maps[title] = []

    def delete_map(self, title: str, delete_documents: bool = False) -> None:
        if title not in self.maps:
            raise KeyError(title)
        doc_ids = self.maps.pop(title)
        if delete_documents:
            for did in doc_ids:
                self.documents.pop(did, None)

    def rename_map(self, old_title: str, new_title: str) -> None:
        """Rename a map by creating a new map and transferring items over."""
        if old_title not in self.maps:
            raise KeyError(old_title)
        if new_title in self.maps:
            raise ValueError(f"Map {new_title!r} already exists")
        # transfer
        self.maps[new_title] = list(self.maps[old_title])
        del self.maps[old_title]

    def list_maps(self) -> List[str]:
        return list(self.maps.keys())

    # Document operations
    def add_document(self, map_title: str, title: str, content: str = "") -> Document:
        if map_title not in self.maps:
            raise KeyError(map_title)
        doc = Document(title=title, content=content)
        self.documents[doc.id] = doc
        self.maps[map_title].append(doc.id)
        return doc

    def add_existing_document_to_map(self, doc_id: str, map_title: str) -> None:
        if doc_id not in self.documents:
            raise KeyError(doc_id)
        if map_title not in self.maps:
            raise KeyError(map_title)
        if doc_id in self.maps[map_title]:
            return
        self.maps[map_title].append(doc_id)

    def remove_document_from_map(self, map_title: str, doc_id: str, delete_document: bool = False) -> None:
        if map_title not in self.maps:
            raise KeyError(map_title)
        try:
            self.maps[map_title].remove(doc_id)
        except ValueError:
            raise KeyError(doc_id)
        if delete_document:
            self.documents.pop(doc_id, None)

    def move_document(self, doc_id: str, from_map: str, to_map: str) -> None:
        self.remove_document_from_map(from_map, doc_id, delete_document=False)
        self.add_existing_document_to_map(doc_id, to_map)

    def edit_document(self, doc_id: str, title: Optional[str] = None, content: Optional[str] = None) -> None:
        if doc_id not in self.documents:
            raise KeyError(doc_id)
        self.documents[doc_id].edit(title=title, content=content)

    def get_documents_in_map(self, map_title: str) -> List[Document]:
        if map_title not in self.maps:
            raise KeyError(map_title)
        return [self.documents[d] for d in self.maps[map_title] if d in self.documents]

    def get_document(self, doc_id: str) -> Document:
        return self.documents[doc_id]

    # Tag operations
    def create_tag(self, name: str) -> None:
        if name in self.tags:
            return
        self.tags[name] = Tag(name)

    def delete_tag(self, name: str) -> None:
        if name in self.tags:
            del self.tags[name]
        # remove tag from all documents
        for doc in self.documents.values():
            doc.remove_tag(name)

    def rename_tag(self, old_name: str, new_name: str) -> None:
        if old_name not in self.tags:
            raise KeyError(old_name)
        if new_name in self.tags:
            raise ValueError(new_name)
        self.tags[new_name] = Tag(new_name)
        del self.tags[old_name]
        for doc in self.documents.values():
            if old_name in doc.tags:
                doc.remove_tag(old_name)
                doc.add_tag(new_name)

    def add_tag_to_document(self, doc_id: str, tag_name: str) -> None:
        if doc_id not in self.documents:
            raise KeyError(doc_id)
        if tag_name not in self.tags:
            self.create_tag(tag_name)
        self.documents[doc_id].add_tag(tag_name)

    def remove_tag_from_document(self, doc_id: str, tag_name: str) -> None:
        if doc_id not in self.documents:
            raise KeyError(doc_id)
        self.documents[doc_id].remove_tag(tag_name)

    # Utility
    def as_dict(self) -> Dict[str, List[dict]]:
        return {m: [self.documents[d].as_dict() for d in docs if d in self.documents] for m, docs in self.maps.items()}
