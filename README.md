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

To run the planner on kubernetes using helm, use the following command:

    helm install astar ./astar

Or if you want to test the parallel version:

    helm install astar-parallel ./astar-parallel

### Known issues:
The parallel version does not return the whole plan yet. This functionality is only available on the simple version.
Also, the parallel version is worse on most domains, except when using domains with a high branching factor.