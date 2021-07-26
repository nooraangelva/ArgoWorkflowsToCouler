# coinflip-recursive is a variation of the coinflip example.
# This is an example of a dynamic workflow which extends
# indefinitely until it acheives a desired result. In this
# example, the 'flip-coin' step is recursively repeated until
# the result of the step is "heads".
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def random_code():
    '''randomly picks either 1 (tails) or 0 (heads) and returns it. '''
    import random

    res = "heads" if random.randint(0, 1) == 0 else "tails"
    print(res)
    

def heads():
    '''echos string when called'''
    return couler.run_container(
        image="alpine:3.6", command=["sh", "-c", 'echo "it was heads"']
    )

def flip_coin():
    '''calls for random_code() function as long as the result is tails. Then returns heads. '''
    result = "tails"
    while result == "tails":
        result = couler.run_script(image="python:alpine3.6", source=random_code)
    return result


resultHeads = flip_coin()
couler.when(couler.equal(resultHeads, "heads"), lambda: heads())
submitter = ArgoSubmitter()
couler.run(submitter=submitter)


