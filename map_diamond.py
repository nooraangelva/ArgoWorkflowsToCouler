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
     couler.map(lambda x: echo(x), lista)

def echo_a(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=["A"], step_name=message,
    )

def echo_b(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=["B"], step_name=message,
    )

def map_diamond():
    '''main function (the brains) creates dependencies and calls functions '''
        
    lista_a=["A1","A2","A3"]
    lista_b=["B1","B2","B3"]
    lista_c=["C1","C2","C3"]
    lista_d=["D1","D2","D3"]

    couler.set_dependencies(lambda: echo_trice(lista=lista_a), dependencies=None)
    couler.set_dependencies(lambda: echo_trice(lista=lista_b), dependencies=["A"])
    #couler.set_dependencies(lambda: echo_trice(lista=lista_c), dependencies=["A"])
    #couler.set_dependencies(lambda: echo_trice(lista=lista_d), dependencies=["B","C"])

map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
