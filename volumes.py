# creates a hello_world.txt file with volumes and then opens it.
# https://github.com/couler-proj/couler/issues/193 had the same issue
# Solution, sense it has not been yet officaly published: https://github.com/couler-proj/couler/issues/193#issuecomment-843550006
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume
    

def whalesay(volume_mount):
    '''creates a hello_world.txt file'''
    couler.run_container(
        image="docker/whalesay:latest",
        args=["ls /mnt/; echo generating message in volume; cowsay hello world | tee /mnt/vol/hello_world.txt; echo generated message in volume; ls /mnt/vol;"],
        command=["sh", "-c"],
        step_name="generate",
        volume_mounts=[volume_mount],
    )
    return 0

def print_message(volume_mount): 
    '''finds the created file and echos it'''  
    couler.run_container(
        image="alpine:latest",
        args=["ls /mnt/vol; echo getting message from volume; cat /mnt/vol/hello_world.txt; "],
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
    whalesay(volume_mount=volume_mount)
    print_message(volume_mount=volume_mount)
    
    

volumes_pvc_example()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
