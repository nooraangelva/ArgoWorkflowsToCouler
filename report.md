# **Summer 2021 internship documentation - Noora Angelva**


# Intro
This is in a way a report and a study journal for myself on my summer doing an internship at CERN.

I will go through the steps that it takes to set up Couler, explain troubles while creating examples and also showcasing the examples. Also I have some general information over Argo, Couler and some coding tips for workflows and for general coding that I picked up over the summer.



# 1. Couler

**Couler** provides a unified interface for constructing and managing workflows on different workflow engines, such as Argo Workflows, Tekton Pipelines, and Apache Airflow. The **venv** provides support for creating lightweight virtual environments.
## 1.1 Set up

You can either use **your laptop** or **LXPLUS8** as a virtual environment.


**Local:**
1. Install [kubectl to linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) if you do not already have it

**LXPLUS8:**
	kubectl is available on lxplus8.cern.ch
1.	log in: ssh username@lxplus8.cern.ch

**Both:**
2.	create or move the config file to lxplus8.cern.ch or your laptop
- If you want to create the config file to lxplus8 or for some reason to your computer, just write ```nano config``` and copy paste the contents to it. then press ```ctrl+O``` then ```Enter``` and ```ctr+X```.
3. the environment variable ```KUBECONFIG``` needs to point to the config file.
- For example: export ```KUBECONFIG=/Users/clange/config```
- In order to be able to use the config file
-	You can get the path to the file with: ```realpath config```

4.	Try ```kubectl get nodes``` to check if this works
- it should list a few nodes starting with argo-cluster-ex7mwvnbnl52-

The first part did not cause any errors and went smoothly for me. 
- If you want to create the config file to lxplus8 or for some reason to your computer, just write ```nano config``` and copy paste the contents to it. then press ```ctrl+O``` then ```Enter``` and ```ctr+X```.

5. You need to use ```python3``` from now on. If you don’t have it install it with this command: 

```shell
sudo apt-get update
sudo apt-get install python3.8 python3-pip
```

### Instructions to install venv and Couler:

1. execute the following commands in a folder where you want it to be stored
```shell
mkdir couler
cd couler
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install git+https://github.com/couler-proj/couler
```

2. You will only need to do that once. Then every time you are in a new shell/terminal:
```shell
cd couler
source .venv/bin/activate
```


**The result:**
![](https://codimd.web.cern.ch/uploads/upload_99cba9c2f9e2a70ed60eadb292935156.png)

**To run Couler code:**
1. Create a .py file
2. In the (.venv) state. run it with: ```python3 [filename].py```



**Errors while installing:**
1. If ```python3 -m  venv .venv``` provides an error where it can’t find the python3.6-venv even if try to install it with ```sudo apt-get install python3.6-venv``` and try again.
**Or**
use rather the following code: 
```sudo apt-get install virtualenv, virtualenv .venv```

2. If Pip doesn’t work and/or you get the error “Bad handshake”, SSLError.
Try the following codes:
```shell 
git clone -q https://github.com/couler-proj/couler.git
python3 setup.py install
```



## 1.2 Examples from Couler's repository

Basic examples from Couler repository README.md

-	[Coinflip-example](https://github.com/couler-proj/couler/blob/master/examples/coin_flip.py)
-	[hello-world](https://github.com/couler-proj/couler/blob/master/examples/hello_world.py)
-	[Dag](https://github.com/couler-proj/couler/blob/master/examples/dag.py)

- More examples are in [gitlab](https://github.com/nooraangelva/ArgoWorkflowsToCouler)

**To run Couler code:**
1. Create a .py file
2. In the (.venv) state. run it with: ```python3 [filename].py```

## 1.3 My Own Examples

I took some examples from the [Argo](https://argoproj.github.io/argo-workflows/examples/) documentation and implemented them in the Couler format. The implementations are available in [GitHub](https://github.com/nooraangelva/ArgoWorkflowsToCouler) in the [READMeE.md](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/README.md) there are links to the implementations (.py) and to the original argo examples. Workflows that Couler has created and submitted can be seen in your [Argo UI](https:// "2. Argo") in a Argo version once you have ran the code. You can also see logs of the workflow there easily. you can also see them from the terminal if you rather prefer that.


### Coinflip-recursive

coinflip-recursive is a variation of the coinflip example.This is an example of a dynamic workflow which extends indefinitely until it acheives a desired result. In this example, the 'flip-coin' step is recursively repeated until the result of the step is "heads".

[Couler version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip-recursive.py)
[Argo version](https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip-recursive.yaml)

**Result in Argo UI:**
![](https://codimd.web.cern.ch/uploads/upload_a68371a6fc4db1383bb44a6e32565a2e.png)

![](https://codimd.web.cern.ch/uploads/upload_3a81af10427975fa24dbb78211053687.png)


### Hello world

Echos Hello world. One step workflow.

[Couler version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip-recursive.py)
[Argo version](https://github.com/argoproj/argo-workflows/blob/master/examples/coinflip-recursive.yaml)

**Result in Argo UI:**

![](https://codimd.web.cern.ch/uploads/upload_71b5c849960ba8881b67fc5093e8d8f4.png)


**Logs:**
![](https://codimd.web.cern.ch/uploads/upload_87994c59739d4b36b95fd83639459d8b.png)

### Diamond-dag-steps
Showcases how to make the steps dependent on other steps.

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/dag-diamond-steps.py)
[Argo](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)

**Results in Argo UI:** 

![](https://codimd.web.cern.ch/uploads/upload_b4b46cddfb8fc0f2014cefc6270314b8.png)

### Exit handler

The code intentionaly fails so that it does the exit handler that deals with errors in the workflow..

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/exit_handler_test.py)
[Argo](https://github.com/argoproj/argo-workflows/blob/master/examples/exit-handlers.yaml)

**Results in Argo UI:** 

![](https://codimd.web.cern.ch/uploads/upload_5b4d1eedd14aeba050d6008060f8e979.png)


**Logs:**
![](https://codimd.web.cern.ch/uploads/upload_86bf11bba15466de7a8b992b95a0b035.png)
![](https://codimd.web.cern.ch/uploads/upload_ce4301bd7d7989897701bab64ce45513.png)

### Volumes

Creates a file and opens it using volumes. 
Had the [Bug 1](https:// "Bug 1:") problem but found a fix.

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/volumes.py)
[Argo](https://github.com/argoproj/argo-workflows/blob/master/examples/volumes-pvc.yaml)

**Results in Argo UI:** 


**Logs:**
![](https://codimd.web.cern.ch/uploads/upload_0549f94b6dd83278dd6efc03ec31e147.png)

### Map

Loops through a list and gives a function a parameter from the list several lists. 

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/map.py)
[Argo](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)

**Results in Argo UI:** 

![](https://codimd.web.cern.ch/uploads/upload_9c173b83916e276493fdae051086d7eb.png)


**Logs:**
![](https://codimd.web.cern.ch/uploads/upload_04eeacf1b496b241e767dc42a7515d78.png)


### Map Diamond

Loops through a list and calls a function and gives it a parameter from the list. Creates a diamond shape with dependencies.
I have the [Bug 2](https:// "Bug 2:") 

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/map_diamond.py)
[Argo](https://github.com/argoproj/argo-workflows/blob/master/examples/dag-diamond-steps.yaml)

**Results in Argo UI:** 

![](https://codimd.web.cern.ch/uploads/upload_be05dee8fa391d537f002362c843da76.png)


**Logs:**

![](https://codimd.web.cern.ch/uploads/upload_b6ef6e5be48a2b4d6d74116bdf07b393.png)

### File handling with volumes

I used `cernopendata-client` to get a file with a list of files and their sizes and sorting them to 5 different equally sized files with a list of files.

[Task](https://github.com/cms-dpoa/cms-dpoa-getting-started/issues/78)
[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/file_retrieve.py)


**Results in Argo UI:** 

![](https://codimd.web.cern.ch/uploads/upload_feebebb962e9781dae4b4280d14131ad.png)

**Logs:**

Showcases the retrieved files and the long list of file addresses in one created file.(Too long to put a picture.)

### Clemens' workflow

[Argo](https://gist.github.com/clelange/067c21c402f5a898de90d8b91e165a18)

**(24.6.2021)**
Working on it ...

**(31.8.2021)**
Had to stop working on the Couler version since there has been no fix in sight for the following bug. (scatter with multiple steps.)
[Bug](https:// "Bug 6:")
 
[The whole workflow in .yaml (Argo)](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/histogram.yaml)

### Simplified two step version of the [POET](https:// "2.4 PhysObjectExtractorTool (POET) workflow")
[The whole workflow in .yaml (Argo)](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/histogram.yaml)
[The whole workflow in .py (Couler)](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/histogram.py)

Two step workflow:

- first producing a slimmer version of the original open data (running in the CMS open data container) 
- second analysing the output file (running in a container with "ROOT" data analysis package). 

**First step:**

[explanation about the step's code and usage by the creators](https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool#objects-information-extractor-tool)
- I used the image: ```cmsopendata/cmssw_5_3_32:latest```

**First step script:**
```
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
```

- At the end I copy the ```myoutput.root``` to ```volumeMount```.

**Reminder!**
the first command after ```bash``` needs to be ```source /opt/cms/entrypoint.sh```. Because of an entry bug.

**Second step:**

[explanation about the step's code by the creators](https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool/tree/master/PhysObjectExtractor/test)

The second step uses two different ways to create a histogram from the file that was created in the previous step. 

- Use 6.22 version of ROOT, you will not be able to compile POET_test.cxx with some earlier versions (for example cmsopendata/cmssw_5_3_32)

- I used image: ```nooraangelva/cmssw:10_6_12-argo-v2```

- Two paralel steps are in the step.



**1.1 step script:**

```
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
```

**1.2 step script:**
```
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
```

## 1.4 Errors 

### **Error 1: Workflows were submited to "default" namespace which set the workflows  to a pending state indefinetly.**

**The Solution:**

You can easily deside the namespace you want the workflow to go by adding it to the submitter in the code:

```submitter = ArgoSubmitter(namespace="[your namespace]")```


### **Error 2: Couler doesnt't seem to support all of it's functions**

Erros such as the on in the picture below have slowed down working with Couler. It seems like the Couler library is missing stuff. The below is an example from Couler project. [couler functions](https://github.com/couler-proj/couler/blob/master/docs/couler-api-design.md)

![](https://codimd.web.cern.ch/uploads/upload_c566a80c71c4b3e98b1fb71672ee1d07.png)

![](https://codimd.web.cern.ch/uploads/upload_7d178c13f919f15f82099645f24e490b.png)

**Solution:**
Make sure you are importing from the right address.

example:
```
from couler.core.syntax.loop import map
import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
```
### Error 3: 
**Failed: ```cannot unmarshall spec: unrecognized type: string```**

[Diamond-dag-steps](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/dag-diamond-steps.py)

**Solution:**
I started from the beginning with the code. Referenced the [Dag-Diamond](https://github.com/couler-proj/couler/blob/master/examples/dag.py)


## 1.5 Bugs

### Bug 1: 

**had problems opening the created file in second step - Obsolete problem now.**

[Volumes - example](https:// "Volumes")
[Same issue found in github](https://github.com/couler-proj/couler/issues/193#)

**Solution:**
Temporary solution, offical solution will be published soon to the main couler branch

[Solution link](https://github.com/couler-proj/couler/issues/193#issuecomment-843550006)

Install Peini Lius branch when using couler.

```pip install git+https://github.com/peiniliu/couler.git```

**Update (26.5.21):**
The solution has been merged to the main branch.

### Bug 2: 

```Map()```  **Doesn't work when trying to use dependencies or dag. Then only executes the function ones.**

[Couler](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/map_diamond.py)

![](https://codimd.web.cern.ch/uploads/upload_da497b66a7da1d826b2f84cbe18e8104.png)



**Solution:**

No solution as of yet.

### Bug 3: 

**Argo UI refusing to connect when trying to access https://localhost:2746/workflows**


**Solution:**

Microsoft 10 has a default fast start up feature that creates a glitch if you want to access localhost. Doesn't affect restart.

https://github.com/microsoft/WSL/issues/5298#issuecomment-636665289

### Bug 4: 

**Couler only supports** ```accessModes: [ "ReadWriteOnce" ]``` **by default. You would have to change the Couler code to make it dynamic or to even change the default.

[Fix](https:// "1. improvement: Making volumeclaim dynamic")

**(24.6.2021)**
I have made a PR for the problem and it has been aproved and merged to the main branch.

### Bug 5:
Couler only supports one argument in ```couler.map()```, which is a list of values that can be called by the specified function.

It prevents me from executing scatter properly.


**(25.6.2021)**
I have made a PR and I'm now waiting for it to be merged to the main branch.

### Bug 6: 
`Map()` (scatter in Argo) only works when you use one function/container. It doesn’t work when trying to create a step with scatter which contains dag: tasks: [the troublesome part of the code](https://gist.github.com/clelange/067c21c402f5a898de90d8b91e165a18#file-bsm-search-yaml-L132-L141)

Similar issues:
- [Issue 1](https://github.com/couler-proj/couler/issues/217 )
- [issue 2](https://github.com/couler-proj/couler/issues/220)


Might be a tricky one to develop for me...

### Bug 7: 

`secret` doesn't work in Couler unless you create it jut before using it and set `dry_run=true` when creating the secret. 

Creating the secret works.

[Issue](https://github.com/couler-proj/couler/issues/231)


## 1.6 development of Couler



### 1. improvement: Making volumeclaim dynamic

- [Bug 4](https:// "Bug 4")
- [Issue](https://github.com/couler-proj/couler/issues/210)
- [PR](https://github.com/couler-proj/couler/pull/212)

Troubles during the development: 

1. [windows row change includes the solution also](https://stackoverflow.com/questions/29045140/env-bash-r-no-such-file-or-directory/29045187)
```sed $'s/\r$//' scripts/integration_tests.sh > scripts/integration_tests.Unix.sh```
Probably because of windows system.

2. Changing the wrong username from my first commit. The username was schools gitlab username. Because of that I couldn't sign the CLA.
```
git stash
git rebase -i {{the last good commit before the bad one}}
git commit --amend
# changed the username and email from the file
git push -f
```

### 2. improvement: Map() to take several *arg

- [Bug 5](https:// "Bug 5")
- [Issue](https://github.com/couler-proj/couler/issues/32)
- [PR](https://github.com/couler-proj/couler/pull/215)
- The first [fix](https://github.com/couler-proj/couler/pull/169/commits/f194c294c330086b67867115513fef2c1212dc88) didn't work. 

**Reason why the first fix didn't work:**
The change just pretty much loops the arguments in the ```map()```.

```return map(map(function, input_list), *other)```

But the return value is a ```Step Class``` not a function so the first ```map()``` will succeed but not the second one or the third... because the ```map()``` checks the function first. 

```inner_step = Step(name=inner_dict["id"], template=template_name)```

```return inner_step```

![](https://codimd.web.cern.ch/uploads/upload_46c1d5a1fd1b186b77fe76826764f4ba.png)


**[Final version](https://github.com/couler-proj/couler/pull/215/commits/6f831b4eb404ed278cbe09f3dd89c95dada2a717)**

**Uses ```*args```**
**```def map(function, input_list, *other):```**

First I started modifying the loop.py to a dynamic form. I modified the syntax checkers that made sure the function, map-function and arguments were valid and in the right format. I had made a loop that saves the the number of arguments and the first values of the list, so i didn't have to change the template creation code. 

Then I just created a loop to save the parameters in blocks.

creates the parameters using two ```while``` loops
- ```def map(function, *other):```
- loops through the lists one index at a time. 
- inner loop: ```other[x][0], other[x][0]...```
- Outer loop: ```other[0][y], other[0][y]...```

### 3. improvement: Possibility to use an existing secret

- [Issue](https:// "Bug 7")
- [PR](https://github.com/couler-proj/couler/pull/235)


# 2. Argo workflows
![](https://codimd.web.cern.ch/uploads/upload_4b5cb99ca8212d903af354c7bc613e8f.png)
## 2.1 Argo explained



Argo Workflows is an open source container-native workflow engine for orchestrating parallel jobs on Kubernetes. 

[.yaml example explained](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/coinflip.yaml)

![](https://codimd.web.cern.ch/uploads/upload_3933a1e77960efdc62a4a1ad2f3f1bb3.png)



## 2.2 Argo UI

https://argoproj.github.io/argo-workflows/argo-server/

1. Start minikube and start argo server. You will find it in: https://localhost:2746/
```shell
minikube start
argo server
```

![](https://codimd.web.cern.ch/uploads/upload_8359a09ad4f17d90d4d0ff6d59c35e79.png)


 
I had a [bug](https:// "Bug 3"), but now Argo UI works nicely.

## 2.3 Argo's Workflows

### submiting a workflow

For submitting Argo workflows from the terminal:

 ```argo submit -n argo --log cron-workflow.yaml #shows the logs also```
 
``` --log``` shows what happens in the workflow when executing it.
 
Resubmiting a workflow
 
*  A Workflow execution has been completed, and you would like to submit it again. Essentially an alias for running argo submit again.

Reruning a workflow

* Rerun a failed Workflow. The same Workflow object is re-run and all of the steps that failed or errored are marked as pending and then executed as normal. No new Workflows are created.

### Suspend and continue workflow on failure

Failing a workflow and then continuing it. 
1. Adding ```continueOn:``` true to the step in question. 
2. Adding a ```suspend step``` afterwards conditioned on it failing 

**First version** not the most practical requires manual writing. 
[first version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/suspend.yaml)

![](https://codimd.web.cern.ch/uploads/upload_8c08251916ca0a9ad67c05b59f9538dd.png)


**Troubled version**:

The implementation did not work straight forwardly. I added the ContinueOn and exitHandler the result kept being the following:
```ExitHandler``` with suspend worked, but the next step did not get executed after resume. ```ContinueOn``` worked but it did not take account the ```exitHandler``` and continued straight to the next step.
[Troubled version](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/suspend-bad.yaml)

![](https://codimd.web.cern.ch/uploads/upload_195edd2253299f87c558f1b0fac44db6.png)


 
## 2.4 jet energy calibrations .YAML

[Yadage version used in REANA](https://gitlab.cern.ch/alintulu/reana-demo-JetMETAnalysis)

The task was to create a .yaml to be used in Argo from [Adelinas JetMETAnalysis](https://gitlab.cern.ch/alintulu/reana-demo-JetMETAnalysis).

- The parameters for the can be found [here](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/inputs.yaml)
- The Workflow [here](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/workflow.yam)
- The steps to the workflow [here](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml)


![](https://codimd.web.cern.ch/uploads/upload_c5033ef1885c2dc4734a0ab8151cf3cd.png)

**Right now the workflow works until apply-l1 step.**

**Good to know:**
```
stages:
  - name: get_conditions
    dependencies: [init]
    scheduler:
      scheduler_type: singlestep-stage
      parameters:
        sample_id: {step: 'init', output: sample_id}
        pileup: '{workdir}/pileup'
        conditions: '{workdir}/conditions'
        cmssw_release: '{workdir}/cmssw_release'
      step: {$ref: workflow/steps.yaml#/get_conditions}
```
- ```depencies:``` is the same as in ```.yaml```
- ```Scheduler_type:``` describes if it scatters or not.
- ```parameters:``` same idea as in ```.yaml``` just a different way to write them. Can be found in the [input file](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/inputs.yaml)
- ```Step: ``` tells the source for the step. Can be found in the [step file](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml)

Because the platform was changed from ```REANA``` to ```Argo``` we decided to use ```volumes``` to store the data, because ```Argo``` doesn't save data the same way as ```REANA```. Then they would be easily accessible to all the ```steps``` without creating a ```parameter``` mess.

This part of the code was replaced by the next snippet of code since it was outdated and to take account the usage of containers.
```
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd $(cat {work_dir})
eval `scramv1 runtime -sh`
```

```
cp /mnt/vol/krb5cc_1000 /tmp
#sudo ls -a /mnt/vol
KRB5CCNAME=FILE:/mnt/vol/krb5cc_1000 

source /opt/cms/cmsset_default.sh
cd $HOME/CMSSW_10_6_12/src
eval `scramv1 runtime -sh
````


1. Step: **get-conditions-name**
First workflow step ```get-conditions-template``` was created easily. The data was saved to volumes as ```.txt files```
[Step code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L481-L501)

2. Creating docker image for the workflow
Second workflow step ```create-PU-dist-template``` 
We created a new [```docker image: nooraangelva/cmssw:10_6_12-argo-v2``` ](https://hub.docker.com/repository/docker/nooraangelva/cmssw)

Commands for its creation:
- ```git clone ssh://git@gitlab.cern.ch:7999/nangelva/reana-demo-JetMETAnalysis.git ``` to create the ```image: alintulu/cmssw:10_6_12-argo```
- ```alintulu/cmssw:10_6_12-argo``` was build with the cmd: ```docker build . -t alintulu/cmssw:10_6_12-argo``` (while being in the ```reana-demo-JetMETAnalysis``` -folder so )
- ```docker build -f Dockerfile-input -t alintulu/cmssw:10_6_12-argo-v2``` Dockerfile-input was added to adelinas image.

**Script inside the ```Dockerfile-input```:**
```
# Parent image CentOS7 with CVMFS embedded
# CMSSW: 10_6_12
# SCRAM ARCH: slc7_amd64_gcc700
FROM alintulu/cmssw:10_6_12-argo

USER cmsusr

# Add code
ADD /input $HOME/input

ENTRYPOINT []
```

- Then the image was pushed to dockerhub so that Argo could use it:
```
sudo docker login
sudo docker image build -t nooraangelva/cmssw:10_6_12-argo-v2 .
sudo docker push nooraangelva/cmssw:10_6_12-argo-v2
```
3. Step: create-PU-dist

The created image was used as a container image.

[Steps code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L503-L520)



4. Creating a secret for login details

[Input files from the cloud](https://cernbox.cern.ch/index.php/s/RLhpdYwRZiRKCJ3) 
- FlatPU/JRA_101.root
- FlatPU/JRA_102.root
- EpsilonPU/JRA_1.root
- EpsilonPU/JRA_10.root

We needed to get files from the cloud in the workflow so Adelina came up with the following command: 
```
scp nangelva@lxplus.cern.ch:/eos/user/a/adlintul/REANA/RunIISummer19UL18/$FILE .
```

The problem was that I needed rights to it. Adelina gave them to me. The next problem was that I needed to login if I wanted to download the files.

So I created a secret key to be used in the workflow. 
with these [cmds](http://docs.reana.io/advanced-usage/access-control/kerberos/#generating-keytab-file):


```
# login to lxplus and generate keytab file
$ ssh nangelva@lxplus.cern.ch
$ ktutil
ktutil:  add_entry -password -p nangelva@CERN.CH -k 1 -e aes256-cts-hmac-sha1-96
Password for nangelva@CERN.CH:
ktutil:  add_entry -password -p nangelva@CERN.CH -k 1 -e arcfour-hmac
Password for nangelva@CERN.CH:
ktutil:  write_kt .keytab
ktutil:  exit

# Let's test generated keytab file by trying to generate Kerberos ticket
$ scp nangelva@lxplus.cern.ch:~/.keytab .
$ kinit -kt ~/.keytab nangelva@CERN.CH
$ klist
Ticket cache: FILE:/tmp/krb5cc_1000
Default principal: nangelva@CERN.CH

Valid starting       Expires              Service principal
04/29/2019 11:24:12  04/30/2019 12:23:52  krbtgt/CERN.CH@CERN.CH
  renew until 05/04/2019 11:23:52
04/29/2019 11:24:49  04/30/2019 12:23:52  host/tweetybird04.cern.ch@CERN.CH
  renew until 05/04/2019 11:23:52
04/29/2019 11:25:00  04/30/2019 12:23:52  host/bigbird14.cern.ch@CERN.CH
  renew until 05/04/2019 11:23:52
```


When I created a kerberos keytab following the instructions above, I needed to copy it to my local directory.

```scp nangelva@lxplus.cern.ch:.keytab .```


I added the kerberos keytab as a secret to my kubernetes cluster (the cluster which is running on my minikube and which can run argo on) after I encoded it [Link to the referenced code](https://kubernetes.io/docs/tasks/configmap-secret/managing-secret-using-kubectl/)

```
cat .keytab | base64 -w 0 > .keytab_encoded
kubectl create secret generic adelina --from-file=.keytab_encoded -n argo
kubectl get secrets
```

The result should look something like this:
```
NAME                  TYPE                                  DATA   AGE
adelina               Opaque                                1      39h
default-token-vrzxr   kubernetes.io/service-account-token   3      33d
```
How to see the secret key:
```kubectl get secret adelina -o yaml -n argo```

Result:
```
apiVersion: v1
data:
  keytab.txt: QlFJQUFBQkdBQUVBQjBjgglORlVrNHVRMGdBQ0c1aGJtZGxiSFpoQUFBQUFXRFRQLzBCQUJJQUlGNnhpM0xDRCs1eTFORmVtSjM2NlgzZklrVXBabmdiNVRHUYCcW5TWUJFZThSQUFBQUFRQUFBRFlBQVFBSFEwVlNUaTVEU0FBSWJtRnVaMlZzZG1FQUFBQUJZTk0vL1FFQUZ3QVFqR3JpYmhiUVNMR1E3SFhnRnRib0xBQUFBQUU9
kind: Secret
metadata:
  creationTimestamp: "2021-06-30T12:54:31Z"
  name: adelina
  namespace: argo
  resourceVersion: "574854"
  uid: 0238a1b3-0e38-4b42-9392-9435928ee2fe
type: Opaque
```
Decode the result:
```
echo <keytab.txt text> | base64 -d
```

5. how to use a secret

**A small example on how to use secret:**

Create simple .yaml printing a secret
[not working .yaml example](https://github.com/argoproj/argo-workflows/blob/master/examples/secrets.yaml)

**When creating the secret in the example remeber to define the namespace!**

```
kubectl create secret generic my-secret --from-literal=mypassword=S00perS3cretPa55word -n argo
```
6. Step: reana-access

[Steps code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L522-L549)

Next I implemented my own secret to Adelina's workflow step.

I created a file in the volumes for a decoded .keytab-secret. 

```
# this decodes the keytab
cat .keytab | base64 -d
```
The step will use image: ```nooraangelva/reana-auth-krb5```. So that the next steps have access to it.
The argo job would have the following lines: 
```
kinit -k -t /secret/mountpath/.keytab nangelva@CERN.CH 
id
klist
ls -l /tmp/krb5cc_1000
cp /tmp/krb5cc_1000 /mnt/vol
```

Using this command: ```kinit -k -t .keytab nangelva@CERN.CH```, would create user 0 a "superuser" and that woudn't work when retrieving information from the cloud, because ...

Dockerfile:

```
FROM reanahub/reana-auth-krb5:1.0.1

RUN  groupadd --gid 1000 cmsusr && useradd --uid 1000 --gid 1000 -G root cmsusr

WORKDIR /home/cmsusr
USER cmsusr
ENV USER cmsusr
ENV HOME /home/cmsusr
```
The bellow won't work because the -g is ambigious:
```groupadd -g 1000 cmsusr && adduser -u 1000 -g 1000 -G root cmsusr complains about -g```


This creates a kerberos token which we can move to a volume mount. And other jobs can read from said volume mount and with access to the kerberos token they can read files from the EOS folder.

7. Testing of the kereberos token

[Adelina's directions to testing in a docker container](https://codimd.web.cern.ch/diu_WRhMThOb7pLrFArTJw?view)
Testing it straight in a docker container:
```
docker run --rm -it -v $PWD:/temp nooraangelva/cmssw:10_6_12-argo-v2 /bin/bash
cp /mnt/vol/krb5cc_1000 /tmp
KRB5CCNAME=FILE:/mnt/vol/krb5cc_1000 
klist
source /opt/cms/cmsset_default.sh
cd $HOME/CMSSW_10_6_12/src
eval `scramv1 runtime -sh`
root -b root://eosuser.cern.ch//eos/user/a/adlintul/REANA/RunIISummer19UL18/FlatPU/JRA_100.root
# above works as suppose to
#bellow not
scp nangelva@lxplus.cern.ch:/eos/user/a/adlintul/REANA/RunIISummer19UL18/FlatPU/JRA_101.root .
```

The code for testing in Argo:
```
cp /mnt/vol/krb5cc_1000 /tmp
KRB5CCNAME=FILE:/mnt/vol/krb5cc_1000 
klist
source /opt/cms/cmsset_default.sh
cd $HOME/CMSSW_10_6_12/src
eval `scramv1 runtime -sh`

# the path:
root -b root://eosuser.cern.ch//eos/user/a/adlintul/REANA/RunIISummer19UL18/FlatPU/JRA_100.root
```
Result:
![](https://codimd.web.cern.ch/uploads/upload_5a78005ba67f1a067f8252d943594f48.png)

8. Step: produce-ntuple-list-lumi

This script is responsible for creating the Ntuples.

Starting from a larger data format, a preliminary filter is applied in order to extract only the information useful for our specfic need. This step produces the so called Ntuples, which can be analysed much faster than complete data files. For AODSIM and MINIAOD the creation is performed with tools implemented in the CMSSW software.

[The Step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L80)
[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L551-L593)

using my docker image: ```nooraangelva/cmssw:10_6_12-argo-v2```

using the token in the container: ```cp /mnt/vol/krb5cc_1000 /tmp
        KRB5CCNAME=FILE:/mnt/vol/krb5cc_1000 ```

There were no real problems when the [file checking part](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L93-111) was deleted as unnessecary.

9. Step: produce-ntuple-match-lumi

This script takes the list from previous step and returns a YAML file with one value containing {batch_size} number of paths to pileup files, as well as every no pileup file that contains they same lumisections as those files. As a result we have successfully clustered the pileup files into batches while simultaneously storing a list of all no pileup files with the same lumisections.

[The step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L80)
[the code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L595-L623)

using my docker image: ```nooraangelva/cmssw:10_6_12-argo-v2```

There were no problems with this step.

10. Step: 
Generating a dynamic scatter creator that also divides the matched file list

[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L625-L672)


11. Step: produce-ntuple-match-jets
Matching the jets

This script matches events between two samples, and then matches the reconstructed jets between those two samples based on particle level. The primary reason for this is to calcualte the difference in pT between a jet that is in an environment where pileup was simulated and the exact same jet when there is no pileup. This tells us the offset or in other words the amount of pileup added to the jet.


[The step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L145)
[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L674-L750)

PU-dist-data is not created in the [create-PU-dist step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L61) -> so it can be found in the image. In the following adress.

```
- name: PU-dist-data                                   
      value: "/home/cmsusr/input/PileupHistogram-goldenJSON-13tev-2018-69200ub-100bins.root"
```

I removed the sleeping part since the scatter step works and creates parallel jobs.
I changed the file list to .txt from .yaml so getting the addresses had to be modified.

12. Step: compute-l1

This script is responsible for computing the L1FastJet jet energy corrections. The goal is to determine how offset over area changes with jet pT and rho. The computed offset can then be removed. A function is fitted to a TGraph2D and the fit becomes a single line in the output text file.

[The step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L208)
[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L752-L797)


13. Step: Scatter-2

Uses the same code as the previous scatter only its result is different the code checks which way to execute its self.

[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L625)

14. Step: apply-l1

This script allows you to apply a set of jet energy corrections. Every uncorrected jet collection in the input tree(s) will be corrected according to the levels parameter, while corrected jet collections will be skipped. The parameter levels is a list of correction levels to be applied, such as L1(FastJet), L2(Relative) and L3(Absolute).

[The step](https://gitlab.cern.ch/nangelva/reana-demo-JetMETAnalysis/-/blob/master/workflow/steps.yaml#L242)
[The code](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/jetsAnalysis.yaml#L799-L844)

Right now the code fails here. Possibliy the name for the  file in hadd is in wrong format or its contents.



## 2.5 PhysObjectExtractorTool (POET) workflow
[For CMS Open Data Workshop 2021](https://github.com/cms-legacydata-analyses/PhysObjectExtractorTool/tree/master/PhysObjectExtractor)

Retrieve a subset of file for processing to a slimmer format with PhysObjectExtractorTool (POET), process them one file/job, merge and create a test histogram of the processed file.
 
- [Volumes used with the workflow](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_volume.py)
- [Argo](https://github.com/argoproj/argo-workflows/blob/4e450e250168e6b4d51a126b784e90b11a0162bc/examples/poet_workflow.yaml)


![](https://codimd.web.cern.ch/uploads/upload_f870af806c479a441db302309cfe9309.png)



You can adjust the input variables wich control what recid is to be used, how many files, which files and how manyevent to do when handling them.

 ``` arguments:
    parameters:
    - name: processName                                  
      value: 'DoubleMuParked'
    - name: firstFile                                  
      value: 10
    - name: nFiles                               
      value: 4
    - name: nEvents                               
      value: 100
    - name: recid
      value: 6004
```

**Steps:**
**1. prepare**
prepare the data directories needed in the workflow steps
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L86-L96)
**2. write-step**
 Getting the files of the wanted recid and cleaning the list up to only wanted files from it
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L99-L124)

**3. generate**
generate the iterator list for the scatter step
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L127-L140)
**4. scatter-step**
do the processing
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L143-L187)
**5. merge-step**
merge the files from the scatter steps to a single file
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L190-L216)
**6. event-loop-analysis**
prepare some histograms to check the merged output file
[Step](https://github.com/nooraangelva/ArgoWorkflowsToCouler/blob/main/poet_workflow.yaml#L219-L240)



# 3 Docker
![](https://codimd.web.cern.ch/uploads/upload_d008561b9e73e47778c7b23ffbca14d5.png)

A software framework for building, running, and managing containers on servers and the cloud


## 3.1 Errors

1. Docker update made it not work anymore on wsl2 and all the images dissapeared from docker. So minikube is not working.
**What to do to solve it:**
Restart computer and re-install update.

# 4 Conclusion

## 4.1 The summer

I started my internship in May. I was at CERN for four months. My instructors were Clemens Lange and Kati Lassila-Perini. I worked on Workflows and I was especially tasked with Couler. Mostly creating or at least trying to create different kinds of examples with it. I did also a few workflows with Argo in .yaml form. One of the workflows was for a workshop.

The first month was challenging. I had not really worked with python or yaml before. I also had never really created workflows and the concept was a bit mysterious at first. In Uni I had mostly just created web applications and games so just focusing on the data and how to handle it efficiently was a new exiting territory.

Slowly I started to understand Couler and why it is smart to use workflows when handling data in certain way often. I mean why use two hours to run code and make sure it succeeds when you can just invent the cycle once and just run the codes automatically and faster.

I didn't really create any codes that process the given data but I created the containers (enviroments) where the codes where programs where run and made the datas trip from one program to the next smooth troubless.



## 4.2 Workflows in general

A Workflow is a sequence of tasks that processes a set of data. Workflows occur across every kind of business and industry. Anytime data is passed between humans and/or systems, a workflow is created. Workflows are the paths that describe how something goes from being undone to done, or raw to processed.

**Process workflow**

A process workflow happens when the set of tasks is predictable and repetitive. This means that before an item begins the workflow, you know exactly what path it should take.

Business process workflows are set up to handle an unlimited number of items going through them. An example is a purchase requisition approval workflow. As soon as it starts, the workflow is set with few variations, and you can process any number of items in a single workflow.

## 4.3 impressions on Couler

Couler aims to provide a unified interface for constructing and managing workflows on different workflow engines, such as Argo Workflows, Tekton Pipelines, and Apache Airflow.

Couler is basically a GitHub project that is still very much in development. I have created a few PR requests for Couler to help develop it. Still it's biggest downfall is the missing feature scatter. Couler has a very simple version of it, but it does not support a scatter that has multiple steps. Which is required in quite a few workflows to optimize the data prosessing. 

There are also other features that are still in kids shoes. I hope that in the near future it will start being developed in a faster pace than now. The scatter feature PR was recently closed with out merging  so I'm not getting my hopes up.
# 5 Useful stuff
## 5.1 Coding Checklist

1.	Indentations
2.	logical code progression
3.	Structuring
4.	Naming – that makes sense
5.	Typos
6.	Comments
    a.	Grammar
    b.	Typos
    c.	Proper sentences
    d.	Understandability
    e.	In English
    f.	Do you even have them?
    g.	At the beginning explanation of the code
    h.	Do functions have explanations?
7.	Debugging – When ready take them out, only then!
8.	Have you tested the right code?
9.	Tested the whole thing not just parts?
10.	Tested it also in parts, when in dev

## 5.2 Memory control tips

Delete only completed workflows: ```argo delete --completed``` 
Change the default namespace: ```kubectl config set-context --current --namespace=<insert-namespace-name-here>```
Clean completed pods, pvs and pvcs: ```kubectl delete pod --field-selector=status.phase==Succeeded -n argo```

**Correct order of cleaning up:**

Clear the pods: ```kubectl delete pod --all -n argo```
Clear the pvcs: ```kubectl delete pvc --all -n argo```
CLear the pvs:  ```kubectl delete pv --all -n argo```

If you have trouble cleaning up delete two line lines:
```
finalizers:
  -  kubernetes.io/pv-protection
  ```
  
```kubectl edit persistentvolume/pvc-521d9a78-dba4–11e8-b576–12241a2479c2```
Exit vim: ```Esc > Shift + ZZ```


## 5.3 Cheat Sheats

[Kubernetes](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

kubectl cp  pv-pod:/mnt/data poddata -n argo
