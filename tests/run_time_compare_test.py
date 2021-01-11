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

"""
This class was built in order to check and compare the run time results of the graph algorithms in our
implementation compared to the run time results of the algorithms in the NetworkX library, and the graph
implementation in Java.
"""


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
    os.chdir("/Users/alon/PycharmProjects/Ex3/data/Graphs_no_pos")
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
    algorithm_labels = ['SP', 'CCS', 'CC']
    plot_titles = ['Graph 1: |V|=10, |E|=80', r'Graph 2: |V|=$10^2$, |E|=$8\cdot10^2$',
                   r'Graph 3: |V|=$10^3$, |E|=$8\cdot10^3$',
                   r'Graph 4: |V|=$10^4$, |E|=$8\cdot10^4$', r'Graph 5: |V|=$2\cdot10^4$, |E|=$16\cdot10^4$',
                   r'Graph 6: |V|=$3\cdot10^4$, |E|=$24\cdot10^4$']

    py_graph = {0: [time_results[0][10], time_results[1][10], time_results[2][10]],
                1: [time_results[0][100], time_results[1][100], time_results[2][100]],
                2: [time_results[0][1000], time_results[1][1000], time_results[2][1000]],
                3: [time_results[0][10000], time_results[1][10000], time_results[2][10000]],
                4: [time_results[0][20000], time_results[1][20000], time_results[2][20000]],
                5: [time_results[0][30000], time_results[1][30000], time_results[2][30000]]}

    nx_graph = {0: [time_results[3][10], time_results[4][10], 0],
                1: [time_results[3][100], time_results[4][100], 0],
                2: [time_results[3][1000], time_results[4][1000], 0],
                3: [time_results[3][10000], time_results[4][10000], 0],
                4: [time_results[3][20000], time_results[4][20000], 0],
                5: [time_results[3][30000], time_results[4][30000], 0]}
    # java dict - graph_num:[[Graph_no_pos results],[Graph_on_circle results],[Graph_random_pos results]]
    java_graph = {0: [[0.015, 0.0001, 0.001], [0.011, 0.0004285, 0.0002523], [0.017, 0.0002458, 0.0001495]],
                  1: [[0.02, 0.002, 0.002], [0.013, 0.0025, 0.001], [0.01, 0.001, 0.000935]],
                  2: [[0.49, 0.24, 0.26], [0.025, 0.017, 0.013], [0.02, 0.02, 0.01]],
                  3: [[0.121, 0.067, 0.077], [0.14, 0.11, 0.049], [0.12, 0.07, 0.12]],
                  4: [[0.218, 0.211, 0.151], [0.189, 0.207, 0.148], [0.18, 0.16, 0.20]],
                  5: [[0.354, 0.247, 0.243], [0.325, 0.322, 0.11], [0.29, 0.34, 0.12]]}

    width = 0.2  # the width of the bars
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(11, 8))
    x = np.arange(len(algorithm_labels))

    for i in range(6):
        plt.subplot(2, 3, i+1)
        plt.title(plot_titles[i])
        y1 = [py_graph[i][0], py_graph[i][1], py_graph[i][2]]
        y2 = [java_graph[i][0][0], java_graph[i][0][1], java_graph[i][0][2]]
        y3 = [nx_graph[i][0], nx_graph[i][1], nx_graph[i][2]]
        plt.yscale('log')
        plt.bar(x-width, y1, width, label='Python', color='red')
        plt.bar(x, y2, width, label='Java', color='mediumblue')
        plt.bar(x+width, y3, width, label='NetworkX', color='green')
        plt.xlabel('Algorithm')
        plt.ylabel('Time Taken in seconds')
        plt.xticks(range(len(algorithm_labels)), algorithm_labels)
        plt.legend(loc='best', prop={'size': 6})

    plt.tight_layout()
    plt.savefig("Comparison1.png")
    plt.show()


if __name__ == '__main__':
    plot_comparison_results()

