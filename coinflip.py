# https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip.yaml
# This is an example of a workflow which
# flips a coin once and tells if it was heads or tails

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def result_check():
    '''checks if the flip_coin functions results was heads or tails and prints it'''
    import random

    res = "heads" if random.randint(0, 1) == 0 else "tails"
    print(res)


def flip_coin():
    '''runs the function result_code in a python container'''
    return couler.run_script(image="python:alpine3.6", source=result_check)


def heads():
    return couler.run_container(
        image="alpine:3.6", command=["sh", "-c", 'echo "it was heads"']
    )


def tails():
    return couler.run_container(
        image="alpine:3.6", command=["sh", "-c", 'echo "it was tails"']
    )


result = flip_coin()
couler.when(couler.equal(result, "heads"), lambda: heads())
couler.when(couler.equal(result, "tails"), lambda: tails())

submitter = ArgoSubmitter()
couler.run(submitter=submitter)
