import numpy
import dijkstra_functions
node_list_txt = r'nodelist.txt'#r"testdata/nodelist.txt"
arc_list_txt = r'arclist.txt'#r"testdata/arclist.txt"

start_node = 2395
end_node = 78
cost_column = 3 # selects the cost column that is read out

node_matrix, arc_list = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, cost_column)
node_matrix = dijkstra_functions.dijkstra(start_node,end_node, node_matrix, arc_list)

print("\nFind way points\n======================")
last_node_data = node_matrix.loc[str(end_node)]
pred_id = last_node_data["p_j"]
way_points = [end_node]     # list that stores the nodes from the end to start point


print("\nLast Node Data\n", last_node_data)
print("Last Node Predecessor ID: ", pred_id)
while pred_id:
    print("pred_id: ", pred_id)
    way_points.append(pred_id)
    next_node_data = node_matrix.loc[str(pred_id)]    # get the node data from the node_matrix to select the next predecessor
    pred_id = next_node_data["p_j"]


print(way_points)
print("Programm ENDE")