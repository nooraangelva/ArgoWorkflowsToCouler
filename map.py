# using map function
#           *
#         / | \
#       x   x  x

from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def consume(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message]
    )

def map_diamond():
    '''main function (the brains) calls function echo_trice and sends lists to function'''
    
    test_paras = ["t1", "t2", "t3"]
    couler.map(lambda x: consume(x), test_paras)

   

map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
