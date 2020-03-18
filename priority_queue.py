from datetime import datetime, timedelta


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

time = datetime(2020, 3, 18, 18, 00)


class Passenger:
    def __init__(self, name: str, time: datetime, classs: str):
        self.name = name
        self.time = time
        self.classs = classs

    def __str__(self):
        return f'{self.late_to_flight()}, {priorities[self.classs]}, {self.name}'

    def __gt__(self, other):
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

    def late_to_flight(self, current_time=time):
        # check if to late
        if current_time > self.time:
            return False
        # check if last call
        if current_time + timedelta(minutes=15) >= self.time:
            return True
        # otherwise in good time
        return False


if __name__ == '__main__':
    from random import shuffle

    comp = lambda x, y: x > y

    time_too_late = time - timedelta(minutes=10)
    time_late = time + timedelta(minutes=10)
    time_early = time + timedelta(minutes=60)

    passenger_list = []
    for x in ['Daniel', 'Jacob', 'Nikolaj', 'Stephan']:
        passenger_list.append(Passenger(x, time_late, 'Family'))
        passenger_list.append(Passenger(x, time_early, 'Disabled'))
        passenger_list.append(Passenger(x, time_late, 'Disabled'))
        passenger_list.append(Passenger(x, time_early, 'Family'))

    shuffle(passenger_list)
    queue = PriorityQueue(comparator=comp)
    for x in passenger_list:
        queue.enqueue(x)

    for _ in range(len(passenger_list)):
        print(queue.dequeue())
