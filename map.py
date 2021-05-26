# using map function 4x
#           *
#         / | \
#       x   x  x
#         \ | /
#           *


from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def echo_trice(lista):
    '''calls echo function three times the same as the lis size.'''
    couler.map(lambda x: echo(x), lista)

def echo(message):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message], step_name=message,
    )

def map_diamond():
    '''main function (the brains) calls function echo_trice and sends lists to function'''

    lista_a=["A1","A2","A3"]
    
    echo_trice(lista=lista_a)
    

    

map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
