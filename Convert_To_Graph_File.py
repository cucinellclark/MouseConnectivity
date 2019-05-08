import sys
filename ="MouseConnectivityTable.csv"
outname = "MouseConnectivity_NoRL.txt"
with open(filename,"r") as f:
    header = f.next().rstrip().split(",")
    areas = header[5:]
    right_left = f.next().rstrip().split(",")[5:]
    areas[len(areas)-1] = areas[len(areas)-1].rstrip()
    ###UNCOMMENT BOTTOM TO ADD IDENTIFIERS
    index = 0
    for i in areas:
        areas[index] = i.rstrip()
        #areas[index] = i.rstrip()+"-"+right_left[index]
        index = index + 1
    ###
    outfile = open(outname,"w")
    for line in f:
        line = line.rstrip().split(",")
        index = 0
        for i in areas:
            weight = float(line[5+index])
            if weight > 0:
                outfile.write("%s %s %s\n"%(line[2],areas[index],format(weight,'.9f'))) 
            index = index + 1
    outfile.close()
