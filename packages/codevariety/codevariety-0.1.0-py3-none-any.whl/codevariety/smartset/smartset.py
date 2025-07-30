

class SmartSet:
    def __init__(self, iterable=None, sorted=False):
        self._data = set(iterable if iterable else [])
        self._sorted_cache = None
        self._is_sorted = sorted

    def __contains__(self, item):
        return item in self._data

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        return iter(self._sorted_cache if self._is_sorted else self._data)

    def __str__(self):
        if self._is_sorted:
            return f'{self._sorted_cache}'
        return f'{list(self._data)}'

    def __sub__(self, other):
        return SmartSet(self._difference_core(other))

    def __add__(self, other):
        return self.__or__(other)

    def __or__(self, other):
        return SmartSet(self._union_core(other))

    def __and__(self, other):
        return SmartSet(self._intersection_core(other))

    def __xor__(self, other):
        return SmartSet(self._symmetric_difference_core(other))

    def __iadd__(self, other):
        return self.__ior__(other)

    def __ior__(self, other):
        self._data |= self._coerce_set(other)
        self._invalidate()
        return self

    def __isub__(self, other):
        self._data -= self._coerce_set(other)
        self._invalidate()
        return self

    def __iand__(self, other):
        self._data &= self._coerce_set(other)
        self._invalidate()
        return self

    def __ixor__(self, other):
        self._data ^= self._coerce_set(other)
        self._invalidate()
        return self

    def __eq__(self, other):
        return self._equals_core(other)

    def __ne__(self, other):
        return not self._equals_core(other)

    def __repr__(self):
        data = self._sorted_cache if self._is_sorted else list(self._data)
        return f'{SmartSet.__name__}({data}, sorted={self._is_sorted})'

    def union(self, other):
        return SmartSet(self._union_core(other))

    def copy(self):
        return SmartSet(self._data.copy())

    def clear(self):
        self._data.clear()
        self._invalidate()
        return self

    def pop(self):
        if not self._data:
            raise KeyError('Cannot pop from an empty set.')
        if self._is_sorted:
            top_value = self._sorted_cache[0]
            self._data.remove(top_value)
            self._invalidate()
            return top_value
        return self._data.pop()

    def add(self, item):
        if item not in self._data:
            self._data.add(item)
            self._invalidate()
        return self

    def remove(self, item):
        self._data.remove(item)
        self._invalidate()
        return self

    def discard(self, item):
        self._data.discard(item)
        self._invalidate()
        return self

    def update(self, other):
        self._data |= self._coerce_set(other)
        self._invalidate()
        return self

    def sort(self):
        self._sorted_cache = sorted(self._data)
        self._is_sorted = True
        return self

    def unsort(self):
        self._invalidate()
        return self

    def difference(self, other):
        return self.__sub__(other)

    def symmetric_difference(self, other):
        return self.__xor__(other)

    def intersection(self, other):
        return self.__and__(other)

    def issubset(self, other):
        return self._data.issubset(self._coerce_set(other))

    def issuperset(self, other):
        return self._data.issuperset(self._coerce_set(other))

    def isdisjoint(self, other):
        return self._data.isdisjoint(self._coerce_set(other))

    def includes(self, other):
        return self.issuperset(other)

    def scale(self, number):
        number = self._check_numeric(number)

        self._data = set(x * number for x in self._data)
        self._invalidate()
        return self

    def scaled(self, number):
        number = self._check_numeric(number)

        return SmartSet(x * number for x in self._data)

    def mean(self):
        self._check_numeric()
        return sum(self._data) / len(self._data)

    def min(self):
        self._check_numeric()
        return min(self._data)

    def max(self):
        self._check_numeric()
        return max(self._data)

    def sum(self):
        self._check_numeric()
        return sum(self._data)

    def normalize(self):
        if not self._data:
            raise KeyError('Cannot normalize an empty set.')
        self._check_numeric()

        norm = sum(x ** 2 for x in self._data) ** 0.5
        if norm == 0:
            raise ValueError('Cannot normalize a set with a zero magnitude.')

        self._data = set(x / norm for x in self._data)
        self._invalidate()
        return self

    def _invalidate(self):
        if self._is_sorted:
            self._sorted_cache = None
            self._is_sorted = False

    def _coerce_set(self, other):
        if isinstance(other, SmartSet):
            return other._data
        return set(other)

    def _difference_core(self, other):
        return self._data - self._coerce_set(other)

    def _intersection_core(self, other):
        return self._data & self._coerce_set(other)

    def _union_core(self, other):
        return self._data | self._coerce_set(other)

    def _equals_core(self, other):
        try:
            return self._data == self._coerce_set(other)
        except TypeError:
            return False

    def _symmetric_difference_core(self, other):
        return self._data ^ self._coerce_set(other)

    def _check_numeric(self, number=None):
        if number is not None:
            try:
                number = float(number)
            except ValueError:
                raise ValueError('Scalar must be an integer or float.')
        if not all(isinstance(x, (int, float)) for x in self._data):
            raise ValueError('SmartSet must contain only numbers for this operation.')
        return number



