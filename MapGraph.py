import networkx as nx
import random
import itertools


class Indexable(object):

    def __init__(self, gen):
        self.gen = iter(gen)

    def __iter__(self):
        return self.gen

    def __getitem__(self, index):
        try:
            return next(itertools.islice(self.gen, index, index+1))
        except TypeError:
            return list(itertools.islice(self.gen, index.start, index.stop, index.step))


def make_graph(row, column):
    node = row*column
    node_limit = column
    G = nx.Graph(name="MAHDI",)
    H = nx.path_graph(node)
    G.add_nodes_from(H)
    counter = 0
    speed_limit = [i for i in range(40, 130, 10)]

    for i in range(node - 1):
        sp = random.choice(speed_limit)
        le = random.randint(10, 100)
        counter += 1
        if counter != node_limit:
            G.add_edge(i, i + 1, speed=sp, length=le)
            if i + node_limit <= node - 1:
                sp = random.choice(speed_limit)
                le = random.randint(10, 100)
                G.add_edge(i, i + node_limit, speed=sp, length=le)
        else:
            G.add_edge(i, i + node_limit, speed=sp, length=le)
            counter = 0

    return G


def add_traffic_weight(G):
    for i in G.edges:
        u, v, = i
        we = random.randint(1, 20)
        G[u][v]["traffic weight"] = we


def add_time_travel(G):
    for i in G.edges:
        u, v,  = i
        t = {1: 100, 2: 95, 3: 90, 4: 85, 5: 80, 6: 75, 7: 70, 8: 65, 9: 60, 10: 55,
             11: 50, 12: 45, 13: 40, 14: 35, 15: 30, 16: 25, 17: 20, 18: 15, 19: 10, 20: 5}
        spe = G[u][v]["speed"]
        le = G[u][v]["length"]
        we = t[G[u][v]["traffic weight"]]
        G[u][v]["time travel"] = (le*60)//(we*spe/100)


def print_map_graph_details(G):
    for i in G.edges:
        u, v, = i
        spe = G[u][v]["speed"]
        le = G[u][v]["length"]
        we = G[u][v]["traffic weight"]
        tim = G[u][v]["time travel"]
        print(f"The avenue {u, v} : permissible speed is {spe} km/h **** length is {le} km **** traffic weight is {we} **** it takes time {tim} minutes")


def find_tre_shortest_paths(G, origin_node, destination_node, overlap=None, weight=None):

    if weight == None:
        all_shortest_paths = nx.all_shortest_paths(G, source=origin_node, target=destination_node)
        path_index = Indexable(all_shortest_paths)
        counter = 0

        if (len(G.nodes) <= 120) and (overlap != None):
            path_00 = [path_index[0]]
            for sh_p in all_shortest_paths:
                for p in path_00:
                    counter = 0
                    for sh in sh_p:
                        if sh in p:
                            counter += 1
                        if counter == overlap:
                            break
                    if counter == overlap:
                        break
                if counter < overlap:
                    path_00.append(sh_p)
            # path = [path_00[random.randint(0, len(path_00)-1)] for i in range(3)]
            path = list(path_00)
            random.shuffle(path)
            path = path[0:3]
        else:
            path = [path_index[random.randint(0, len(G.nodes))] for i in range(3)]

    else:
        all_simple_paths = nx.shortest_simple_paths(G, origin_node, destination_node, weight=weight)
        path = []
        counter = 0
        for i in all_simple_paths:
            counter += 1
            path.append(i)
            if counter == 3:
                break
    return path


def paths_edges(paths: list):
    path_edges = []
    for i in paths:
        edges = [(i[j], i[j+1]) for j in range(0, len(i)-1)]
        path_edges.append(edges)
    return path_edges



