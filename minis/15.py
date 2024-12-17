from typing import Any, List
from dataclasses import dataclass
import sys
import copy
import threading


@dataclass
class TaskQueue:
    __queue: List[Any]
    __lock: threading.Lock
    __cond: threading.Condition
    __done: bool

    def __init__(self):
        self.__queue = []
        self.__lock = threading.Lock()
        self.__cond = threading.Condition(self.__lock)
        self.__done = False

    def isDone(self) -> bool:
        assert self.__lock.locked()
        return self.__done

    def isEmpty(self) -> bool:
        assert self.__lock.locked()
        return len(self.__queue) == 0

    def markDone(self):
        with self.__lock:
            self.__done = True

    def push(self, task: Any):
        with self.__lock:
            self.__queue.append(task)
            self.__cond.notify()

    def pop(self) -> Any:
        with self.__lock:
            if self.isEmpty():
                self.__cond.wait_for(
                    lambda: self.isDone() or not self.isEmpty()
                )
            try:
                return self.__queue.pop()
            except IndexError:
                return None


queue = TaskQueue()


def produce(max_size: int, value: int, max_power: int):
    for size in range(1, max_size + 1):
        for p in range(1, max_power):
            queue.push((size, value, p))
    queue.markDone()


def consume(results, index):
    res = 0
    while True:
        v = queue.pop()
        if v is None:
            break
        n, v, p = v
        matrix = [[] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                matrix[i].append(v ** (i + j))
        if p == 1:
            res += sum(map(sum, matrix))
            continue

        mat_copy = copy.deepcopy(matrix)
        for _ in range(p - 1):
            buf = [[0 for _ in range(n)] for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        buf[i][j] += matrix[i][k] * mat_copy[k][j]
            matrix, buf = buf, matrix
        res += sum(map(sum, matrix))
    results[index] = res


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Expected consumer count as the first argument")
        exit(2)
    CONSUMERS = int(sys.argv[1])
    producer = threading.Thread(target=produce, args=[20, 2, 50])
    results = [0 for _ in range(CONSUMERS)]
    consumers = [
        threading.Thread(target=consume, args=[results, i])
        for i in range(CONSUMERS)
    ]
    producer.start()
    for cons in consumers:
        cons.start()

    producer.join()
    for cons in consumers:
        cons.join()
    print(sum(results))
