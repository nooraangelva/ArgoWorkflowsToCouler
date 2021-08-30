# using map() a simple example of scatter with several parameters
#
#           *
#         / | \
#       x   x  x

from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def echo(message1, message2):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message1, message2]
    )


def map_diamond():
    '''main function (the brains) calls function echo_trice and sends lists to function'''

    test_paras = ["t1", "t2", "t3"]
    test_paras2 = ["cowsay", "echo", "cat"]
    couler.map(lambda x, y: echo(x, y), test_paras, test_paras2)


map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
# print(couler.run(submitter=submitter))
