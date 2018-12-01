import pandas as pd
import numpy

node_list_txt = r"testdata/nodelist.txt"
arc_list_txt = r"testdata/arclist.txt"

N = list()      # nachbarschaftsliste
T = list()      # Temp Liste
P = list()      # Permanent Liste
arc_list = dict()       #adjazente arcliste - beschreibt welcher arc ZU welchem folgeknoten läuft
node_matrix = dict()      # dictionary with vertices id as key and list of successors IDs as value
# read out the node list, which contains the info how many arcs lead to successors from the point v_i
with open(node_list_txt) as node_file:

    for line in node_file:
        line = line.split("\n")[0]
        N.append(int(line))
    print(N)
    # create a node list dict that contains the point_id as key and the arc ids in a  list, that point to the successors in the
    # direct neigbourhood
    for node_list_element in range(0,len(N)-1,1):
        #print("Node %s has %s arcs that lead to successors" % (node_list_element+1, N[node_list_element+1] - N[node_list_element]))
        #print([ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)])
        node_matrix[str(node_list_element+1)] ={"neighbour_arc": [ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)],
                                              "l": 0,       # permanent label
                                              "p_j": False,
                                              "T": False,
                                              "P": False,
                                              "l_j": 0}     #temp label

    node_matrix = pd.DataFrame.from_dict(node_matrix).T
    print("\n- node_matrix:\n==============\n", node_matrix)
#read out the adjacent_list, which contains info which arc leads to which successor and the cost info
with open(arc_list_txt) as arc_file:
    cou = 1
    for line in arc_file:
        #print("cou: ", cou)
        data = line.split("\n")[0].split("\t")
        arc_list[str(cou)] = dict({"neighbour":int(data[0]), "cost":int(data[1]), "pre":None})
        #print(arc_list[str(cou)])
        cou += 1

arc_list = pd.DataFrame.from_dict(arc_list).T

arc_list["neighbour"].astype(numpy.int16)

# now we know how many arcs and which (arc_ids) point from the v_i to its successors
# now do i need the predecessor info in the pandas frame or is it okay to store it seperatly for the algorithm?

print("\n- arc_list:\n==============\n", arc_list)

v_s = 1         # start vertices

# {% 1 %} - Initialisierung Dijkstra  im Pseudocode
print("\n- Beginn Dijkstra")

# initial start punkt settings
print(node_matrix)
node_matrix["l_j"] = numpy.inf
node_matrix["l"] = numpy.inf
node_matrix.at[str(v_s), "l"] = 0
node_matrix.at[str(v_s), "l_j"] = 0
node_matrix.at[str(v_s), "T"] = True


print("Initial Node Matrix\n", node_matrix,"\n")

cou = 1
#{% 3 %} - iter as long there are elements in the Temp node list
while (node_matrix["T"] == True).any():

    print("\nDurchlauf %s - Sind True werte drinnen" %str(cou))

    #{% 4 %} - select node with minimal label in Temp - (in the beginning the starting point)
    node_matrix_temp_true_subset = node_matrix[node_matrix["T"] == True]
    #print("\n- nodematrix subset\n", node_matrix_temp_true_subset, "\n")
    current_node_index = node_matrix_temp_true_subset.index[node_matrix_temp_true_subset["l_j"] == min(node_matrix_temp_true_subset["l_j"])][0]

    # select current label and neighbours
    current_node_label = node_matrix.loc[str(current_node_index)]["l_j"]
    neighbour_list = node_matrix.loc[str(current_node_index)]["neighbour_arc"]

    print("- current Node index : %s" % str(current_node_index))
    print("- current node label: ", current_node_label)
    print("- current node %s - neighour list " % str(current_node_index), neighbour_list)

    #{% 5 %} - set the current node permanent and eliminate it from the Temp list
    node_matrix.at[str(current_node_index), "T"] = False
    node_matrix.at[str(current_node_index), "P"] = True

    #{% 6 %} - iter over neighbours
    for neighbour in neighbour_list:

        neighbour_node_id = int(arc_list.loc[str(neighbour)]["neighbour"])
        costs = arc_list.loc[str(neighbour)]["cost"]

        print("* neighbour: ", neighbour_node_id, " - costs: ", costs)

        #{% 7 %} - if the neighbour node is not in the temp or permanent list
        if (node_matrix.loc[str(neighbour_node_id)]["T"] == False) and (node_matrix.loc[str(neighbour_node_id)]["P"] == False):
            print("*   if clause 1 - neighbour_id %s - current_id %s" % (str(neighbour_node_id), str(current_node_index)))
            #{% 8 %} - if the neighbour node is neither in the Temp list nor the Permanent list label them with their aerc
            # costs and set the current node as their predecessor
            node_matrix.at[str(neighbour_node_id), "l"] = node_matrix.at[str(current_node_index), "l"]+costs
            node_matrix.at[str(neighbour_node_id), "l_j"] = node_matrix.loc[str(neighbour_node_id)]["l"]
            node_matrix.at[str(neighbour_node_id), "p_j"] = current_node_index
            #{% 9 %} - set neighbour nodes of current node Temp so the loop walks an to another node
            node_matrix.at[str(neighbour_node_id), "T"] = True

        if (node_matrix.loc[str(neighbour_node_id)]["T"] == True) and (node_matrix.loc[str(neighbour_node_id)]["l"] > node_matrix.loc[str(current_node_index)]["l"] + costs):
            print("*   if clause 2 - neighbour_id %s - current_id %s" % (str(neighbour_node_id), str(current_node_index)))
            node_matrix.at[str(neighbour_node_id), "l"] = node_matrix.at[str(current_node_index), "l"] + costs
            node_matrix.at[str(neighbour_node_id), "l_j"] = node_matrix.loc[str(neighbour_node_id)]["l"]
            node_matrix.at[str(neighbour_node_id), "p_j"] = current_node_index


    print(node_matrix)
    if cou == 2:
        break
    cou += 1



print("Programm ENDE")