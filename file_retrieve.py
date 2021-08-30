# Task: https://github.com/cms-dpoa/cms-dpoa-getting-started/issues/78
# Couler version:
# retrieves files from cernopendata-client and and sorts them out

import couler.argo as couler
from couler.argo_submitter import ArgoSubmitter
from couler.core.templates.volume import VolumeMount, Volume
from couler.core.templates.volume_claim import VolumeClaimTemplate
from couler.core.syntax.volume import create_workflow_volume


def retrieve(volume_mount, id):
    '''Retrieves file with a list of files for certain id from cernopendata'''
    couler.run_container(
        image="cernopendata/cernopendata-client",
        args=["echo generating file in volume; cernopendata-client get-file-locations --recid " +
              str(id)+" --verbose | tee /mnt/vol/files_"+str(id)+".txt;"],
        command=["sh", "-c"],
        step_name="retrieve",
        volume_mounts=[volume_mount],
    )
    return 0


def file_handling():
    '''Creates 5 files that contain a list of file addresses. 
    Each file is equaly sized. Sorted with wanted file sizes.'''

    size = list()
    everyList = list()
    lines = list()

    f = open("/mnt/vol/files_6010.txt", "r")

    # gets all the file sizes and file information
    #  to a list from txt file line by line
    for x in f:
        size.append(int(x.split()[1]))
        lines.append(x)

    f.close()

    # splits list that contains file sizes to 5 equaly sized lists (does not mess up the order)

    # print(sum(size))
    # print(len(size))
    z = 0
    nLists = 0
    divLists = list()
    partSize = sum(size)/5

    while nLists < 5:

        partSizeList = list()

        while z < len(size):

            if sum(partSizeList) < partSize or not partSizeList:
                partSizeList.append(size[z])
                z += 1
            else:
                break

        # print(sum(partSizeList))
        # print(len(partSizeList))

        divLists.append(partSizeList)
        nLists += 1

    i = 0
    x = 0
    length = 0

    # Puts all the lines from file to the right lists using index
    # and the length of created 5 lists (divLists)
    while i < 5:

        osaList = list()
        length += len(divLists[i])
        while x < length:

            osaList.append(lines[x])
            x += 1

        everyList.append(osaList)
        i += 1

    y = 0

    # Writes the lists to 5 different .txt files in volume
    for x in everyList:
        file = open("/mnt/vol/files_6010_"+str(y)+".txt", "w")
        file.write(str(x))
        file.close()
        y += 1

    f = open("/mnt/vol/files_6010_0.txt", "r")
    print(f.read())


def opendata(id):
    '''creates volume and executes containers by calling functions (containers)'''
    volume = VolumeClaimTemplate("workdir")
    create_workflow_volume(volume)
    volume_mount = VolumeMount("workdir", "/mnt/vol")

    retrieve(volume_mount=volume_mount, id=id)
    couler.run_script(
        image="python:3",
        source=file_handling,
        step_name="sorting",
        volume_mounts=[volume_mount]
    )


opendata(6010)

submitter = ArgoSubmitter(namespace="argo")
couler.run(submitter=submitter)
