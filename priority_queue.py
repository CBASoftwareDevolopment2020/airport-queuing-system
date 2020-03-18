from datetime import datetime


class PriorityQueue(object):
    def __init__(self, comparator: callable):
        self.items = []
        self.size = 0
        self.comparator = comparator

    def __str__(self):
        return ' '.join([str(i) for i in self.items])

    def is_empty(self):
        return len(self.items) == 0

    def heapify(self):
        for i in range(self.size, -1, -1):
            self._heapify(self.items, self.size, i, comparator=self.comparator)

    def enqueue(self, item: object):
        self.items.append(item)
        self.size += 1

        self.heapify()

    def dequeue(self) -> object:
        item = self.items.pop(0)
        self.size -= 1

        self.heapify()

        return item

    def _heapify(self, data: list, n: int, i: int, comparator: callable):
        prioritised = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and comparator(data[left], data[prioritised]):
            prioritised = left
        if right < n and comparator(data[right], data[prioritised]):
            prioritised = right

        if prioritised != i:
            data[i], data[prioritised] = data[prioritised], data[i]
            self._heapify(data, n, prioritised, comparator)


priorities = {
    'Disabled': 0,
    'Business class': 1,
    'Family': 2,
    'Monkey': 3,
}


class Passenger:
    def __init__(self, name: str, time: datetime, classs: str):
        self.name = name
        self.time = time
        self.classs = classs

    def __cmp__(self, other):
        # check if same type
        if type(other) is not type(self):
            return True
        # check self late and other not late
        if self.late_to_flight() and not other.late_to_flight():
            return True
        # check self not late and other late
        elif not self.late_to_flight() and other.late_to_flight():
            return False
        else:
            # check if classs is prioritised for both
            if self.classs in priorities and other.classs in priorities:
                return priorities[self.classs] <= priorities[other.classs]
            # check if classs is not prioritised for both
            elif self.classs not in priorities and other.classs not in priorities:
                return True
            # self bias
            return self.classs in priorities

    def late_to_flight(self, current_time: datetime = datetime.now()):
        # check if to late
        if current_time > self.time:
            return False
        # check if last call
        if (self.time - current_time).seconds * 60 < 15:
            return True
        # otherwise in good time
        return False


comp = lambda x, y: x > y
