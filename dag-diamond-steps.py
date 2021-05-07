# The following workflow executes a diamond workflow, with each
# node comprising of three parallel fan-in fan-out steps.
# 
#           *
#         / | \
#       A1 A2  A3
#         \ | /
#           *
#         /   \ 
#       /       \
#      *         *
#    / | \     / | \
#  B1  B2 B3  C1 C2 C3
#    \ | /     \ | /
#      *         *
#       \       /
#         \   /
#           *
#         / | \
#       D1 D2  D3
#         \ | /
#           *

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def echo_trice(message):
    i = 1
    while i <4:
        message = message + str(i)
        i = i+ 1
        echo(message)
   

def echo(message):
    couler.run_container(
        image="alpine:3.6",
        command=["echo"],
        args=[message],
        step_name="echo",
    )

def diamond():
    couler.dag(
        [
            [lambda: echo_trice(message="A")],
            [lambda: echo_trice(message="A"), lambda: echo_trice(message="B")],  # A -> B
            [lambda: echo_trice(message="A"), lambda: echo_trice(message="C")],  # A -> C
            [lambda: echo_trice(message="B"), lambda: echo_trice(message="D")],  # B -> D
            [lambda: echo_trice(message="C"), lambda: echo_trice(message="D")],  # C -> D
        ]
    )


diamond()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)