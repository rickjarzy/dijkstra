import pandas as pd
import numpy

node_list_txt = r"testdata/nodelist.txt"
arc_list_txt = r"testdata/arclist.txt"

N = list()      # nachbarschaftsliste
T = list()      # Temp Liste
P = list()      # Permanent Liste
arc_list = dict()       #adjazente arcliste - beschreibt welcher arc ZU welchem folgeknoten läuft
node_list = dict()      # dictionary with vertices id as key and list of successors IDs as value
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
        node_list[str(node_list_element+1)] ={"suc": [ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)],
                                              "l_j": 0, "p_j": None}
    node_list = pd.DataFrame.from_dict(node_list).T
    print("- node_list:\n==============\n", node_list)
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

print("- adj_list:\n==============\n", adj_list)

v_s = 1         # start vertices
T = [False] * len(node_list)

# {% 1 %} - Initialisierung Dijkstra  im Pseudocode
l_s = 0
T[v_s-1] = v_s      # setze startpunkt
P = dict()
V = node_list       # pandas dataframe

print("V: ", V)
# {% 2 %} -  Setze alle Labels für alle Knoten ausser des Startknoten auf unendlich


print("- T:\n==============\n", T)
print("- P:\n==============\n", P)



print("Programm ENDE")