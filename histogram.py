
# Couler version:
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume


def Step(volume_mount):
    '''Generate '''

    couler.run_container(
        image="cmsopendata/cmssw_5_3_32:latest",
        command=["bash","-c"],
        args=[
            "source /opt/cms/entrypoint.sh; git clone git://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; cd PhysObjectExtractorTool; cd PhysObjectExtractor; scram b;  ln -s python/poet_cfg.py .; ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1; ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db; cmsRun poet_cfg.py; cp myoutput.root /mnt/vol/",
        ],
        volume_mounts=[volume_mount],
        step_name="first"
    )

def Stepone(volume_mount):
    '''Generate '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        command=["bash","-c"],
        args=[
            "source /opt/cms/cmsset_default.sh; cd $HOME/CMSSW_10_6_12/src; eval `scramv1 runtime -sh`; git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; cd PhysObjectExtractorTool; cd PhysObjectExtractor; cd test; \cp -r /mnt/vol/myoutput.root ./; g++ -g -O3 -Wall -Wextra -o EventLoopAnalysis EventLoopAnalysisTemplate.cxx $(root-config --cflags --libs); ./EventLoopAnalysis; ls -a",
        ],
        volume_mounts=[volume_mount],
    )

def Steptwo(volume_mount):
    '''Generate '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        command=["bash","-c"],
        args=[
            "source /opt/cms/cmsset_default.sh; cd $HOME/CMSSW_10_6_12/src; eval `scramv1 runtime -sh`; git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git; cd PhysObjectExtractorTool; cd PhysObjectExtractor; cd test; \cp -r /mnt/vol/myoutput.root ./; g++ -g -O3 -Wall -Wextra -Wpedantic -o RDFAnalysis RDFAnalysisTemplate.cxx $(root-config --cflags --libs); ./RDFAnalysis; ls -a",
        ],
        volume_mounts=[volume_mount],
    )
   
def opendata():
    '''creates volume and executes containers by calling functions (containers)'''

    # Create volume
    volume = VolumeClaimTemplate("vol-cephfs-bsm", ['ReadWriteMany'], '1Gi')
    create_workflow_volume(volume)
    volume_mount = VolumeMount("workdir", "/mnt/vol")
    
    couler.set_dependencies(lambda: Step(volume_mount), dependencies=None)
    couler.set_dependencies(lambda: Stepone(volume_mount), dependencies=["first"])
    couler.set_dependencies(lambda: Steptwo(volume_mount), dependencies=["first"])
    

opendata()
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
