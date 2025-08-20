from typing import Any


class Dictionary:

    def __init__(self, capacity: int = 8) -> None:
        self.capacity = capacity
        self.data = [[] for _ in range(capacity)]
        self.size = 0

    def __setitem__(self, key: Any, value: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value, _hash)
                return

        bucket.append((key, value, _hash))
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if k == key:
                return v

        raise KeyError(f"Key {key} not found")

    def __len__(self) -> int:
        return self.size

    def _resize(self) -> None:
        new_capacity = self.capacity * 2
        new_data = [[] for _ in range(new_capacity)]

        for bucket in self.data:
            for key, value, _hash in bucket:
                new_index = _hash % new_capacity
                new_data[new_index].append((key, value, _hash))

        self.capacity = new_capacity
        self.data = new_data

    def clear(self) -> None:
        self.data = [[] for _ in range(self.capacity)]
        self.size = 0

    def __delitem__(self, key: Any) -> None:
        _hash = hash(key)
        index = _hash % self.capacity
        bucket = self.data[index]

        for i, (k, v, h) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError(key)

    def update(
            self,
            other: dict | list[tuple] | None = None,
            **kwargs
    ) -> None:
        if other is not None:
            if isinstance(other, dict):
                items = other.items()
            else:
                items = other
            for key, value in items:
                self[key] = value

        for key, value in kwargs.items():
            self[key] = value
