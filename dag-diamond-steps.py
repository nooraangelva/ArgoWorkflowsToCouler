# the code executes the functions, that echo A1, A2... visually in the following way.
# Doesn't use scatter function from yaml (map() in couler)
#           X1
#         / | \
#       A1 A2  A3
#         \ | /
#           X2
#         /   \
#       /       \
#      X3         X4
#    / | \     / | \
#  B1  B2 B3  C1 C2 C3
#    \ | /     \ | /
#      X5         X6
#       \       /
#         \   /
#           X7
#         / | \
#       D1 D2  D3
#         \ | /
#           X8

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def job_x(message):
    couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c", 'echo "'+message+'"'],
        args=[message],
        step_name=message,
    )


def job_a(message):
    couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c", 'echo "'+message+'"'],
        args=[message],
        step_name=message,
    )


def job_b(message):
    couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c", 'echo "'+message+'"'],
        args=[message],
        step_name=message,
    )


def job_c(message):
    couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c", 'echo "'+message+'"'],
        args=[message],
        step_name=message,
    )


def job_d(message):
    couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c", 'echo "'+message+'"'],
        args=[message],
        step_name=message,
    )


def listCreation(message):
    '''creates list of dependencies with given letter'''
    listNum = [1, 2, 3]
    newList = list(())
    for x in listNum:
        newList.append(message+str(x))

    return newList


def diamond():

    couler.set_dependencies(lambda: job_x(message="X1"), dependencies=None)
    couler.set_dependencies(lambda: job_a(message="A1"), dependencies=["X1"])
    couler.set_dependencies(lambda: job_a(message="A2"), dependencies=["X1"])
    couler.set_dependencies(lambda: job_a(message="A3"), dependencies=["X1"])
    dep1 = listCreation(message="A")

    couler.set_dependencies(lambda: job_x(message="X2"), dependencies=dep1)
    couler.set_dependencies(lambda: job_x(message="X3"), dependencies=["X2"])
    couler.set_dependencies(lambda: job_x(message="X4"), dependencies=["X2"])

    couler.set_dependencies(lambda: job_b(message="B1"), dependencies=["X3"])
    couler.set_dependencies(lambda: job_b(message="B2"), dependencies=["X3"])
    couler.set_dependencies(lambda: job_b(message="B3"), dependencies=["X3"])
    dep2 = listCreation(message="B")

    couler.set_dependencies(lambda: job_x(message="X5"), dependencies=dep2)
    couler.set_dependencies(lambda: job_c(message="C1"), dependencies=["X4"])
    couler.set_dependencies(lambda: job_c(message="C2"), dependencies=["X4"])
    couler.set_dependencies(lambda: job_c(message="C3"), dependencies=["X4"])
    dep3 = listCreation(message="C")

    couler.set_dependencies(lambda: job_b(message="X6"), dependencies=dep3)
    couler.set_dependencies(lambda: job_b(message="X7"),
                            dependencies=["X6", "X5"])
    couler.set_dependencies(lambda: job_d(message="D1"), dependencies=["X7"])
    couler.set_dependencies(lambda: job_d(message="D2"), dependencies=["X7"])
    couler.set_dependencies(lambda: job_d(message="D3"), dependencies=["X7"])
    dep4 = listCreation(message="D")
    couler.set_dependencies(lambda: job_d(message="X8"), dependencies=dep4)


diamond()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
