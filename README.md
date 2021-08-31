# ArgoWorkflowsToCouler
This repository contains Argo workflows implemented in a couler format.
The original Argo workflows are from [Argo's](https://github.com/argoproj/argo-workflows/tree/master/examples) repository

Repository also contains some Argo workflows that are using CERN's opendata.

## Documentation about Argo, Couler, codes and thoughts about them
[CodiMD](https://codimd.web.cern.ch/UCT5cM_yTsWqM79VLiGnbw?view)

## Explained .yaml file
[Argo workflow explained](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip.yaml)

## suspend.yaml file
[Argo workflow](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/suspend.yaml)

## Coinflip
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip.yaml)

## Coinflip recursive
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip-recursive.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip-recursive.yaml)

## Dag-diamond-steps
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/dag-diamond-steps.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)

## Hello world
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/helloworld.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/hello-world.yaml)

## Conditionals
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/conditionals.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/conditionals.yaml)

## Exit handler
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/exit_handler_test.py) (removed the send email step)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/exit-handlers.yaml)

## Volumes
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/volumes.py)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/volumes-pvc.yaml)

## Map
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/map.py) (Basic example of usage)
- [Argo-version](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)

## Getting a file and sorting it
[Task](https://github.com/cms-dpoa/cms-dpoa-getting-started/issues/78)
- [Couler-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/file_retrieve.py)
- [Argo-version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/file_retrieve.yaml)

## Secret
- [Couler - creates also secret](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/secretC.py)
- [Couler - uses already existing secret](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/secret.py)
- [Argo](https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/histogram.yaml)

## a way to extract information from a CMS root file type EDM and creating histograms
- [Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/histogram.py)
- [Argo](https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/histogram.yaml)

## Extract information of different physics objects into a ROOT file called myoutput.root. Creates histograms in the end.
- [Volumes used with the workflow](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_volume.py)
- [Argo](https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/poet_workflow.yaml)

## jetMETAnalysis workflow
- [Original](https://gitlab.cern.ch/alintulu/reana-demo-JetMETAnalysis)
- [Couler-in progress](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.py)
- [Argo-in progress](https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/jetsAnalysis.yaml)


