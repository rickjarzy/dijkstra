import numpy
import os
import pandas as pd

node_list_txt = r"testdata/nodelist.txt"
arc_list_txt = r"testdata/arclist.txt"

N = list()
T = list()
P = list()
arc_list = dict()
node_list = dict()
# read out the node list, which contains the info how many arcs lead to successors from the point v_i
with open(node_list_txt) as node_file:

    for line in node_file:
        line = line.split("\n")[0]
        N.append(int(line))
    print(N)
    # create a node list dict that contains the point_id as key and the arc id as list, that oint to the successors in the
    # direct neigbourhood
    for node_list_element in range(0,len(N)-1,1):
        print("Node %s has %s arcs that lead to successors" % (node_list_element+1, N[node_list_element+1] - N[node_list_element]))
        print([ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)])
        node_list[str(node_list_element+1)] = [ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)]
    print(node_list)
#read out the adjacent_list, which contains info which arc leads to which successor and the cost info
with open(arc_list_txt) as arc_file:
    cou = 1
    for line in arc_file:
        #print("cou: ", cou)
        data = line.split("\n")[0].split("\t")
        arc_list[str(cou)] = dict({"suc":int(data[0]), "cost":int(data[1]), "pre":None})
        #print(arc_list[str(cou)])
        cou += 1

adj_list = pd.DataFrame.from_dict(arc_list).T

# now we know how many arcs and which (arc_ids) point from the v_i to its successors
# now do i need the predecessor info in the pandas frame or is it okay to store it seperatly for the algorithm?

print(adj_list)




print("Programm ENDE")