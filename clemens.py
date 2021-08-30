# discontinued development -> Couler has no support for multistep-scatter
# Task: https://github.com/cms-dpoa/cms-dpoa-getting-started/issues/78
# Couler version:

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume


def cleanup_recreate_dir(direc, volume_mount):
    '''clean up and creation of dir'''
    couler.run_container(
        image="reanahub/reana-demo-bsm-search",
        args=[],
        command=["bash", "-c", "set -x", "rm -rf "+direc, "mkdir -p "+direc, ],
        step_name="prepare-dir",
        volume_mounts=[volume_mount],
    )
    return 0


def wflow_all_mc(type, mcweight, nevents, njobs):

    # First draft - without dependencies
    #couler.run_script(image="python:alpine3.6", source=scatter_template, step_name="scatter", )
    # generate(type,nevents,njobs)
    # volume_mount=VolumeMount,type=type,nevents=nevents,njobs=njobs,base_dir="base-dir"

    # Second draft - with dependencies (dag - tasks)

    #couler.set_dependencies(lambda : couler.run_script(image="python:alpine3.6", source=scatter_template, step_name="scatter",), dependencies=None)
    #couler.set_dependencies(lambda: generate(type,nevents,njobs), dependencies=["scatter"])
    consume(message=type, message2=mcweight)

    return 0


def consume(message, message2):
    return couler.run_container(
        image="docker/whalesay:latest", command=["cowsay"], args=[message, message2]
    )


def scatter_template():
    '''Scater'''

    import json
    import sys

    json.dump([i for i in range(4)], sys.stdout)
    # https://github.com/couler-proj/couler/issues/196


def generate(type, nevents, njobs):
    '''Generate '''

    couler.run_container(
        image="reanahub/reana-demo-bsm-search",
        args=[],
        command=["bash", "-c", "set -x", "source /usr/local/bin/thisroot.sh",
                 "python /code/generantuple.py "+type+" "+nevents+" base-dir/"+type+"_"+njobs+".root"],
        volume_mounts=[VolumeMount("vol-cephfs-bsm", "/data/")],
    )
    return 0


def opendata():
    '''creates volume and executes containers by calling functions (containers)'''

    # Lists
    type = ["mc1", "mc2"]
    mcweight = ["0.1875", "0.0125"]
    nevents = ["40000", "40000"]
    njobs = ["4", "4"]
    base_dir = "base-dir"

    #x = 0

    # Create volume
    volume = VolumeClaimTemplate("vol-cephfs-bsm", ['ReadWriteMany'], '1Gi')
    create_workflow_volume(volume)
    volume_mount = VolumeMount("vol-cephfs-bsm", "/data/")

    # First draft without dependencies

    # cleanup_recreate_dir(direc="base-dir", volume_mount=volume_mount)
    # couler.map(lambda x,y,z,c: wflow_all_mc(x,y,z,c), type, mcweight, nevents, njobs)
    # couler.map(lambda x,y: consume(x,y), type, mcweight)
    # wflow_all_mc(type, mcweight, nevents, njobs)

    # Second draft with dependencies

    couler.set_dependencies(lambda: cleanup_recreate_dir(
        direc=base_dir, volume_mount=volume_mount), dependencies=None)
    couler.set_dependencies(lambda: couler.map(lambda x, y, z, c: wflow_all_mc(
        x, y, z, c), type, mcweight, nevents, njobs), dependencies=["prepare-dir"])


opendata()
# couler.config_workflow(name="pytest")
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
