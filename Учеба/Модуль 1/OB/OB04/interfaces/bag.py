from typing import Dict
from .items import Items


class Bag:
    def __init__(self, capacity: int):
        self._capacity = capacity
        self._items: Dict[int, Items] = {}

    @property
    def capacity(self) -> int:
        return self._capacity

    def put(self, item: Items) -> Dict[int, Items] | None:
        if len(self._items) < self.capacity:
            self._items: Dict
            self._items.update({item.id:item})
            return self._items
        return None

    def take(self, item_id: int) -> Items | None:
        self._items: Dict
        if item_id in self._items:
            return self._items.get(item_id)

        return None

    def lose_items(self) -> Dict[int, Items] | None:
        items: Dict[int, Items] = self._items.copy()
        for k, v in items.items():
            print(f"Предмет {v.__class__.__name__} выпал.")

        self._items.clear()
        return items