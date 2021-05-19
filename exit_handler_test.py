# the code tests exit handler. the code does the error exit handler -> intentionaly fails.
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter


def intentional_fail():
    '''intentionaly fails so that the exit handler will do the cry()'''
    return couler.run_container(
        image="alpine:3.6",
        command=["sh", "-c"],
        step_name="failure-exit",
        args=["echo intentional failure; exit 1"],
    )


def celebrate():
    '''echos hooray if exithandler succeeds'''
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo hooray!'],
        args=["echo hooray!"],
        step_name="celebrate",
    )
    return 0

def cry():
    '''echos boohoo if intentional_fail() fails'''
    couler.run_container(
        image="alpine:3.6", 
        command=["sh", "-c", 'echo boohoo!'],
        args=["echo boohoo!"],
        step_name="cry",
    )
    return 0

# an exit handler that runs when the workflow succeeds.
couler.set_exit_handler(
    couler.WFStatus.Succeeded, celebrate
)
# an exit handler that runs when the workflow failed.
couler.set_exit_handler(couler.WFStatus.Failed, cry)

intentional_fail()


submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
