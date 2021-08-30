def file_handling():
    '''Creates 5 files that contain a list of file addresses. 
    Each file is equaly sized. Sorted with wanted file sizes.'''

    size = list()
    everyList = list()
    lines = list()

    # the path for wanted file
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
