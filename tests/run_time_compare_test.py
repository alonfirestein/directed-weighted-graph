import networkx as nx
import time
import random
import os
import glob
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import matplotlib.pyplot as plt
import math
import numpy as np

random.seed(7)


def graph_creator(num_of_nodes: int):
    graph = DiGraph()
    for node in range(num_of_nodes):
        print("Adding node: ", node)
        graph.add_node(node)

    for edge in range(num_of_nodes * 2):
        weight = random.uniform(0, 10)
        nodeA = random.randint(0, num_of_nodes - 1)
        nodeB = random.randint(0, num_of_nodes - 1)
        while (nodeA == nodeB) or (nodeB in graph.all_out_edges_of_node(nodeA)):
            nodeB = random.randint(0, num_of_nodes - 1)
        graph.add_edge(nodeA, nodeB, weight)
        print("Connecting edge number: ", edge, " - between: ", nodeA, " and ", nodeB)
    return graph


def create_nx_graph(graph):
    nx_graph = nx.DiGraph()
    for key, node in graph.get_all_v().items():
        pos = node.pos
        nx_graph.add_node(key, pos=pos)

        for neighbour, weight in graph.all_out_edges_of_node(key).items():
            ni_pos = graph.get_all_v()[neighbour].pos
            nx_graph.add_node(neighbour, pos=ni_pos)
            nx_graph.add_edge(key, neighbour, weight=weight)

    return nx_graph


def get_json_graphs():
    my_graphs = list()
    os.chdir("/Users/alon/PycharmProjects/Ex3/data")
    for file in glob.glob("G_*"):
        graph = DiGraph()
        algo = GraphAlgo(graph)
        algo.load_from_json(file)
        graph = algo.get_graph()
        my_graphs.append(graph)

    return my_graphs

def compare_graph_algorithms():
    shortest_path_results = dict()
    connected_components_results = dict()
    connected_comp_results = dict()
    nx_shortest_path_results = dict()
    nx_connected_components_results = dict()

    for my_graph in get_json_graphs():
        index = my_graph.v_size()
        algo = GraphAlgo(my_graph)
        nx_graph = create_nx_graph(my_graph)

        # Shortest Path:
        start = time.time()
        algo.shortest_path(4, 9)
        end = time.time()
        result = end - start
        shortest_path_results[index] = result

        start = time.time()
        nx.dijkstra_path_length(nx_graph, 4, 9)
        end = time.time()
        nx_result = end - start
        nx_shortest_path_results[index] = nx_result

        # Connected Components:
        start = time.time()
        algo.connected_components()
        end = time.time()
        result = end - start
        connected_components_results[index] = result

        start = time.time()
        nx.strongly_connected_components(nx_graph)
        end = time.time()
        nx_result = end - start
        nx_connected_components_results[index] = nx_result

        # Connected Component:
        start = time.time()
        algo.connected_component(8)
        end = time.time()
        result = end - start
        connected_comp_results[index] = result

    return shortest_path_results, connected_components_results, connected_comp_results, nx_shortest_path_results, \
           nx_connected_components_results


def plot_comparison_results():
    time_results = compare_graph_algorithms()
    labels = ['My Graph in Python', 'Graph in NetworkX', 'My Graph in Java']  # Add Java as third label
    labels2 = ['SP', 'CCS', 'CC']
    labels_for_nx = ['SP', 'CCS']

    py_graph_1 = [time_results[0][10], time_results[1][10], time_results[2][10]]
    py_graph_2 = [time_results[0][100], time_results[1][100], time_results[2][100]]
    py_graph_3 = [time_results[0][1000], time_results[1][1000], time_results[2][1000]]
    py_graph_4 = [time_results[0][10000], time_results[1][10000], time_results[2][10000]]
    py_graph_5 = [time_results[0][20000], time_results[1][20000], time_results[2][20000]]
    py_graph_6 = [time_results[0][30000], time_results[1][30000], time_results[2][30000]]

    nx_graph_1 = [time_results[3][10], time_results[4][10]]
    nx_graph_2 = [time_results[3][100], time_results[4][100]]
    nx_graph_3 = [time_results[3][1000], time_results[4][1000]]
    nx_graph_4 = [time_results[3][10000], time_results[4][10000]]
    nx_graph_5 = [time_results[3][20000], time_results[4][20000]]
    nx_graph_6 = [time_results[3][30000], time_results[4][30000]]

    width = 0.1  # the width of the bars
    fig, ax = plt.subplots(2, figsize=(9, 6))
    x = np.arange(len(labels2))-(width/2)

    # Add Java as third subplot
    plt.subplot(1, 2, 1)
    plt.title(labels[0])
    y1 = [py_graph_1[0], py_graph_1[1], py_graph_1[2]]
    y2 = [py_graph_2[0], py_graph_2[1], py_graph_2[2]]
    y3 = [py_graph_3[0], py_graph_3[1], py_graph_3[2]]
    y4 = [py_graph_4[0], py_graph_4[1], py_graph_4[2]]
    y5 = [py_graph_5[0], py_graph_5[1], py_graph_5[2]]
    y6 = [py_graph_6[0], py_graph_6[1], py_graph_6[2]]

    plt.yscale('log')
    plt.bar(x-width*2, y1, width, label='10 nodes', color='black')
    plt.bar(x-width, y2, width, label=r'$10^2$ nodes', color='purple')
    plt.bar(x, y3, width, label=r'$10^3$ nodes', color='mediumvioletred')
    plt.bar(x+width, y4, width, label=r'$10^4$ nodes', color='r')
    plt.bar(x+width*2, y5, width, label=r'$2\cdot10^4$ nodes', color='darkorange')
    plt.bar(x+width*3, y6, width, label=r'$3\cdot10^4$ nodes', color='gold')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 7})

    # Add Java as third subplot
    plt.subplot(1, 2, 2)
    x = np.arange(len(labels_for_nx))-(width/2)

    plt.title(labels[1])
    y7 = [nx_graph_1[0], nx_graph_1[1]]
    y8 = [nx_graph_2[0], nx_graph_2[1]]
    y9 = [nx_graph_3[0], nx_graph_3[1]]
    y10 = [nx_graph_4[0], nx_graph_4[1]]
    y11 = [nx_graph_5[0], nx_graph_5[1]]
    y12 = [nx_graph_6[0], nx_graph_6[1]]

    plt.yscale('log')
    plt.bar(x-width*2, y7, width, label= r'10 nodes', color='deeppink')
    plt.bar(x-width*1, y8, width, label= r'$10^2$ nodes', color='violet')
    plt.bar(x, y9, width, label= r'$10^3$ nodes', color='navajowhite')
    plt.bar(x+width, y10, width, label= r'$10^4$ nodes', color='silver')
    plt.bar(x+width*2, y11, width, label= r'$2\cdot10^4$ nodes', color='greenyellow')
    plt.bar(x+width*3, y12, width, label= r'$3\cdot10^4$ nodes', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels_for_nx)), labels_for_nx, rotation=45)
    plt.legend(loc='best', prop={'size': 7})

    plt.tight_layout()
    fig.tight_layout()
    plt.savefig("Comparison.png")
    plt.show()


if __name__ == '__main__':
    plot_comparison_results()

