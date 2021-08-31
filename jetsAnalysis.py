# https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/inputs.yaml
# Task: https://github.com/cms-dpoa/cms-dpoa-getting-started/issues/78
# Couler version:
import sys
import base64
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume, add_volume


def get_conditions_template(volume_mount, sampleid):
    '''clean up and creation of dir'''
    couler.run_container(
        image="peterevans/curl-jq",
        args=[''' curl_command="curl https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get/'''+sampleid+''' -k --silent"; \
        eval $curl_command | jq ".results.sequences[].pileup" | sed s/'"'/''/g > /mnt/vol/pileup.txt; \
        eval $curl_command | jq ".results.sequences[].conditions" | sed s/'"'/''/g > /mnt/vol/conditions.txt; \
        eval $curl_command | jq ".results.cmssw_release" | sed s/'"'/''/g > /mnt/vol/release.txt; \
        echo -n "Pileup: "; \
        cat /mnt/vol/pileup.txt; \
        echo -n "Conditions: "; \
        cat /mnt/vol/conditions.txt; \
        echo -n "CMSSW release: "; \
        cat /mnt/vol/release.txt;'''],
        command=["sh", "-c"],
        step_name="get-conditions",
        volume_mounts=[volume_mount],
    )
    return 0


def create_PU_dist_template(volume_mount, puDistData, puDistMc):
    '''Generate '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        args=['''#cp input/PileupHistogram-goldenJSON-13tev-2018-69200ub-100bins.root '''+puDistData+'''; \
        source /opt/cms/cmsset_default.sh; \
        cd $HOME/CMSSW_10_6_12/src; \
        eval `scramv1 runtime -sh`; \
        python makeMCPileupHist.py SimGeneral.MixingModule.mix_$(cat /mnt/vol/pileup.txt)_cfi --outputFilename '''+puDistMc+''';'''
              ],
        command=["bash", "-c"],
        step_name="create-PU-dist",
        volume_mounts=[volume_mount],
    )
    return 0


def reana_access_template(volume_mount):
    '''Generate '''

    access_key = ["keytab_encoded"]
    secret = couler.obtain_secret(
        secret_keys=access_key, namespace="argo", name="encodedjet", dry_run=True,
    )

    couler.run_container(
        image="nooraangelva/reana-auth-krb5",
        command=["bash", "-c"],
        args=["echo $keytab_encoded | base64 -d > /mnt/vol/.keytab; kinit -k -t /mnt/vol/.keytab nangelva@CERN.CH; id; klist; ls -l /tmp/krb5cc_1000; cp /tmp/krb5cc_1000 /mnt/vol;"
              ],
        step_name="reana-access",
        volume_mounts=[volume_mount],
        secret=secret
    )
    return 0


def produce_ntuple_template(algo, cone_size, jet_type, para1, para2, output, volume_mount):
    '''Generate '''

    couler.run_container(
        image="nooraangelva/cmssw:10_6_12-argo-v2",
        command=["bash", "-c"],
        args=['''mount_vol_files=/mnt/vol/files.txt; 
        echo "root://eosuser.cern.ch//eos/user/a/adlintul/REANA/RunIISummer19UL18/"'''+para1+''' > $mount_vol_files; \
        echo "root://eosuser.cern.ch//eos/user/a/adlintul/REANA/RunIISummer19UL18/"'''+para2+''' >> $mount_vol_files; \
      
        cp /mnt/vol/krb5cc_1000 /tmp; \
        KRB5CCNAME=FILE:/mnt/vol/krb5cc_1000; \

        source /opt/cms/cmsset_default.sh; \
        cd $HOME/CMSSW_10_6_12/src; \
        eval `scramv1 runtime -sh`; \
        
        algorithm=$(echo '''+algo+cone_size+jet_type+''' | tr '[:upper:]' '[:lower:]'); \

        #for i in $(cat $mount_vol_files); do
        #   ./RunListRunLumi $i $algorithm >> '''+output+''';
        #done '''
              ],
        volume_mounts=[volume_mount],
    )
    return 0


def opendata():
    '''creates volume and executes containers by calling functions (containers)'''

    # Create volume
    volume = VolumeClaimTemplate("workdir", ['ReadWriteMany'], '1Gi')
    # create_workflow_volume(volume)
    #volume = Volume("workdir", "task-pv-sc-claim")
    volume_mount = VolumeMount("workdir", "/mnt/vol")
    add_volume(volume)

    sampleid = "JME-RunIISummer19UL18DIGI-00012"
    puDistData = "/mnt/vol/MyDataPileupHistogram.root"
    puDistMc = "/mnt/vol/MyMCPileupHistogram.root"
    algo = ["AK", "AK"]
    cone_size = ["4", "4"]
    jet_type = ["PFchs", "PFchs"]
    para1 = ["FlatPU/JRA_101.root", "EpsilonPU/JRA_1.root"]
    para2 = ["FlatPU/JRA_102.root", "EpsilonPU/JRA_10.root"]
    output = ["/mnt/vol/lumi_file_PU.txt", "/mnt/vol/lumi_file_noPU.txt"]
    volumes = [volume_mount, volume_mount]

    # Steps execution
    couler.set_dependencies(lambda: get_conditions_template(
        volume_mount=volume_mount, sampleid=sampleid), dependencies=None)
    couler.set_dependencies(lambda: create_PU_dist_template(
        volume_mount, puDistData, puDistMc), dependencies=["get-conditions"])
    couler.set_dependencies(lambda: reana_access_template(
        volume_mount), dependencies=["create-PU-dist"])
    #couler.set_dependencies(lambda: couler.map(lambda a,s,d,f,g,h,j: produce_ntuple_template(a,s,d,f,g,h,j), algo,cone_size,jet_type,para1,para2,output,volumes), dependencies=["reana-access"])


opendata()
# couler.config_workflow(name="pytest")
submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
