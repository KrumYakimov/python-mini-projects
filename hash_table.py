from typing import List, Optional, NamedTuple, Any, Union


class Pair(NamedTuple):
    key: Any
    value: Any


class Deleted:
    pass


class HashTable:
    DELETED = Deleted()

    def __init__(self, capacity: int = 4):
        self.capacity = capacity
        self._array: List[Optional[Union[Pair, Deleted]]] = [None] * self.capacity

    @property
    def capacity(self):
        return self.__capacity

    @capacity.setter
    def capacity(self, value):
        if value < 1:
            raise ValueError("Capacity must be positive")
        self.__capacity = value

    @property
    def array(self):
        return {pair for pair in self._array if pair not in (None, self.DELETED)}

    @property
    def keys(self):
        return {pair.key for pair in self.array}

    @property
    def values(self):
        return {pair.value for pair in self.array}

    def hash(self, key) -> int:
        # return sum(ord(char) for char in key) % self.capacity
        return hash(key) % self.capacity

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def _linear_probing(self, key):
        idx = self.hash(key)

        for _ in range(self.capacity):
            yield idx, self._array[idx]
            idx = (idx + 1) % self.capacity

    def _resize(self):
        copy = HashTable(capacity=self.capacity * 2)

        for key, value in self.array:
            copy[key] = value

        self.capacity = copy.capacity
        self._array = copy._array

    def __setitem__(self, key, value):
        for idx, pair in self._linear_probing(key):
            if pair is self.DELETED:
                continue

            if pair is None or pair.key == key:
                self._array[idx] = Pair(key, value)
                break
        else:
            self._resize()
            self[key] = value

    def __getitem__(self, key):
        for _, pair in self._linear_probing(key):
            if pair is self.DELETED:
                continue

            if pair is None:
                raise KeyError(key)

            if pair.key == key:
                return pair.value
        else:
            KeyError(key)

    def __delitem__(self, key):
        for idx, pair in self._linear_probing(key):
            if pair is self.DELETED:
                continue

            if pair is None:
                raise KeyError(key)

            if pair.key == key:
                self._array[idx] = self.DELETED
                break
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
        except KeyError:
            raise False
        else:
            return True

    def __iter__(self):
        yield from self.keys

    def __len__(self):
        return len(self.array)

    def __str__(self):
        pairs = []
        for key, value in self.array:
            pairs.append(f"{key!r}: {value!r}")

        return "{" + ", ".join(pairs) + "}"


table = HashTable()

table["Name"] = "George"
table["Age"] = 27
table["City"] = "Sofia"
table["Occupation"] = "Data Scientist"
table["Education"] = "Mathematics"
table["Courses"] = "Python"
table["Languages"] = "Bulgarian"
table["Interest"] = "Mountain Biking"


print(table)
print(table.get("Name"))
print(table["Age"])
print(len(table))
print("Age" in table)

