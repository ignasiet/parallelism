from aiohttp import ClientSession, web
import aiohttp
import asyncio
import json
from libs.classes import State
from libs.algs.distributed_algorithm import DAlgorithm
from libs.algs.heuristic import Heuristic

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

class AstarClient(DAlgorithm):
    """ AstarClient is the class that will represent the client part of the algorithm.
        Its responsabilities will be to get new states and expand them, and calculate the heuristics
    """
    def load_functions(self)->None:
        # In order to create the different time waits, we add the following:
        self.timestop_1 = False
        self.timestop_2 = False
        self.heuristic_search = Heuristic(initialState=self.initialState,
                                         actions=self.actions,
                                         goals=self.goals
                                        )


    def getHeuristicValue(self, state: State) -> int:
        return self.heuristic_search.getHValue(state)

    async def start(self, base_server_url: str):
        finished = False
        logging.info("Starting requesting to %s", base_server_url)
        while not finished:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_server_url + "/getState") as resp:
                    data = await resp.json()
                    logging.info("Received state: %s", data)
                    if "GOAL" in data:
                        finished = True
                        continue
                    if "EMPTY" in data:
                        if not self.timestop_1:
                            logging.info("First stop")
                            self.timestop_1 = True
                            await asyncio.sleep(5)
                            continue
                        elif not self.timestop_2:
                            logging.info("Second stop")
                            self.timestop_2 = True
                            await asyncio.sleep(10)
                            continue
                        else:
                            finished = True
                        self.timestop_1 = False
                        self.timestop_2 = False
                        continue
                    states = await self.process(data)
                    await self.send_states(states,
                                           base_server_url,
                                           session)

    async def process(self, data: dict):
        current_state = State(predicates=frozenset(data['predicates']),
                              cost=data['cost'],
                              heuristic=data['heuristic'],
                              parent_action=data['parent_action'])
        # 3 Generate its succesors
        # Each successor has cost = parent_cost + action_cost
        states = []
        for action in self.actions:
            # Verify if action is applicable, else continue:
            if not current_state.isApplicable(action):
                continue
            logging.debug(f"Applying action: {action.name}")
            next_state = self.expandState(current_state,
                                          action)
            if current_state.cost == float("inf"):
                next_state.cost = action.cost
            else:
                next_state.cost = current_state.cost + action.cost

            if self.openListContains(next_state):
                # Verify if we have the same state with a lesser cost
                if self.getStateFromOpenList(next_state).cost < next_state.cost:
                    logging.debug(f"State already on list with lower cost")
                    continue
            elif self.closedListContains(next_state):
                # Verify if we have to reopen same state
                if self.getStateFromClosedList(next_state).cost < next_state.cost:
                    logging.debug(f"Found state already expanded with lower cost")
                    continue
            else:
                # Obtain heuristic value for nextState
                logging.debug("Computing heuristic")
                next_state.heuristic = self.getHeuristicValue(next_state)
                logging.debug(f"Heuristic value {next_state.heuristic}")
            states.append(next_state.export())
            self.addStatetoOpenList(next_state)
            # We want to keep track of each state parent:
            self.solvedStates[next_state.predicates] = current_state
        # We send the current state to the closed list, because we expanded it:
        self.addStatetoClosedList(current_state)
        return states

    async def send_states(self,
                          states: list,
                          base_server_url: str,
                          session: ClientSession):
        async with session.post(base_server_url + "/pushState",
                                json=json.dumps({"list_states": states})) as resp:
            logging.info("Sending %s", len(states))
            return await resp.text()
