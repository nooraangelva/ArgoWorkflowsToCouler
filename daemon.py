# the code tests exit handler. the code does the error exit handler.
# https://www.bogotobogo.com/python/Multithread/python_multithreading_Daemon_join_method_threads.php
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
#from flask import request

def hello():
    couler.run_container(
    image="nginx:1.13",
    command=["nginx"], 
    step_name= "Server-",
    daemon=True,
)

def curl():
    couler.run_container(
    image="appropriate/curl:latest",
    command=["/bin/sh", "-c"], 
    args=["curl http://localhost:8080/"],
    step_name= "Curl-",
)

def daemon_nginx_example():
    
    
    hello()
    curl()


daemon_nginx_example()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
