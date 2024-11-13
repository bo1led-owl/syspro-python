import unittest
from typing import Any, Optional
from enum import Enum


class LruCache:
    def __init__(self, capacity: int = 16):
        self.__kv = {}
        self.__held_keys = [None for _ in range(capacity)]

    # private:
    def __findKeyIndex(self, key: Any) -> int:
        assert key in self.__kv

        for i, k in enumerate(self.__held_keys):
            if k == key:
                return i

    def __promoteKey(self, key: Any):
        assert key in self.__kv

        index = self.__findKeyIndex(key)
        index = min(index, self.capacity - 1)
        self.__held_keys.pop(index)
        self.__held_keys.insert(0, key)

    def __insertKey(self, key: Any):
        assert key not in self.__kv

        self.__held_keys.pop()
        self.__held_keys.insert(0, key)

    # public:
    @property
    def capacity(self) -> int:
        return len(self.__held_keys)

    def setCapacity(self, value: int):
        if self.capacity > value:
            for key in self.__held_keys[value:]:
                self.__kv.pop(key)
            self.__held_keys = self.__held_keys[:value]
        else:
            self.__held_keys += [
                None for _ in range(value - len(self.__held_keys))
            ]

    def get(self, key: Any) -> Optional[Any]:
        result = self.__kv.get(key)
        if result is None:
            return None

        self.__promoteKey(key)
        return result

    def put(self, key: Any, value: Any):
        if key in self.__kv:
            self.__kv[key] = value
            self.__promoteKey(key)
        else:
            key_to_delete = self.__held_keys[-1]
            if key_to_delete is not None:
                self.__kv.pop(key_to_delete)
            self.__insertKey(key)
            self.__kv[key] = value


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
