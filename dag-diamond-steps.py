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


def job_a(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name="A",
    )


def job_b(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name=message,
    )


def job_c(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name="B",
    )


def job_d(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name="D",
    )


#           *
#         / | \
#       A1 A2  A3
#         \ | /
#           *
#   
def diamond():
    couler.dag(
        [
            [lambda: job_a(message="*")],
            [lambda: job_a(message="*"), lambda: job_b(message="A1")],  # A -> B
            [lambda: job_a(message="*"), lambda: job_b(message="A2")],  # A -> C
            [lambda: job_a(message="*"), lambda: job_b(message="A3")],  # B -> D
            [lambda: job_b(message="A1"), lambda: job_c(message="*")],  # C -> D
            [lambda: job_b(message="A1"), lambda: job_c(message="*")],  # C -> D
            [lambda: job_b(message="A2"), lambda: job_c(message="*")],  # C -> D
            [lambda: job_b(message="A3"), lambda: job_c(message="*")],  # C -> D
        ]
    )


diamond()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
