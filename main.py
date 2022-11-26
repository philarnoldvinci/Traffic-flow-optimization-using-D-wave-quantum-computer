from TrafficFlowOptimization import TrafficFlowOptimization
import MapGraph
import networkx as nx
import matplotlib.pyplot as plt

row = int(input("Please enter the row of the graph ==> "))
column = int(input("Please enter the column of the graph ==> "))

G = MapGraph.make_graph(row, column)
MapGraph.add_traffic_weight(G)
MapGraph.add_time_travel(G)

pos = nx.spring_layout(G)
nx.draw_networkx(G, pos, with_labels=True)
plt.show()
MapGraph.print_map_graph_details(G)

print(f"The graph node is {G.nodes}")
origin_node = int(input("Please enter origin node ==> "))
destination_node = int(input("Please enter destination node ==> "))

print("The 3 shortest paths from the origin to the destination are shown below ....... ")
paths = MapGraph.find_tre_shortest_paths(G, origin_node, destination_node, overlap=5, weight="time travel")
path_edges = MapGraph.paths_edges(paths)

for i in path_edges:
    zaman = 0
    for s in i:
        u, v = s
        zaman += G[u][v]["time travel"]
    print(f'time travel of rout {i} is {int(zaman//60)}:{int(zaman%60)}')


nx.draw(G, pos, node_color='k', with_labels=True)
nx.draw_networkx_nodes(G, pos, nodelist=paths[0], node_color='g')
nx.draw_networkx_edges(G, pos, edgelist=path_edges[0], edge_color='g', width=10)
nx.draw_networkx_nodes(G, pos, nodelist=paths[1], node_color='r')
nx.draw_networkx_edges(G, pos, edgelist=path_edges[1], edge_color='r', width=10)
nx.draw_networkx_nodes(G, pos, nodelist=paths[2], node_color='b')
nx.draw_networkx_edges(G, pos, edgelist=path_edges[2], edge_color='b', width=10)
plt.axis('equal')
plt.show()

streets = G.edges()
routs_A_B = path_edges

number_of_cars = int(input("please enter the number of cars ---> "))

model = TrafficFlowOptimization(number_of_cars, routs_A_B, streets)
cars_variables = model.make_cars_variables()
routes_cars = model.route_for_each_cars_variables(cars_variables)
qubo = model.make_qubo(cars_variables)
model.adding_cost_and_penalty(qubo, routes_cars)
model.solve_with_Dwave(qubo,  method = "hybrid")


