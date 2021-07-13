apiVersion: argoproj.io/v1alpha1
kind: Workflow
metadata:
  generateName: kati-
spec:
  entrypoint: boss
  volumeClaimTemplates:
  - metadata:
      name: workdir
    spec:
      accessModes: ["ReadWriteMany"]
      resources:
        requests:
          storage: 1Gi
  volumes:
  - name: cloud-pass


  templates:
  - name: boss
    dag:
      tasks:
      - name: first-step
        template: first-step-template
      - name: second-first-way-step
        dependencies: [first-step]
        template: second-step-first-template
      - name: second-second-way-step
        dependencies: [first-step]
        template: second-step-two-template


  - name: first-step-template
    script:
      image: cmsopendata/cmssw_5_3_32
      command: [bash]
      source: | 
        source /opt/cms/entrypoint.sh
        git clone git://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git
        cd PhysObjectExtractorTool
        cd PhysObjectExtractor
        scram b
        ln -s python/poet_cfg.py .
        ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA FT_53_LV5_AN1
        ln -sf /cvmfs/cms-opendata-conddb.cern.ch/FT_53_LV5_AN1_RUNA.db FT_53_LV5_AN1_RUNA.db
        cmsRun poet_cfg.py
        cp myoutput.root /mnt/vol/
        ls -a  /mnt/vol/
      volumeMounts:
      - name: workdir
        mountPath: /mnt/vol

  - name: second-step-first-template
    script:
      image: nooraangelva/cmssw:10_6_12-argo-v2
      command: [bash]
      source: | 
        source /opt/cms/cmsset_default.sh
        cd $HOME/CMSSW_10_6_12/src
        eval `scramv1 runtime -sh`

        git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git
        cd PhysObjectExtractorTool
        cd PhysObjectExtractor
        cd test
        \cp -r /mnt/vol/myoutput.root ./
        g++ -g -O3 -Wall -Wextra -o EventLoopAnalysis EventLoopAnalysisTemplate.cxx $(root-config --cflags --libs)
        ./EventLoopAnalysis
        ls -a

      volumeMounts:
      - name: workdir
        mountPath: /mnt/vol

  - name: second-step-two-template
    script:
      image: nooraangelva/cmssw:10_6_12-argo-v2
      command: [bash]
      source: | 
        source /opt/cms/cmsset_default.sh
        cd $HOME/CMSSW_10_6_12/src
        eval `scramv1 runtime -sh`

        git clone https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool.git
        cd PhysObjectExtractorTool
        cd PhysObjectExtractor
        cd test
        \cp -r /mnt/vol/myoutput.root ./
        g++ -g -O3 -Wall -Wextra -Wpedantic -o RDFAnalysis RDFAnalysisTemplate.cxx $(root-config --cflags --libs)
        ./RDFAnalysis
        ls -a

      volumeMounts:
      - name: workdir
        mountPath: /mnt/vol
  



  

