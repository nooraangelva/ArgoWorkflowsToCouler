#  The following workflow executes a diamond workflow, with each
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
from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def echo_trice(lista,letter):
    couler.map(lambda x: echo(x, letter), lista)

def echo(message, letter):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[letter+message], step_name=letter,
    )


def map_diamond():
    '''main function (the brains) creates dependencies and calls functions '''
        
    lista_a=["1","2","3"]
    
    #lista_b=["B1","B2","B3"]
    #lista_c=["C1","C2","C3"]
    #lista_d=["D1","D2","D3"]

    couler.set_dependencies(lambda: echo_trice(lista_a, "A"), dependencies=None)
    couler.set_dependencies(lambda: echo_trice(lista_a, "B"), dependencies=["A"])
    couler.set_dependencies(lambda: echo_trice(lista_a, "C"), dependencies=["A"])
    couler.set_dependencies(lambda: echo_trice(lista_a, "D"), dependencies=["B","C"])



map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
