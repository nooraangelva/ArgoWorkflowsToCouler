# 
#           X
#         / | \
#       A1 A2  A3
#         \ | /
#           X
#         /   \ 
#       /       \
#      X         X
#    / | \     / | \
#  B1  B2 B3  C1 C2 C3
#    \ | /     \ | /
#      X         X
#       \       /
#         \   /
#           X
#         / | \
#       D1 D2  D3
#         \ | /
#           X

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def job_x(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name=message,
    )


def job_a(message):
    couler.run_container(
        image="docker/whalesay:latest",
        command=["cowsay"],
        args=[message],
        step_name=message,
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
        step_name=message,
    )

def job_d(message):
    couler.run_container(
    image="docker/whalesay:latest",
    command=["cowsay"],
    args=[message],
    step_name=message,
    )



def diamond():
    couler.dag(
        [
            [lambda: job_x(message="X1")],
            [lambda: job_x(message="X1"), lambda: job_a(message="A1")],  # X -> A
            [lambda: job_x(message="X1"), lambda: job_a(message="A2")],  # X -> A
            [lambda: job_x(message="X1"), lambda: job_a(message="A3")],  # X -> A
            [lambda: job_a(message="A1"), lambda: job_x(message="X2")],  # A -> X
            [lambda: job_a(message="A2"), lambda: job_x(message="X2")],  # A -> X
            [lambda: job_a(message="A3"), lambda: job_x(message="X2")],  # A -> X
            [lambda: job_x(message="X2"), lambda: job_x(message="X3")],  # X -> X
            [lambda: job_x(message="X2"), lambda: job_x(message="X4")],  # X -> X
            [lambda: job_x(message="X3"), lambda: job_b(message="B1")],  # X -> B
            [lambda: job_x(message="X3"), lambda: job_b(message="B2")],  # X -> B
            [lambda: job_x(message="X3"), lambda: job_b(message="B3")],  # X -> B
            [lambda: job_x(message="X4"), lambda: job_c(message="C1")],  # X -> C
            [lambda: job_x(message="X4"), lambda: job_c(message="C2")],  # X -> C
            [lambda: job_x(message="X4"), lambda: job_c(message="C3")],  # X -> C
            [lambda: job_c(message="C1"), lambda: job_x(message="X5")],  # X -> X
            [lambda: job_c(message="C2"), lambda: job_x(message="X5")],  # C -> X
            [lambda: job_c(message="C3"), lambda: job_x(message="X5")],  # C -> X
            [lambda: job_b(message="B1"), lambda: job_x(message="X6")],  # B -> X
            [lambda: job_b(message="B2"), lambda: job_x(message="X6")],  # B -> X
            [lambda: job_b(message="B3"), lambda: job_x(message="X6")],  # B -> X
            [lambda: job_x(message="X5"), lambda: job_x(message="X7")],  # X -> X
            [lambda: job_x(message="X6"), lambda: job_x(message="X7")],  # X -> X
            [lambda: job_x(message="X7"), lambda: job_d(message="D1")],  # X -> D
            [lambda: job_x(message="X7"), lambda: job_d(message="D2")],  # X -> D
            [lambda: job_x(message="X7"), lambda: job_d(message="D3")],  # X -> D
            [lambda: job_d(message="D1"), lambda: job_x(message="X8")],  # D -> X
            [lambda: job_d(message="D2"), lambda: job_x(message="X8")],  # D -> X
            [lambda: job_d(message="D3"), lambda: job_x(message="X8")],  # D -> X
        ]
    )


diamond()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
