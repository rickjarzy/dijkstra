import pandas as pd
import numpy
import time


def polar_to_karth(input_phi, input_lam):
    """
    transforms polar koords to karthesian koordinates
    :param input_phi: phi in [°]
    :param input_lam: lam in [°]
    :return: a list with the karthesian representation of the polar koordinates
    """

    pi = numpy.pi
    R = 6356000  # middle earth radius - bezugsysteme

    phi = input_phi * (pi / 180)
    lam = input_lam * (pi / 180)
    x = R * numpy.sin(lam) * numpy.cos(phi)
    y = R * numpy.sin(lam) * numpy.sin(phi)
    z = R * numpy.cos(lam)

    return [x, y, z]


def get_s12(list_p1, list_p2):
    """
    calcuates the distance between two 3d points
    :param list_p1: list with x,y,z koords of P1
    :param list_p2: list with x,y,z koords of P2
    :return: distance between P1 and P2
    """

    s12 = numpy.sqrt((list_p1[0] - list_p2[0]) ** 2 + (list_p1[1] - list_p2[1]) ** 2 + (list_p1[2] - list_p2[2]) ** 2)

    return s12

def dijkstra(start_node, node_matrix, arc_list, input_desc):
    time_start = time.clock()
    v_s = start_node  # start node

    # {% 1 %} - Initialisierung Dijkstra  im Pseudocode
    print("\n- Beginn Dijkstra %s\n==========================" % input_desc)
    # initial start punkt settings
    # print(node_matrix)
    node_matrix["l_j"] = numpy.inf
    node_matrix["l"] = numpy.inf
    node_matrix.at[str(v_s), "l"] = 0
    node_matrix.at[str(v_s), "l_j"] = 0
    node_matrix.at[str(v_s), "T"] = True

    # print("Initial Node Matrix\n", node_matrix,"\n")

    cou = 1
    # {% 3 %} - iter as long there are elements in the Temp node list
    while (node_matrix["T"] == True).any():

        #print("\nDurchlauf %s - Sind True werte drinnen" % str(cou))

        # {% 4 %} - select node with minimal label in Temp - (in the beginning the starting point)
        node_matrix_temp_true_subset = node_matrix[node_matrix["T"] == True]
        # print("\n- nodematrix subset\n", node_matrix_temp_true_subset, "\n")
        current_node_index = node_matrix_temp_true_subset.index[
            node_matrix_temp_true_subset["l_j"] == min(node_matrix_temp_true_subset["l_j"])][0]

        # select current label and neighbours
        current_node_label = node_matrix.loc[str(current_node_index)]["l_j"]
        neighbour_list = node_matrix.loc[str(current_node_index)]["neighbour_arc"]

        # print("- current Node index : %s" % str(current_node_index))
        # print("- current node label: ", current_node_label)
        # print("- current node %s - neighour list " % str(current_node_index), neighbour_list)

        # {% 5 %} - set the current node permanent and eliminate it from the Temp list
        node_matrix.at[str(current_node_index), "T"] = False
        node_matrix.at[str(current_node_index), "P"] = True

        # {% 6 %} - iter over neighbours
        for neighbour in neighbour_list:

            neighbour_node_id = int(arc_list.loc[str(neighbour)]["neighbour"])
            costs = arc_list.loc[str(neighbour)]["cost"]

            # print("* neighbour: ", neighbour_node_id, " - costs: ", costs)

            # {% 7 %} - if the neighbour node is not in the temp or permanent list
            if (node_matrix.loc[str(neighbour_node_id)]["T"] == False) and (
                    node_matrix.loc[str(neighbour_node_id)]["P"] == False):
                # print("*   if clause 1 - neighbour_id %s - current_id %s" % (str(neighbour_node_id), str(current_node_index)))
                # {% 8 %} - if the neighbour node is neither in the Temp list nor the Permanent list label them with their aerc
                # costs and set the current node as their predecessor
                node_matrix.at[str(neighbour_node_id), "l"] = node_matrix.at[str(current_node_index), "l"] + costs
                node_matrix.at[str(neighbour_node_id), "l_j"] = node_matrix.loc[str(neighbour_node_id)]["l"]
                node_matrix.at[str(neighbour_node_id), "p_j"] = current_node_index

                # update predecessor list - collects node ids from start to end point
                # node_matrix.at[str(neighbour_node_id), "pred_list"].append(current_node_index)
                # {% 9 %} - set neighbour nodes of current node Temp so the loop walks an to another node
                node_matrix.at[str(neighbour_node_id), "T"] = True

            # {% 10 %} if neighbour node from current node vi is allready in the temp list, we will check if his label needs an update due to cheaper costs otherwise it will stay the same
            if (node_matrix.loc[str(neighbour_node_id)]["T"] == True) and (
                    node_matrix.loc[str(neighbour_node_id)]["l"] > node_matrix.loc[str(current_node_index)]["l"] + costs):
                # print("*   if clause 2 - neighbour_id %s - current_id %s" % (str(neighbour_node_id), str(current_node_index)))
                node_matrix.at[str(neighbour_node_id), "l"] = node_matrix.at[str(current_node_index), "l"] + costs
                node_matrix.at[str(neighbour_node_id), "l_j"] = node_matrix.loc[str(neighbour_node_id)]["l"]
                node_matrix.at[str(neighbour_node_id), "p_j"] = current_node_index

                # update predecessor list - collects node ids from start to end point
                # node_matrix.at[str(neighbour_node_id), "pred_list"].append(current_node_index)

        # print(node_matrix)
        # if cou == 4:
        #    break
        cou += 1

    print(node_matrix)
    print("- ellapsed time: ", time.clock()-time_start, " [sec]")
    return node_matrix


def create_data_matrix(input_node_list_txt, input_arc_list_txt, input_node_koords_txt, input_home_node, cost_column=2):

    """
    Creates the node_matrix and arc_list that are needed to serve the dijkstra algorithm for its labeling tasks
    :param input_node_list_txt: path to the node.txt file
    :param input_arc_list_txt: path to the arc.txt file
    :param input_node_koords_txt: path to the txt file with the polar coordinates
    :param input_home_node:  polar coorindates of my hometowm
    :param cost_column: integer which tells the arclist algo which cost column from the txt file should be used in the dijkstra
    :return: node_matrix and arc_list as pandas dataframe
    """

    cmd_strings = ["node_id", "time", "distance", "speed limit", "clazz", "flags", "own"]
    N = list()  # nachbarschaftsliste
    arc_list = dict()  # adjazente arcliste - beschreibt welcher arc ZU welchem folgeknoten läuft
    node_matrix = dict()  # dictionary with vertices id as key and list of successors IDs as value
    # read out the node list, which contains the info how many arcs lead to successors from the point v_i
    with open(input_node_list_txt) as node_file:
        print("- Read out file %s %s" % (input_node_list_txt, cmd_strings[cost_column-1]))
        for line in node_file:
            line = line.split("\n")[0]
            N.append(int(line))
        #print(N)
        # create a node list dict that contains the point_id as key and the arc ids in a  list, that point to the successors in the
        # direct neigbourhood
        for node_list_element in range(0, len(N) - 1, 1):
            # print("Node %s has %s arcs that lead to successors" % (node_list_element+1, N[node_list_element+1] - N[node_list_element]))
            # print([ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)])
            node_matrix[str(node_list_element + 1)] = {
                "neighbour_arc": [arc_index for arc_index in range(N[node_list_element], N[node_list_element + 1], 1)],
                "l": 0,  # permanent label
                "p_j": False,   #predecessor
                "T": False,     # temp status
                "P": False,     # permanent status
                "l_j": 0,       # temp label
                "phi": 0,       # polar kooridnate phi from txt nodepl file
                "lam": 0,       # polar koordinate lam form txt nodepl file
                "geom_dist": 0, # geom distance between the karthesian representations of the polar kooridnates and my home
                }  # temp label

        node_matrix = pd.DataFrame.from_dict(node_matrix).T



    # read out the adjacent_list, which contains info which arc leads to which successor and the cost info
    with open(input_arc_list_txt) as arc_file:
        cou = 1
        print("- Read out file %s %s" % (input_arc_list_txt, cmd_strings[cost_column-1]))
        for line in arc_file:
            # print("cou: ", cou)
            data = line.split("\n")[0].split()
            #print("\n\n data", data)

            if cost_column == 7:
                # if the line is a line with the flag 2,4,6,7 ( all bike or pedestrian flags) speed up the time in the file by dividing it
                # with 100. so the bike and pedestrian have a better "time" (lower) wich should be favored by the dijkstra algorithm
                #print("- ",int(data[5]))
                arc_list[str(cou)] = dict({"neighbour": int(data[0]), "cost": float(data[1]) if int(data[5]) in [2,4,6,7] else float(data[1])*100, "pre": None})

            else:
                arc_list[str(cou)] = dict({"neighbour": int(data[0]), "cost": float(data[cost_column]), "pre": None})
            # print(arc_list[str(cou)])
            cou += 1

    arc_list = pd.DataFrame.from_dict(arc_list).T
    arc_list["neighbour"].astype(numpy.int16)

    # now we know how many arcs and which (arc_ids) point from the v_i to its successors
    # now do i need the predecessor info in the pandas frame or is it okay to store it seperatly for the algorithm?

    #print("\n- arc_list:\n==============\n", arc_list)

    with open(input_node_koords_txt) as koords_file:
        print("- Read out file %s %s" % (input_node_koords_txt, cmd_strings[cost_column-1]))
        cou = 1
        for line in koords_file:
            data = line.split("\n")[0].split()

            phi_txt = float(data[0])
            lam_txt = float(data[1])
            node_matrix.at[str(cou), "phi"] = phi_txt
            node_matrix.at[str(cou), "lam"] = lam_txt
            node_matrix.at[str(cou), "geom_dist"] = get_s12( polar_to_karth(phi_txt, lam_txt), polar_to_karth(input_home_node[0], input_home_node[1]) )

            #print("\n\nkoords: ",data)
            #print(node_matrix.loc[str(cou)])
            #print(node_matrix.loc[str(cou)]["phi"])
            cou += 1

    #print("\n- node_matrix:\n==============\n", node_matrix)
    return node_matrix, arc_list

def create_testdata_matrix(input_node_list_txt, input_arc_list_txt):

    print("\n- read out test data\n==================")
    N = list()  # nachbarschaftsliste
    arc_list = dict()  # adjazente arcliste - beschreibt welcher arc ZU welchem folgeknoten läuft
    node_matrix = dict()  # dictionary with vertices id as key and list of successors IDs as value
    # read out the node list, which contains the info how many arcs lead to successors from the point v_i
    with open(input_node_list_txt) as node_file:

        for line in node_file:
            line = line.split("\n")[0]
            N.append(int(line))
        print(N)
        # create a node list dict that contains the point_id as key and the arc ids in a  list, that point to the successors in the
        # direct neigbourhood
        for node_list_element in range(0, len(N) - 1, 1):
            # print("Node %s has %s arcs that lead to successors" % (node_list_element+1, N[node_list_element+1] - N[node_list_element]))
            # print([ arc_index for arc_index in range(N[node_list_element], N[node_list_element+1],1)])
            node_matrix[str(node_list_element + 1)] = {
                "neighbour_arc": [arc_index for arc_index in range(N[node_list_element], N[node_list_element + 1], 1)],
                "l": 0,  # permanent label
                "p_j": False,
                "T": False,
                "P": False,
                "l_j": 0,
                "pred_list": []}  # temp label

        node_matrix = pd.DataFrame.from_dict(node_matrix).T
        #print("\n- node_matrix:\n==============\n", node_matrix)
    # read out the adjacent_list, which contains info which arc leads to which successor and the cost info
    with open(input_arc_list_txt) as arc_file:
        cou = 1
        for line in arc_file:
            # print("cou: ", cou)
            data = line.split("\n")[0].split("\t")
            arc_list[str(cou)] = dict({"neighbour": int(data[0]), "cost": int(data[1]), "pre": None})
            # print(arc_list[str(cou)])
            cou += 1

    arc_list = pd.DataFrame.from_dict(arc_list).T

    arc_list["neighbour"].astype(numpy.int16)

    # now we know how many arcs and which (arc_ids) point from the v_i to its successors
    # now do i need the predecessor info in the pandas frame or is it okay to store it seperatly for the algorithm?

    #print("\n- arc_list:\n==============\n", arc_list)

    return node_matrix, arc_list


def find_route(end_point, node_matrix):
    last_node_data = node_matrix.loc[str(end_point)]
    pred_id = last_node_data["p_j"]
    way_points = [end_point]  # list that stores the nodes from the end to start point
    phi_koords = [node_matrix.loc[str(end_point)]["phi"]]
    lam_koords = [node_matrix.loc[str(end_point)]["lam"]]
    #print("- Last Node Data\n", last_node_data)
    #print("- Last Node Predecessor ID: ", pred_id)
    while pred_id:
        #print("pred_id: ", pred_id)
        way_points.append(pred_id)
        next_node_data = node_matrix.loc[str(pred_id)]  # get the node data from the node_matrix to select the next predecessor
        phi_koords.append(next_node_data["phi"])
        lam_koords.append(next_node_data["lam"])
        pred_id = next_node_data["p_j"]

    return way_points, phi_koords, lam_koords