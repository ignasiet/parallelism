# [WIP] Parallel algorithms example with K8s

This code is an example of using Kubernetes to deploy an A* algorithm that can use parallelism. 
It will simulate a central message broker, that will coordinate all the different pods.

Please note, this example is still in progress.

## Running

To run the tests, please:

    python -m unittest

You can also run the algorithm outside Kubernetes:

    python -m main

Note that in this case you should set your env vars to point to the problem that will be used as example.
