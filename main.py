# -*- coding: utf-8 -*-
# Navigations Systems lab 1 WS18/19
# 0031430
# Paul Arzberger
from matplotlib import pyplot as plt
import dijkstra_functions
import numpy


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
# create node matrix and arc list with distance
node_matrix_distance, arc_list_distance = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, node_koords_txt, home_node, 2)
# create node matrix and arc list with own
node_matrix_own, arc_list_own = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, node_koords_txt, home_node, 7)

#shows node id with the nearest distance
start_node_temp = node_matrix_time.loc[node_matrix_time["geom_dist"] == min(node_matrix_time["geom_dist"])]
print("start node: \n", start_node_temp)
print("phi: ",start_node_temp["phi"].values[0],"\nlam: ", start_node_temp["lam"].values[0], "\ndistance: ", start_node_temp["geom_dist"])# <----- there I got my node ID for the nearest Node

# create labeled graph with dijkstra algorithm
node_matrix_time = dijkstra_functions.dijkstra(start_node, node_matrix_time, arc_list_time, "Time")
node_matrix_distance = dijkstra_functions.dijkstra(start_node, node_matrix_distance, arc_list_distance, "Distance")
node_matrix_own = dijkstra_functions.dijkstra(start_node, node_matrix_own, arc_list_own, "Own")
print("\nFind way points\n======================")

# TIME
# ========
print("Find time_route to Ikea: ")
ikea_route_pred, ikea_phi_time, ikea_lam_time , distance_list_ikea_time = dijkstra_functions.find_route(end_node_ikea, node_matrix_time)
print("ikea number of nodes: ", len(ikea_route_pred))
print("costs ikea route time: ", node_matrix_time.loc[str(end_node_ikea)]["l"]*60, " [min]")
dijkstra_functions.write_phi_lam_txt(ikea_phi_time,ikea_lam_time,"Ikea_time")
print("Data Distance Ikea route Time: ", sum(distance_list_ikea_time), " [km]")

print("\nFind time_route to Sattler: ")
sattler_route_pred, sattler_phi_time, sattler_lam_time, distance_list_sattler_time = dijkstra_functions.find_route(end_node_sattler, node_matrix_time)
print("sattler number of nodes: ", len(sattler_route_pred))
print("costs sattler route time: ", node_matrix_time.loc[str(end_node_sattler)]["l"]*60, " [min]")
dijkstra_functions.write_phi_lam_txt(sattler_phi_time,sattler_lam_time,"Sattler_time")
print("Data Distance Sattler route Time: ", sum(distance_list_sattler_time), " [km]")

print("Find time_route to Klettergarten Weinzödl: ")
kletter_route_pred, kletter_phi_time, kletter_lam_time, distance_list_kletter_time = dijkstra_functions.find_route(end_node_kletter, node_matrix_time)
print("kletter number of nodes: ", len(kletter_route_pred))
print("costs Klettergarten route time: ", node_matrix_time.loc[str(end_node_kletter)]["l"]*60, " [min]")
dijkstra_functions.write_phi_lam_txt(kletter_phi_time,kletter_lam_time,"Kletter_time")
print("Data Distance Klettergarten route Time: ", sum(distance_list_kletter_time), " [km]")
# DISTANCE
# ===========

print("\nFind distance_route to Ikea: ")
ikea_route_pred_distance, ikea_phi_distance, ikea_lam_distance, distance_list_ikea_distance = dijkstra_functions.find_route(end_node_ikea, node_matrix_distance)
print("ikea number of nodes: ", len(ikea_route_pred_distance))
print("costs IKEA route distance: ", node_matrix_distance.loc[str(end_node_ikea)]["l"])
dijkstra_functions.write_phi_lam_txt(ikea_phi_distance,ikea_lam_distance,"Ikea_distance")
print("Data Distance Ikea route distance: ", sum(distance_list_ikea_distance), " [km]")

print("Find distance_route to Sattler: ")
sattler_route_pred_distance, sattler_phi_distance, sattler_lam_distance, distance_list_sattler_distance = dijkstra_functions.find_route(end_node_sattler, node_matrix_distance)
print("sattler number of nodes: ", len(sattler_route_pred_distance))
print("costs Sattler route distance: ", node_matrix_distance.loc[str(end_node_sattler)]["l"])
dijkstra_functions.write_phi_lam_txt(sattler_phi_distance,sattler_lam_distance,"Sattler_distance")
print("Data Distance Sattler route distance: ", sum(distance_list_sattler_distance), " [km]")

print("Find distance_route to Klettergarten Weinzödl: ")
kletter_route_pred_distance, kletter_phi_distance, kletter_lam_distance, distance_list_kletter_distance = dijkstra_functions.find_route(end_node_kletter, node_matrix_distance)
print("kletter number of nodes: ", len(kletter_route_pred_distance))
print("costs Klettergarten route distance: ", node_matrix_distance.loc[str(end_node_kletter)]["l"])
dijkstra_functions.write_phi_lam_txt(kletter_phi_distance,kletter_lam_distance,"Kletter_distance")
print("Data Distance Kletter route distance: ", sum(distance_list_kletter_distance), " [km]")
# OWN
# ===========

print("\nFind own_route to Ikea: ")
ikea_route_pred_own, ikea_phi_own, ikea_lam_own, distance_list_ikea_own = dijkstra_functions.find_route(end_node_ikea, node_matrix_own)
print("ikea number of nodes: ", len(ikea_route_pred_own))
print("costs Ikea route own: ", node_matrix_own.loc[str(end_node_ikea)]["l"])
dijkstra_functions.write_phi_lam_txt(ikea_phi_own,ikea_lam_own,"Ikea_own")
print("Data Distance Ikea route own: ", sum(distance_list_ikea_own), " [km]")

print("Find own_route to Sattler: ")
sattler_route_pred_own, sattler_phi_own, sattler_lam_own, distance_list_sattler_own = dijkstra_functions.find_route(end_node_sattler, node_matrix_own)
print("sattler number of nodes: ", len(sattler_route_pred_own))
print("costs Sattler route own: ", node_matrix_own.loc[str(end_node_sattler)]["l"])
print("Data Distance Sattler route own: ", sum(distance_list_sattler_own), " [km]")
dijkstra_functions.write_phi_lam_txt(sattler_phi_own,sattler_lam_own,"Sattler_own")

print("Find own_route to Klettergarten Weinzödl: ")
kletter_route_pred_own, kletter_phi_own, kletter_lam_own, distance_list_kletter_own = dijkstra_functions.find_route(end_node_kletter, node_matrix_own)
print("kletter number of nodes: ", len(kletter_route_pred_own))
print("costs Klettergarten route own: ", node_matrix_own.loc[str(end_node_kletter)]["l"])
print("Data Distance Klettergarten route own: ", sum(distance_list_kletter_own), " [km]")
dijkstra_functions.write_phi_lam_txt(kletter_phi_own,kletter_lam_own,"Kletter_own")


plt.figure()
plt.plot(node_matrix_time["lam"], node_matrix_time["phi"], 'bx', markersize=3, label="Graph Nodes", alpha=0.3)
plt.plot(home_node[1], home_node[0], color='red', marker='*', markersize=15, label="Home Node Am Hohenberg")
plt.plot([15.4457347], [47.1327090], color='green', marker='*', markersize=15, label="Nearest Node Sundlweg")


# Time
plt.plot(ikea_lam_time, ikea_phi_time, 'y-', markersize=22, linewidth=5, label="Route IKEA - Time")
plt.plot(sattler_lam_time, sattler_phi_time, 'y-', markersize=22, linewidth=5, label="Route Sattler - Time")
plt.plot(kletter_lam_time, kletter_phi_time, 'y-', markersize=22, linewidth=5, label="Route Klettergarten - Time")
# Distance
plt.plot(ikea_lam_distance, ikea_phi_distance, 'm-.', markersize=22, linewidth=5, label="Route IKEA - Distance")
plt.plot(sattler_lam_distance, sattler_phi_distance, 'm-.', markersize=22, linewidth=5, label="Route Sattler - Distance")
plt.plot(kletter_lam_distance, kletter_phi_distance, 'm-.', markersize=22, linewidth=5, label="Route Klettergarten - Distance")
# Own
plt.plot(ikea_lam_own, ikea_phi_own, 'g:', markersize=22, linewidth=5, label="Route IKEA - Own")
plt.plot(sattler_lam_own, sattler_phi_own, 'g:', markersize=22, linewidth=5, label="Route Sattler - Own")
plt.plot(kletter_lam_own, kletter_phi_own, 'g:', markersize=22, linewidth=5, label="Route Klettergarten - Own")

plt.plot(node_matrix_time.loc[str(end_node_kletter)]["lam"], node_matrix_time.loc[str(end_node_kletter)]["phi"], color="black", marker='*', markersize=15, label="Endnode Weinzödl")
plt.plot(node_matrix_time.loc[str(end_node_sattler)]["lam"], node_matrix_time.loc[str(end_node_sattler)]["phi"], color='magenta', marker='*', markersize=15, label="Endnode Sattler")
plt.plot(node_matrix_time.loc[str(end_node_ikea)]["lam"], node_matrix_time.loc[str(end_node_ikea)]["phi"], color='cyan', marker='*', markersize=15, label="Endnode IKEA")
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
plt.title("Lab1 - Dijkstra Algorithm NavSys WS18/19")
plt.xlabel(r'lambda [°]')
plt.ylabel(r'phi [°]')
plt.xlim([15.32, 15.56])
plt.ylim([47.00, 47.16])
plt.yticks(numpy.arange(47.00, 47.16, 0.04), [str(x/100) for x in range(4700, 4716, 4)])
plt.xticks(numpy.arange(15.32, 15.60, 0.04), [str(x/100) for x in range(1532, 1560, 4)])

plt.grid(True)
plt.show()

print("Programm ENDE")