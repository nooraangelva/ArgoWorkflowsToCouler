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

    lista_a=["A","A","A"]
    lista_b=["B","B","B"]
    lista_c=["C","C","C"]
    lista_d=["D","D","D"]

    echo_trice(lista=lista_a)
    echo_trice(lista=lista_b)
    echo_trice(lista=lista_c)
    echo_trice(lista=lista_d)


    ''' couler map does not work with dag or dependencies. Does the function only ones  
    couler.dag(
        [
            [lambda: couler.map(lambda x: echo(x), lista_a)],
            [lambda: couler.map(lambda x: echo(x), lista_a), lambda: couler.map(lambda x: echo(x), lista_b)],  # A -> B
            [lambda: couler.map(lambda x: echo(x), lista_a), lambda: couler.map(lambda x: echo(x), lista_c)],  # A -> C
            [lambda: couler.map(lambda x: echo(x), lista_b), lambda: couler.map(lambda x: echo(x), lista_d)],  # B -> D
            [lambda: couler.map(lambda x: echo(x), lista_c), lambda: couler.map(lambda x: echo(x), lista_d)],  # C -> D
        ]
    )

     couler.set_dependencies(lambda: couler.map(lambda x: echo(x), lista_a), dependencies=None)
     '''
   

map_diamond()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
#print(couler.run(submitter=submitter))
