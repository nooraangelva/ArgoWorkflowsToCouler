# https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool to a workflow
# Couler version:
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume


def Step(volume_mount):
    '''Generates file myoutput.root and \
    copies it to a volume for the other steps '''

    couler.run_container(
        image="cmsopendata/cmssw_5_3_32:latest",
        command=["bash", "-c"],
        args=[
            "source /opt/cms/entrypoint.sh; \
             git clone git://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; \
             cd PhysObjectExtractorTool; \
             cd PhysObjectExtractor; \
             scram b;  ln -s python/poet_cfg.py .; \
             cmsRun poet_cfg.py; \
             cp myoutput.root /mnt/vol/; \
             ls -a /mnt/vol/ ",
        ],
        volume_mounts=[volume_mount],
        step_name="first"
    )


def StepOne(volume_mount):
    '''Generates a histogram using file myoutput.root, EventLoopAnalysis '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        command=["bash", "-c"],
        args=["source /opt/cms/cmsset_default.sh; \
            cd $HOME/CMSSW_10_6_12/src; eval `scramv1 runtime -sh`; \
             git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; \
             cd PhysObjectExtractorTool; \
             cd PhysObjectExtractor; \
             cd test; \
             \cp -r /mnt/vol/myoutput.root ./; \
             g++ -g -O3 -Wall -Wextra -o EventLoopAnalysis EventLoopAnalysisTemplate.cxx $(root-config --cflags --libs); \
             ./EventLoopAnalysis; \
             ls -a;",
              ],
        volume_mounts=[volume_mount],
    )


def StepTwo(volume_mount):
    '''Generates a histogram using file myoutput.root, RDFAnalysis '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        command=["bash", "-c"],
        args=[
            "source /opt/cms/cmsset_default.sh;\
             cd $HOME/CMSSW_10_6_12/src; eval `scramv1 runtime -sh`; \
             git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; \
             cd PhysObjectExtractorTool; \
             cd PhysObjectExtractor; cd test; \
             \cp -r /mnt/vol/myoutput.root ./; \
             g++ -g -O3 -Wall -Wextra -Wpedantic -o RDFAnalysis RDFAnalysisTemplate.cxx $(root-config --cflags --libs); \
             ./RDFAnalysis; \
             ls -a;",
        ],
        volume_mounts=[volume_mount],
    )


def opendata():
    '''creates volume and executes containers by calling the functions (containers)'''

    # Create volume
    volume = VolumeClaimTemplate("workdir", ['ReadWriteMany'], '1Gi')
    create_workflow_volume(volume)
    volume_mount = VolumeMount("workdir", "/mnt/vol")

    couler.set_dependencies(lambda: Step(
        volume_mount=volume_mount), dependencies=None)
    couler.set_dependencies(lambda: StepOne(
        volume_mount=volume_mount), dependencies=["first"])
    couler.set_dependencies(lambda: StepTwo(
        volume_mount=volume_mount), dependencies=["first"])


opendata()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
