import math
import matplotlib.pyplot as plt
import sys
from scipy import stats

ren_data_file = "MCRL_metis_RD.txt"
num_nodes_list = []
adj_edges_list = []
color_list = []
partitions = ['2','4','8','16','32','64','128']
colors = ['b','g','r','c','m','y','k','w']
with open(ren_data_file,"r") as rdf:
    header = rdf.next() 
    for line in rdf:
        #nodes, edges = line.rstrip().split() 
        nodes, edges, partition = line.rstrip().split()
        #col_index = partitions.index(partition) 
        #color_list.append(colors[col_index])
        #print line
        #if math.log(float(nodes)) == 0:
        # 	continue
        #remove from macaque cortex
        #if math.log(float(nodes)) > 4.5:
        # 	continue
        #
        num_nodes_list.append(math.log(float(nodes)))
        adj_edges_list.append(math.log(float(edges)))

slope, intercept, r_value, p_value, std_err = stats.linregress(num_nodes_list,adj_edges_list)
sys.stdout.write("Slope = Rentian Exponent = %s\n"%slope)
regress_line = [slope*i+intercept for i in num_nodes_list] 
#fig, ax = plt.subplots()
ax = plt.subplot(111)
ax.tick_params(axis="y",direction="in")
ax.tick_params(axis="x",direction="in")

ax.plot(num_nodes_list,adj_edges_list,'r*',num_nodes_list,regress_line)
#ax.legend(loc='bottom right')
#plt.plot(num_nodes_list,adj_edges_list,'r*')
slope_text = "p = " + str(slope)[0:4]
plt.xlabel('log(n)',fontsize=20)
plt.ylabel('log(c)',fontsize=20)
plt.title('Mouse Connectivity Rentian Scaling',fontsize=26)

nodes = 777
edges = 100084
modules = 510
txtstr = textstr = '\n'.join((
    r'p = %.2f' % (slope, ),
    r'nodes = %d' % (nodes, ),
    r'edges = %d' % (edges, ),
    r'modules = %d' % (modules, )))
ax.text(0.6, 0.35, textstr, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', horizontalalignment='left',bbox=dict(facecolor='none',edgecolor='black',pad=8.0))
#ax.text(2.5,5.5,slope_text,fontsize=14)

plt.show()
