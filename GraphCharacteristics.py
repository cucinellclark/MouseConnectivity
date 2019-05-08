import networkx as nx
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
fname = "MCRL_edges.txt"

#What to calculate
AVERAGEPATH = False
DEGREE = False
COEFFICIENT = True
WEIGHTDISTRIBUTION = True

WEIGHTED = True

#Get graph info
minscale = 1.6
threshold = 1e-8
edges = []
nodes = []
weights = {}
maxweight = 0
with open(fname,"r") as f:
	header = f.next().rstrip()
	for line in f:
		info = line.rstrip().split()
		if float(info[2]) <= 0.0:
			continue
		edge = info[1]+","+info[0]
		if info[0] not in nodes:
			nodes.append(info[0])
		if info[1] not in nodes:
			nodes.append(info[1])
		if float(info[2]) > maxweight:
			maxweight = float(info[2])
		weight = -1*math.log10(float(info[2]))+minscale
		if edge not in weights:
			weights[edge] = []
		weights[edge].append(weight)
		#nedge = (info[0],info[1],weight)
		#edges.append(nedge)

#print(maxweight)
#sys.exit()

#Average edges
avg_weights = []
for key in weights:
	head, tail = key.split(",")
	weight = weights[key]
	weight_avg = np.sum(weight)/len(weight)
	avg_weights.append(weight_avg)
	if WEIGHTED:
		edges.append((head,tail,weight_avg))
		weights[key] = weight_avg
	else:
		edges.append((head,tail))

#SET UP GRAPH
G = nx.MultiGraph()
#G = nx.Graph()
#G.add_edges_from(edges) #unweighted
G.add_weighted_edges_from(edges)

#WEIGHT DISTRIBUTION
if WEIGHTDISTRIBUTION:
	mean_weight = np.mean(avg_weights)
	print(mean_weight)
	plt.hist(avg_weights)
	plt.xlabel("Normalized Edge Weights",fontsize=14)
	plt.ylabel("Edge Count",fontsize=14)
	plt.title("Normalized Edge Weight Distribution",fontsize=16)
	plt.show()

#AVERAGE PATHLENGTH
if AVERAGEPATH:
	path_sum = 0.0
	lengthlist = []
	for source in nodes:
		paths = nx.single_source_shortest_path(G,source)
		for path in paths:
			tail = source
			sourcesum = 0
			for node in paths[path]:
				if node != source:
					key = tail+","+node
					if key in weights:
						path_sum = path_sum + weights[key]
						sourcesum = sourcesum + weights[key]
					tail = node
			lengthlist.append(sourcesum)

	plt.boxplot(lengthlist,showfliers=True,vert=False)
	numNodes = len(nodes)
	avg_path = path_sum / (numNodes*(numNodes-1))
	mean_path = np.mean(lengthlist)
	print(mean_path)
	#print(avg_path)
	#avg_path = 10**(minscale-avg_path)
	plt.title('Path Length Distribution',fontsize=16)
	plt.yticks([],[])
	plt.xlabel('Normalized Path Length',fontsize=16)
	plt.show()
	#sys.exit()

#GET DEGREE DISTRIBUTION
if DEGREE:
	degrees = G.degree()
	degree_sum = 0
	degree_list = []
	for d in degrees:
		degree_sum = degree_sum + degrees[d]
		degree_list.append(degrees[d])
	avg_degree = degree_sum / len(nodes)
	print("average degree = " + str(avg_degree))
	plt.hist(degree_list)
	plt.xlabel("Degree of Node")
	plt.ylabel("Degree Count")
	plt.title("Node Degree Distribution")
	plt.show()

#Clustering coefficient
if COEFFICIENT:
	avg_cluster = nx.average_clustering(G)
	print("average cluster = " + str(avg_cluster))
	node_clusters = nx.clustering(G)
	cluster_list = []
	for node in node_clusters:
		cluster_list.append(node_clusters[node])
	plt.hist(cluster_list)
	plt.show()
