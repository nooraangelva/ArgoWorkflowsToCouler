# 
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
# Gives an erro at first but when you press retry in Argo works well
# using diamond2 not diamond in workflow

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def job_x(message):
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo "X"'],
        args=[message],
        step_name=message,
    )


def job_a(message):
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo "A"'],
        args=[message],
        step_name=message,
    )


def job_b(message):
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo "B"'],
        args=[message],
        step_name=message,
    )


def job_c(message):
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo "C"'],
        args=[message],
        step_name=message,
    )

def job_d(message):
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo "D"'],
        args=[message],
        step_name=message,
    )

#Diamond2 - odd errors
def depen(message):
    listan = [1,2,3]
    dlista = list(())
    for x in listan:
        dlista.append(message+str(x))
    return dlista

def job(message):
    lista = ["1","2","3"]
    for x in lista:
        if message == "A":
            job_a(message=message+x)
        elif message == "B":
            job_b(message=message+x)
        elif message == "C":
            job_c(message=message+x)
        elif message == "D":
            job_d(message=message+x)

def diamond():
    couler.dag(
        [
            [lambda: job_x(message="X1")],
            [lambda: job_x(message="X1"), lambda: job_a(message="A1")],  # X1 -> A1
            [lambda: job_x(message="X1"), lambda: job_a(message="A2")],  # X1 -> A2
            [lambda: job_x(message="X1"), lambda: job_a(message="A3")],  # X1 -> A3
            [lambda: job_a(message="A1"), lambda: job_x(message="X2")],  # A1 -> X2
            [lambda: job_a(message="A2"), lambda: job_x(message="X2")],  # A2 -> X2
            [lambda: job_a(message="A3"), lambda: job_x(message="X2")],  # A3 -> X2
            [lambda: job_x(message="X2"), lambda: job_x(message="X3")],  # X2 -> X3
            [lambda: job_x(message="X2"), lambda: job_x(message="X4")],  # X2 -> X4
            [lambda: job_x(message="X3"), lambda: job_b(message="B1")],  # X3 -> B1
            [lambda: job_x(message="X3"), lambda: job_b(message="B2")],  # X3 -> B2
            [lambda: job_x(message="X3"), lambda: job_b(message="B3")],  # X3 -> B3
            [lambda: job_x(message="X4"), lambda: job_c(message="C1")],  # X3 -> C1
            [lambda: job_x(message="X4"), lambda: job_c(message="C2")],  # X4 -> C2
            [lambda: job_x(message="X4"), lambda: job_c(message="C3")],  # X4 -> C3
            [lambda: job_c(message="C1"), lambda: job_x(message="X5")],  # C1 -> X5
            [lambda: job_c(message="C2"), lambda: job_x(message="X5")],  # C2 -> X5
            [lambda: job_c(message="C3"), lambda: job_x(message="X5")],  # C3 -> X5
            [lambda: job_b(message="B1"), lambda: job_x(message="X6")],  # B1 -> X6
            [lambda: job_b(message="B2"), lambda: job_x(message="X6")],  # B2 -> X6
            [lambda: job_b(message="B3"), lambda: job_x(message="X6")],  # B3 -> X6
            [lambda: job_x(message="X5"), lambda: job_x(message="X7")],  # X5 -> X7
            [lambda: job_x(message="X6"), lambda: job_x(message="X7")],  # X6 -> X7
            [lambda: job_x(message="X7"), lambda: job_d(message="D1")],  # X7 -> D1
            [lambda: job_x(message="X7"), lambda: job_d(message="D2")],  # X7 -> D2
            [lambda: job_x(message="X7"), lambda: job_d(message="D3")],  # X7 -> D3
            [lambda: job_d(message="D1"), lambda: job_x(message="X8")],  # D1 -> X8
            [lambda: job_d(message="D2"), lambda: job_x(message="X8")],  # D2 -> X8
            [lambda: job_d(message="D3"), lambda: job_x(message="X8")],  # D3 -> X8
        ]
    )
    

def diamond2(): #odd errors

    couler.set_dependencies(lambda: job_x(message="X1"), dependencies=None)
    couler.set_dependencies(lambda: job(message="A"), dependencies="X1")
    #couler.set_dependencies(lambda: job(message="A1"), dependencies="X1")
    #couler.set_dependencies(lambda: job_a(message="A2"), dependencies="X1")
    #couler.set_dependencies(lambda: job_a(message="A3"), dependencies="X1")
    depe = depen(message="A")
    print(depe)
    couler.set_dependencies(lambda: job_x(message="X2"), dependencies=depe) #Error: Nonetype? Even though it's a list
    couler.set_dependencies(lambda: job_x(message="X3"), dependencies="X2") #accepts lists too
    couler.set_dependencies(lambda: job_x(message="X4"), dependencies="X2")

    couler.set_dependencies(lambda: job(message="B"), dependencies="X3")
    #couler.set_dependencies(lambda: job_b(message="B1"), dependencies="X3")
    #couler.set_dependencies(lambda: job_b(message="B2"), dependencies="X3")
    #couler.set_dependencies(lambda: job_b(message="B3"), dependencies="X3")
    depe2 = depen(message="B")
    print(depe2)
    couler.set_dependencies(lambda: job_x(message="X5"), dependencies=depe2)
    couler.set_dependencies(lambda: job(message="C"), dependencies="X4")
    #couler.set_dependencies(lambda: job_c(message="C1"), dependencies="X4")
    #couler.set_dependencies(lambda: job_c(message="C2"), dependencies="X4")
    #couler.set_dependencies(lambda: job_c(message="C3"), dependencies="X4")
    depe3 = depen(message="C")
    print(depe3)
    couler.set_dependencies(lambda: job_b(message="X6"), dependencies=depe3)
    couler.set_dependencies(lambda: job_b(message="X7"), dependencies=["X6","X5"])
    couler.set_dependencies(lambda: job(message="D"), dependencies="X7")
    #couler.set_dependencies(lambda: job_d(message="D1"), dependencies="X7")
    #couler.set_dependencies(lambda: job_d(message="D2"), dependencies="X7")
    #couler.set_dependencies(lambda: job_d(message="D3"), dependencies="X7")
    depe4 = depen(message="D")
    print(depe4)
    couler.set_dependencies(lambda: job_d(message="X8"), dependencies=depe4)


diamond2()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
