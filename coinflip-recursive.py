# https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip-recursive.yaml
#coinflip-recursive is a variation of the coinflip example.
# This is an example of a dynamic workflow which extends
# indefinitely until it acheives a desired result. In this
# example, the 'flip-coin' step is recursively repeated until
# the result of the step is "heads".
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def random_code():
    import random

    res = "heads" if random.randint(0, 1) == 0 else "tails"
    print(res)

def flip_coin():
    result = "tails"
    while result == "tails":
        result = couler.run_script(image="python:alpine3.6", source=random_code)
    return result
    

def heads():
    return couler.run_container(
        image="alpine:3.6", command=["sh", "-c", 'echo "it was heads"']
    )


resultHeads = flip_coin()
couler.when(couler.equal(resultHeads, "heads"), lambda: heads())
print("heads")
submitter = ArgoSubmitter()
couler.run(submitter=submitter)
