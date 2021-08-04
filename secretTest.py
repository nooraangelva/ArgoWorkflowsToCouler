
# Couler version:
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume

    



def opendata():
    '''creates volume and executes containers by calling functions (containers)'''

    access_key = {"access_key": "key1234", "access_value": "value5678"}
    secret2 = couler.create_secret(
        secret_data=access_key, namespace="argo", name="dummypart7", dry_run=True
    )
    couler.run_container(
        image="ubuntu:latest", secret=secret2, command=["bash","-c", "echo $access_value"]
    )
    

opendata()
#couler.config_workflow(name="pytest")
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
