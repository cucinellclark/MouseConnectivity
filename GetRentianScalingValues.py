import sys
import numpy as np

commfile = "MCRL_metis.txt"
edgefile = "MCRL_edges.txt"
renfile = "MCRL_metis_RD.txt"

#scale = 1
edge_dict = {}
with open(edgefile,"r") as e:
    for line in e:
        head, tail, weight = line.rstrip().split()
        #head, tail = line.rstrip().split()
        if head not in edge_dict:
            edge_dict[head] = []
        if tail not in edge_dict:
            edge_dict[tail] = []
        if tail not in edge_dict[head]:
            edge_dict[head].append(tail)
        if head not in edge_dict[tail]:
            edge_dict[tail].append(head)

with open(commfile,"r") as c:
    comm_dict = {}
    partition = "0"
    for line in c:
        if line[0] == "#": #new partition
            line = line.rstrip().split("=")
            partition = line[1].rstrip()
            comm_dict[partition] = {}
            continue
        node, comm = line.rstrip().split()
        if comm not in comm_dict[partition]:
            comm_dict[partition][comm] = []
        comm_dict[partition][comm].append(node)

with open(renfile,"a+") as r:
    r.write("Number_Nodes\tNumber_Edges\tPartitions\n")
    for partition in comm_dict: 
        for comm_num in comm_dict[partition]:
            comm_edges = comm_dict[partition][comm_num]
            adjacent_num = 0
            for edge in comm_edges:
                if edge not in edge_dict:
                    continue
                adjacent = np.setdiff1d(edge_dict[edge],comm_edges)   
                adjacent_num = adjacent_num + len(adjacent)
            r.write("%s\t%s\t%s\n"%(len(comm_edges),adjacent_num,partition)) 
