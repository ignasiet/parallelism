import asyncio
import os
from libs.distributed.server import AstarServer
from libs.classes.parser import MyParser

import time

def server():
    path = os.getenv("problem")
    p = MyParser(path)
    binary_rep = os.getenv("binary", 'False').lower() in ('true', '1', 't')
    print(f"Using Binary representation: {binary_rep}")

    AstarServer(initialState=p.getInitState(binary_rep),
                actions=p.getActions(binary_rep),
                goals=p.getGoal(binary_rep))


if __name__ == "__main__":
    server()
