import asyncio
import random
import os
import time
from libs.distributed.client import AstarClient
from libs.classes.parser import MyParser

def client():
    path = os.getenv("problem")
    p = MyParser(path)
    binary_rep = os.getenv("binary", 'False').lower() in ('true', '1', 't')
    print(f"Using Binary representation: {binary_rep}")
    # Sleep 10 seconds after creation
    sleep_time = 5+random.randint(1,5)
    print(f"Waiting {sleep_time} seconds")
    time.sleep(sleep_time)

    as_client = AstarClient(initialState=p.getInitState(binary_rep),
                            actions=p.getActions(binary_rep),
                            goals=p.getGoal(binary_rep))
    asyncio.run(as_client.start(os.getenv("server")))

if __name__ == "__main__":
    client()
