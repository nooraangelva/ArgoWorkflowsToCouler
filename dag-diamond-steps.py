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

#Diamond2 - odd errors - but works now
def listCreation(message):
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

    

def diamond2(): #odd errors

    couler.set_dependencies(lambda: job_x(message="X1"), dependencies=None)
    #couler.set_dependencies(lambda: job(message="A"), dependencies=["X1"])
    couler.set_dependencies(lambda: job_a(message="A1"), dependencies=["X1"])
    couler.set_dependencies(lambda: job_a(message="A2"), dependencies=["X1"])
    couler.set_dependencies(lambda: job_a(message="A3"), dependencies=["X1"])
    depe = listCreation(message="A")
    #print(depe)
    couler.set_dependencies(lambda: job_x(message="X2"), dependencies=depe) #Error: Nonetype? Even though it's a list
    couler.set_dependencies(lambda: job_x(message="X3"), dependencies=["X2"]) #accepts lists too
    couler.set_dependencies(lambda: job_x(message="X4"), dependencies=["X2"])

    #couler.set_dependencies(lambda: job(message="B"), dependencies=["X3"])
    couler.set_dependencies(lambda: job_b(message="B1"), dependencies=["X3"])
    couler.set_dependencies(lambda: job_b(message="B2"), dependencies=["X3"])
    couler.set_dependencies(lambda: job_b(message="B3"), dependencies=["X3"])
    depe2 = listCreation(message="B")
    #print(depe2)
    couler.set_dependencies(lambda: job_x(message="X5"), dependencies=depe2)
    #couler.set_dependencies(lambda: job(message="C"), dependencies=["X4"])
    couler.set_dependencies(lambda: job_c(message="C1"), dependencies=["X4"])
    couler.set_dependencies(lambda: job_c(message="C2"), dependencies=["X4"])
    couler.set_dependencies(lambda: job_c(message="C3"), dependencies=["X4"])
    depe3 = listCreation(message="C")
    #print(depe3)
    couler.set_dependencies(lambda: job_b(message="X6"), dependencies=depe3)
    couler.set_dependencies(lambda: job_b(message="X7"), dependencies=["X6","X5"])
    #couler.set_dependencies(lambda: job(message="D"), dependencies=["X7"])
    couler.set_dependencies(lambda: job_d(message="D1"), dependencies=["X7"])
    couler.set_dependencies(lambda: job_d(message="D2"), dependencies=["X7"])
    couler.set_dependencies(lambda: job_d(message="D3"), dependencies=["X7"])
    depe4 = listCreation(message="D")
    #print(depe4)
    couler.set_dependencies(lambda: job_d(message="X8"), dependencies=depe4)


diamond2()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
