# using map function
#           *
#         / | \
#       A1 A2  A3
#         \ | /
#           *

from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def echo_trice(lista):

    couler.map(lambda x: echo_a(x), lista)

def echo_a(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message], step_name="A",
    )

def echo_b(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message], step_name="B",
    )

def echo_c(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message], step_name="C",
    )

def echo_d(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message], step_name="D",
    )

def map_diamond():
    '''main function (the brains) creates dependencies and calls functions '''
        
    lista_a=["A1","A2","A3"]
    lista_b=["B1","B2","B3"]
    lista_c=["C1","C2","C3"]
    lista_d=["D1","D2","D3"]

    couler.set_dependencies(lambda: couler.map(lambda x: echo_a(x), lista_a), dependencies=None)
    couler.set_dependencies(lambda: couler.map(lambda x: echo_b(x), lista_b), dependencies=["A"])
    couler.set_dependencies(lambda: couler.map(lambda x: echo_c(x), lista_c), dependencies=["A"])
    couler.set_dependencies(lambda: couler.map(lambda x: echo_d(x), lista_d), dependencies=["B","C"])

map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
