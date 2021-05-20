
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume
    

def whalesay(volume_mount):
    '''creates a hello_world.txt file'''
    couler.run_container(
        image="docker/whalesay:latest",
        args=["echo generating message in volume; cowsay hello world | tee /mnt/vol/hello_world.txt"],
        command=["bash", "-c"],
        step_name="generate",
        volume_mounts=[volume_mount],
    )
    return 0

def print_message(volume_mount): 
    '''finds the created file and echos it'''  
    couler.run_container(
        image="alpine:latest",
        args=["echo getting message from volume; find /mnt/vol; cat /mnt/vol/hello_world.txt"],
        command=["sh", "-c"],
        step_name="print",
        volume_mounts=[volume_mount],
    )
    return 0


def volumes_pvc_example():
    '''creates volume and executes containers by calling functions'''
    volume = VolumeClaimTemplate("workdir")
    create_workflow_volume(volume)
    volume_mount = VolumeMount("workdir", "/mnt/vol")
    couler.set_dependencies(lambda: whalesay(volume_mount=volume_mount), dependencies=None)
    couler.set_dependencies(lambda: print_message(volume_mount=volume_mount), dependencies=["generate"])
    
    

volumes_pvc_example()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
