from libs.classes.state import State
from queue import PriorityQueue
import time


class CostQueue():
    def __init__(self) -> None:
        self.queue = PriorityQueue()

    # We use time as second parameter
    def addElement(self, element: State)->None:
        self.queue.put((element.cost+element.heuristic, time.time(), element))

    def getNextState(self)->State:
        try:
            return self.queue.get()
        except TypeError:
            print(f"Size: {self.queue.qsize()}")
            raise

    def isEmpty(self)->bool:
        return self.queue.empty()

    def __len__(self):
        return self.queue.qsize()
