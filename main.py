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

cost_column = 2 # selects the cost column that is read out

# create node matrix and arc list
node_matrix, arc_list = dijkstra_functions.create_data_matrix(node_list_txt, arc_list_txt, node_koords_txt, home_node, cost_column)

#shows node id with the nearest distance
start_node_temp = node_matrix.loc[node_matrix["geom_dist"] == min(node_matrix["geom_dist"])]
print("start node: \n", start_node_temp)

# create labeled graph with dijkstra algorithm
node_matrix = dijkstra_functions.dijkstra(start_node, node_matrix, arc_list)

print("\nFind way points\n======================")
print("Find route to Ikea: ")
ikea_route_pred, ikea_phi, ikea_lam = dijkstra_functions.find_route(end_node_ikea, node_matrix)
print("ikea number of nodes: ", len(ikea_route_pred))

print("\nFind route to Sattler: ")
sattler_route_pred, sattler_phi, sattler_lam = dijkstra_functions.find_route(end_node_sattler, node_matrix)
print("sattler number of nodes: ", len(sattler_route_pred))

print("Find route to Klettergarten Weinzödl: ")
kletter_route_pred, kletter_phi, kletter_lam = dijkstra_functions.find_route(end_node_kletter, node_matrix)
print("kletter number of nodes: ", len(kletter_route_pred))

plt.figure()
plt.plot( node_matrix["lam"],node_matrix["phi"], 'bx', markersize=12)
plt.plot(home_node[1], home_node[0], color='red', marker='*', markersize=22)
plt.plot([15.4457347], [47.1327090], color='green', marker='*', markersize=22)
plt.plot(ikea_lam, ikea_phi, 'y-', markersize=22, linewidth=5)
plt.plot(sattler_lam, sattler_phi, 'm-', markersize=22, linewidth=5)
plt.plot(kletter_lam, kletter_phi, 'c-', markersize=22, linewidth=5)
plt.show()

print("Programm ENDE")