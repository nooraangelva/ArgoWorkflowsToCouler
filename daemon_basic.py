# the code tests exit handler. the code does the error exit handler.
# https://www.bogotobogo.com/python/Multithread/python_multithreading_Daemon_join_method_threads.php
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
#from flask import request

def test():   
    import threading
    import time
    import logging

    logging.basicConfig(level=logging.DEBUG,
                        format='(%(threadName)-9s) %(message)s',) 

    def n():
        logging.debug('Starting')
        logging.debug('Exiting')

    def d():
        logging.debug('Starting')
        time.sleep(5)
        logging.debug('Exiting')

    t = threading.Thread(name='non-daemon', target=n)

    d = threading.Thread(name='daemon', target=d)
    d.setDaemon(True)

    d.start()
    t.start()


def daemon_nginx_example():
    
    
    couler.run_script(
        image="python:3", 
        source=test, 
        step_name="daemon-t", 
        daemon= True
    )


daemon_nginx_example()

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
