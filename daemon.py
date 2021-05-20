# the code tests exit handler. the code does the error exit handler.
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume

    

def nginx_server():
    couler.run_container(
        image="nginx:1.13", 
        daemon="true",
        command=["sh, -c"],
        step_name="nginx_server",
        timeout=1   
    )
    return 0


def nginx_client(ip):
    couler.run_container(
        image="appropriate/curl:latest", 
        command=["/bin/sh", "-c"],
        args=["echo curl --silent -G http://{{inputs.parameters.server-ip}}:80/ && curl --silent -G http://{{inputs.parameters.server-ip}}:80/"],
        step_name="nginx_client",
        
    )
    return 0


def daemon_nginx_example():
    
    nginx_server()
    nginx_client()

daemon_nginx_example()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
