from aiohttp import web
from libs.algs.search import Search
from libs.classes import State,Action
from libs.classes.parser import MyParser

routes = web.RouteTableDef()


class MyStateQueue():
    def __init__(self) -> None:
        self.queue = [1,2,3,4,5,6]

    async def handle_intro(self, request):
        return web.Response(text="Hello, world")

    async def setValue(self, request):
        self.queue.append(value)

    async def getValue(self, request):
        v = self.queue.pop(0) if self.queue else None
        return web.Response(text=str(v))

def start():
    handler = MyStateQueue()
    app = web.Application()
    app.add_routes([web.get('/intro', handler.handle_intro),
                    web.get('/get', handler.getValue)])
    web.run_app(app)

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
    p = MyParser("libs/problems/problem1.yaml")
    p.parse()
    se = Search(initialState=p.getInitState(),
                actions=p.actions,
                goals=p.goal)
    solution = se.start()

if __name__ == "__main__":
    run()
