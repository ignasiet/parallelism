from libs.algs.search import Search
from libs.classes import State,Action
from libs.classes.parser import MyParser
from libs.classes.mapper import Mapper
import os

import time

# class MyStateQueue():
#     def __init__(self) -> None:
#         self.queue = [1,2,3,4,5,6]

#     async def handle_intro(self, request):
#         return web.Response(text="Hello, world")

#     async def setValue(self, request):
#         self.queue.append(value)

#     async def getValue(self, request):
#         v = self.queue.pop(0) if self.queue else None
#         return web.Response(text=str(v))

# def start():
#     handler = MyStateQueue()
#     app = web.Application()
#     app.add_routes([web.get('/intro', handler.handle_intro),
#                     web.get('/get', handler.getValue)])
#     web.run_app(app)

def example():
    init = State(frozenset(['p1']),
                    cost=0,
                    heuristic=0)
    g = frozenset(['not_p1','p2'])
    action1 = Action('act_1',
                    ['p1'],
                    ['not_p1'],
                    ['p1'],
                    1)
    action2 = Action('act_2',
                    [],
                    ['p2'],
                    [],
                    1)
    se = Search(initialState=init,
                actions=[action1,action2],
                goals=g)
    solution = se.start()

def run():
    start = time.time()
    # path = os.getenv("problem")
    path = "libs/problems/boarding.yaml"
    p = MyParser(path)
    binary_rep = os.getenv("binary", 'False').lower() in ('true', '1', 't')
    print(f"Using Binary representation: {binary_rep}")

    se = Search(initialState=p.getInitState(binary_rep),
                actions=p.getActions(binary_rep),
                goals=p.getGoal(binary_rep))
    end = time.time()
    prev_time = end - start
    print(f"Time to compute and parse: {prev_time}")

    start = time.time()
    solution = se.start()
    end = time.time()
    tot_time = end - start
    print(f"Total Search time: {tot_time}")

if __name__ == "__main__":
    run()
