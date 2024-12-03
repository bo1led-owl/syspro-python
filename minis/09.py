import unittest
from dataclasses import dataclass
from typing import Any, Optional, Dict, List
from enum import Enum


@dataclass
class _Entry:
    next: Optional[Any]
    prev: Optional[Any]
    key: Any
    value: Any


@dataclass(slots=True)
class LruCache:
    __first: Optional[_Entry]
    __last: Optional[_Entry]
    __size: int
    __capacity: int

    def __init__(self, capacity: int = 16):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.__first = self.__last = None
        self.__size = 0
        self.__capacity = capacity

    # private:
    def __remove(self, entry: _Entry):
        if entry is self.__first:
            self.__first = entry.next
        if entry is self.__last:
            self.__last = entry.prev

        if entry.prev:
            entry.prev.next = entry.next
        if entry.next:
            entry.next.prev = entry.prev

    def __insertFront(self, key: Any, value: Any):
        old_first = self.__first
        self.__first = _Entry(old_first, None, key, value)
        if old_first:
            old_first.prev = self.__first
        else:
            self.__last = self.__first

    def __getEntryAndPromote(self, key: Any) -> Optional[_Entry]:
        cur = self.__first

        found = False
        while cur:
            if cur.key == key:
                found = True
                break
            cur = cur.next
        if not found:
            return None

        if cur is self.__first:
            return cur

        self.__remove(cur)
        self.__insertFront(cur.key, cur.value)
        return cur

    # public:
    @property
    def capacity(self) -> int:
        return self.capacity

    def setCapacity(self, value: int):
        if value <= 0:
            raise ValueError("Capacity must be positive")
        if value < self.__capacity:
            for _ in range(self.__capacity - value):
                self.__remove(self.__last)
            self.__size = min(self.__size, value)
        self.__capacity = value

    def get(self, key: Any) -> Optional[Any]:
        entry = self.__getEntryAndPromote(key)
        if entry is None:
            return None
        return entry.value

    def put(self, key: Any, value: Any):
        entry = self.__getEntryAndPromote(key)
        if entry:
            entry.value = value
        else:
            assert self.__size <= self.__capacity
            if self.__size < self.__capacity:
                self.__size += 1
            elif self.__size == self.__capacity:
                self.__remove(self.__last)
            self.__insertFront(key, value)


class TestSuite(unittest.TestCase):
    def testBasic(self):
        cache = LruCache()
        cache.put(1, "value")
        cache.put("key", 42)

        self.assertEqual("value", cache.get(1))
        self.assertEqual(42, cache.get("key"))
        self.assertEqual(None, cache.get("something"))

    def testKeyRemoval(self):
        cache = LruCache(capacity=4)
        cache.put(1, 1)
        cache.put(2, 2)
        cache.put(3, 3)
        cache.put(4, 4)

        self.assertEqual(4, cache.get(4))
        self.assertEqual(3, cache.get(3))
        self.assertEqual(2, cache.get(2))
        self.assertEqual(1, cache.get(1))

        cache.put(5, 5)
        self.assertEqual(1, cache.get(1))
        self.assertEqual(2, cache.get(2))
        self.assertEqual(3, cache.get(3))

        # notice that 4 gets replaced, it was used earlier than any other key
        self.assertEqual(None, cache.get(4))

        self.assertEqual(5, cache.get(5))

    def testSetCapacity(self):
        cache = LruCache(capacity=1)
        cache.put(1, 1)
        cache.put(2, 2)

        self.assertEqual(2, cache.get(2))
        self.assertEqual(None, cache.get(1))

        cache.setCapacity(4)
        cache.put(1, 1)
        cache.put(3, 3)
        cache.put(4, 4)
        self.assertEqual(1, cache.get(1))
        self.assertEqual(2, cache.get(2))
        self.assertEqual(3, cache.get(3))
        self.assertEqual(4, cache.get(4))


if __name__ == "__main__":
    unittest.main()
