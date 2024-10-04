from contextlib import suppress
from aiohttp import web
import asyncio
from libs.classes.parser import MyParser
from libs.classes import State, Action, CostQueue
from libs.algs.distributed_algorithm import DAlgorithm
from libs.algs.heuristic import Heuristic
import os
import logging
import json
import time

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class AstarServer(DAlgorithm):
    """ AstarServer is the class that will represent the server part of the algorithm.
        Its responsabilities will be to register the states in a centralized queue, and
        serve each client a new state when asked.
        It will also have to keep track of the global queues (open and closed)
    """
    def load_functions(self):
        self.heuristic_search = Heuristic(initialState=self.initialState,
                                         actions=self.actions,
                                         goals=self.goals
                                        )
        self.app = web.Application()
        self.state_processor = web.AppKey("state_processor", asyncio.Task[None])
        self.app.add_routes([web.get('/getState', self.get_state),
                             web.post('/pushState', self.push_state),
                             web.get('/healthz', self.healthz),
                             web.get('/solution', self.get_solution),])
        logging.info("Initializing states.")
        self.queue.addElement(self.initialState)
        logging.info("Ready to receive requests")
        self.start = time.time()
        # get the loop and add a task
        self.app.cleanup_ctx.append(self.run_other_task)
        # run the code
        web.run_app(self.app)

    async def getHeuristicValue(self, state: State) -> int:
        return self.heuristic_search.getHValue(state)

    async def run_other_task(self, _app):
        self.app[self.state_processor] = asyncio.create_task(self.process_states())
        yield
        self.app[self.state_processor].cancel()
        with suppress(asyncio.CancelledError):
            await self.app[self.state_processor]  # Ensure any exceptions etc. are raised.

    async def process_states(self):
        """ This function is an additional client embedded on server to start providing states to
            the queue on the fly
        """
        # 1 First get lowest cost state from queue
        _, _, current_state = self.queue.getNextState()
        async for next_state in self.parallel_expansion(current_state):
            self.queue.addElement(next_state)
            self.addStatetoOpenList(next_state)
            # We want to keep track of each state parent:
            self.solvedStates[next_state.predicates] = current_state
            await asyncio.sleep(0.5)
        # We send the current state to the closed list, because we expanded it:
        self.addStatetoClosedList(current_state)

    async def healthz(self, request):
        """ Health endpoint for K8s
        """
        logging.debug("Endpoint is running OK")
        return "OK"

    async def get_state(self, request):
        """ This algorithm should return a state. It can be a json with the predicates
        """
        logging.info("Received request, sending state")
        # If queue is empty, end search:
        if self.queue.isEmpty():
            # Search ended, collect times:
            end = time.time()
            self.elapsed_time = end - self.start
            return web.json_response({
                "EMPTY": "True",
                "stats": self.get_stats()})
        # 1 First get lowest cost state from queue
        _, _, current_state = self.queue.getNextState()
        # TODO: how to stop when reaching a goal state
        if self.isGoalState(current_state, self.goals):
            self.app[self.state_processor].cancel()
            self.elapsed_time = time.time() - self.start
            self.goal_state = current_state
            stats = self.get_stats()
            self.resetSearch()
            return web.json_response({"GOAL": "True", "Stats": f"{stats}"})
        # We send the current state to the closed list,
        # because we suppose the client will expand it:
        self.addStatetoClosedList(current_state)
        return web.json_response(current_state.export())

    async def push_state(self, request):
        """TODO: this algorithm should add a state to the current stack.
                A state should be a json with the keys:
                predicates: frozenset=None,
                cost: int=None,
                heuristic: int=0,
                parent_action:
        """
        logging.info("Received states")
        states = await request.json()
        logging.debug("Received the following list: %s", states)
        logging.debug("Type of states: %s", type(states))
        list_states = json.loads(states)['list_states']

        for data in list_states:
            logging.debug("Received the following state: %s", data)
            s = State(predicates=frozenset(data['predicates']),
                      cost=data['cost'],
                      heuristic=data['heuristic'],
                      parent_action=data['parent_action'])
            if self.openListContains(s):
                # Verify if we have the same state with a lesser cost
                if self.getStateFromOpenList(s).cost < s.cost:
                    logging.info("State already on the open list")
                    continue
            elif self.closedListContains(s):
                # Verify if we have to reopen same state
                if self.getStateFromClosedList(s).cost < s.cost:
                    logging.info("State closed already with lesser cost")
                    continue
            else:
            # if not (self.openListContains(s) and self.getStateFromOpenList(s).cost < s.cost) \
            # and not (self.closedListContains(s) and self.getStateFromClosedList(s).cost < s.cost):
            # Verify if we have the same state with a lesser cost of if we have to reopen same state
                logging.info("Add element to queue")
                self.queue.addElement(s)
                self.addStatetoOpenList(s)
            # We want to keep track of each state parent:
            self.solvedStates[s.predicates] = s
        return web.Response(text="OK")
    
    async def get_solution(self, request):
        """ This function should return the stats of the search
        """
        expandedStates = len(self.solvedStates)
        solution = []
        pState = self.goal_state.predicates
        solution.append(self.goal_state.parent_action)
        last_action = ''
        current_action = self.goal_state.parent_action
        while pState != self.initialState.predicates and last_action != current_action:
            last_action = current_action
            current_action = self.solvedStates[pState].parent_action
            solution.append(current_action)
            logger.info(current_action)
            pState = self.solvedStates[pState].predicates
            self.solvedStates.pop(pState)
        solution_size = len(solution)
        return_dict = {
            "expanded_states": expandedStates,
            "solution": solution,
            "size": solution_size,
            "time": self.elapsed_time
        }
        return web.json_response(data=return_dict)

    def get_stats(self)->dict:
        """ This function should return the stats of the search
        """
        expandedStates = len(self.solvedStates)
        # solution = []
        # pState = self.goal_state.predicates
        # solution.append(self.goal_state.parent_action)
        # while pState != self.initialState.predicates:
        #     solution.append(self.solvedStates[pState].parent_action)
        #     pState = self.solvedStates[pState].predicates
        # solution_size = len(solution)
        solution = {
            "expanded_states": expandedStates,
            # "solution": solution,
            # "size": solution_size,
            "time": self.elapsed_time
        }
        return solution
