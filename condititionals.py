import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter

def should_print():
    return "false"

def print_hello():
    return couler.run_container(
        image="alpine:3.6", command=["sh", "-c", 'echo "it was true"']
    )



result = should_print()
couler.when(couler.equal(result, "true"), lambda: print_hello())

submitter = ArgoSubmitter()
couler.run(submitter=submitter)
