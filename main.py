# -*- coding: utf-8 -*-
from matplotlib import pyplot as plt
import dijkstra_functions


# with the implemented distance calculation the nearest node would be 5433 but 5432 would be the node with the
# id corresponding to the standard port of postgresql database servers - so i couldn resist to change the startnode to 5432
# 5432 47.1275197     15.3584347
# 5433 47.1327094     15.4457347

node_list_txt = r'nodelist.txt'#r"testdata/nodelist.txt"
arc_list_txt = r'arclist.txt'#r"testdata/arclist.txt"
node_koords_txt = r'nodepl.txt'
home_node = (47.1513825, 15.4476257)

# i read that from the command line output
start_node = 5433
end_node_ikea = 78
end_node_sattler = 3364
end_node_kletter = 963

#cost column
# 1 = time - h
# 2 = distance - km
# 3 = speed limit - km/h
# 4 = clazz
# 5 = flags


# create node matrix and arc list with time
node_matrix_time, arc_list_time = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, node_koords_txt, home_node, 1)

node_matrix_distance, arc_list_distance = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, node_koords_txt, home_node, 2)


#shows node id with the nearest distance
start_node_temp = node_matrix_time.loc[node_matrix_time["geom_dist"] == min(node_matrix_time["geom_dist"])]
print("start node: \n", start_node_temp)      # <----- there I got my node ID for the nearest Node

# create labeled graph with dijkstra algorithm
node_matrix_time = dijkstra_functions.dijkstra(start_node, node_matrix_time, arc_list_time, "Time")
node_matrix_distance = dijkstra_functions.dijkstra(start_node, node_matrix_distance, arc_list_distance, "Distance")
print("\nFind way points\n======================")

# TIME
# ========
print("Find time_route to Ikea: ")
ikea_route_pred, ikea_phi_time, ikea_lam_time = dijkstra_functions.find_route(end_node_ikea, node_matrix_time)
print("ikea number of nodes: ", len(ikea_route_pred))

print("\nFind time_route to Sattler: ")
sattler_route_pred, sattler_phi_time, sattler_lam_time = dijkstra_functions.find_route(end_node_sattler, node_matrix_time)
print("sattler number of nodes: ", len(sattler_route_pred))

print("Find time_route to Klettergarten Weinzödl: ")
kletter_route_pred, kletter_phi_time, kletter_lam_time = dijkstra_functions.find_route(end_node_kletter, node_matrix_time)
print("kletter number of nodes: ", len(kletter_route_pred))

# DISTANCE
# ===========

print("Find distance_route to Ikea: ")
ikea_route_pred_distance, ikea_phi_distance, ikea_lam_distance = dijkstra_functions.find_route(end_node_ikea, node_matrix_distance)
print("ikea number of nodes: ", len(ikea_route_pred_distance))

print("\nFind distance_route to Sattler: ")
sattler_route_pred_distance, sattler_phi_distance, sattler_lam_distance = dijkstra_functions.find_route(end_node_sattler, node_matrix_distance)
print("sattler number of nodes: ", len(sattler_route_pred_distance))

print("Find distance_route to Klettergarten Weinzödl: ")
kletter_route_pred_distance, kletter_phi_distance, kletter_lam_distance = dijkstra_functions.find_route(end_node_kletter, node_matrix_distance)
print("kletter number of nodes: ", len(kletter_route_pred_distance))

plt.figure()
plt.plot(node_matrix_time["lam"], node_matrix_time["phi"], 'bx', markersize=3, label="Graph Nodes")
plt.plot(home_node[1], home_node[0], color='red', marker='*', markersize=10, label="Home Node Am Hohenberg")
plt.plot([15.4457347], [47.1327090], color='green', marker='*', markersize=10, label="Nearest Node Sundlweg")
plt.plot(node_matrix_time.loc[str(end_node_ikea)]["lam"], node_matrix_time.loc[str(end_node_ikea)]["phi"], color='black', marker='*', markersize=10, label="Endnode IKEA")
plt.plot(node_matrix_time.loc[str(end_node_kletter)]["lam"], node_matrix_time.loc[str(end_node_kletter)]["phi"], color="black", marker='*', markersize=10, label="Endnode Weinzödl")
plt.plot(node_matrix_time.loc[str(end_node_sattler)]["lam"], node_matrix_time.loc[str(end_node_sattler)]["phi"], color='black', marker='*', markersize=10, label="Endnode Sattler")
# Time
plt.plot(ikea_lam_time, ikea_phi_time, 'y-', markersize=22, linewidth=5, label="Route IKEA - Time")
plt.plot(sattler_lam_time, sattler_phi_time, 'm-', markersize=22, linewidth=5, label="Route Sattler - Time")
plt.plot(kletter_lam_time, kletter_phi_time, 'c-', markersize=22, linewidth=5, label="Route Klettergarten - Time")
# Distance
plt.plot(ikea_lam_distance, ikea_phi_distance, 'y--', markersize=22, linewidth=5, label="Route IKEA - Distance")
plt.plot(sattler_lam_distance, sattler_phi_distance, 'm--', markersize=22, linewidth=5, label="Route Sattler - Distance")
plt.plot(kletter_lam_distance, kletter_phi_distance, 'c--', markersize=22, linewidth=5, label="Route Klettergarten - Distance")
plt.legend()
plt.title("Lab1 - Dijkstra Algorithm NavSys WS18/19")
plt.xlabel('lam [°]')
plt.ylabel('phi [°]')
plt.grid(True)
plt.show()

print("Programm ENDE")