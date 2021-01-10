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
    os.chdir("/Users/alon/PycharmProjects/Ex3/data/Graphs_on_circle")
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
    labels2 = ['SP', 'CCS', 'CC']
    plot_titles = ['Graph 1: |V|=10, |E|=80', r'Graph 2: |V|=$10^2$, |E|=$8\cdot10^2$', r'Graph 3: |V|=$10^3$, |E|=$8\cdot10^3$',
                    r'Graph 4: |V|=$10^4$, |E|=$8\cdot10^4$', r'Graph 5: |V|=$2\cdot10^4$, |E|=$16\cdot10^4$',
                    r'Graph 6: |V|=$3\cdot10^4$, |E|=$24\cdot10^4$']
    py_graph_1 = [time_results[0][10], time_results[1][10], time_results[2][10]]
    py_graph_2 = [time_results[0][100], time_results[1][100], time_results[2][100]]
    py_graph_3 = [time_results[0][1000], time_results[1][1000], time_results[2][1000]]
    py_graph_4 = [time_results[0][10000], time_results[1][10000], time_results[2][10000]]
    py_graph_5 = [time_results[0][20000], time_results[1][20000], time_results[2][20000]]
    py_graph_6 = [time_results[0][30000], time_results[1][30000], time_results[2][30000]]

    nx_graph_1 = [time_results[3][10], time_results[4][10], 0]
    nx_graph_2 = [time_results[3][100], time_results[4][100], 0]
    nx_graph_3 = [time_results[3][1000], time_results[4][1000], 0]
    nx_graph_4 = [time_results[3][10000], time_results[4][10000], 0]
    nx_graph_5 = [time_results[3][20000], time_results[4][20000], 0]
    nx_graph_6 = [time_results[3][30000], time_results[4][30000], 0]

    java_graph_1 = [0.015, 0.0001, 0.001]
    java_graph_2 = [0.02, 0.002, 0.002]
    java_graph_3 = [0.49,  0.24, 0.26]
    java_graph_4 = [0.121, 0.067, 0.077]
    java_graph_5 = [0.218, 0.211, 0.151]
    java_graph_6 = [0.354, 0.247, 0.243]

    width = 0.2  # the width of the bars
    fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(11, 8))
    x = np.arange(len(labels2))

    plt.subplot(2, 3, 1)
    plt.title(plot_titles[0])
    y1 = [py_graph_1[0], py_graph_1[1], py_graph_1[2]]
    y2 = [java_graph_1[0], java_graph_1[1], java_graph_1[2]]
    y3 = [nx_graph_1[0], nx_graph_1[1], nx_graph_1[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.subplot(2, 3, 2)
    plt.title(plot_titles[1])
    y1 = [py_graph_2[0], py_graph_2[1], py_graph_2[2]]
    y2 = [java_graph_2[0], java_graph_2[1], java_graph_2[2]]
    y3 = [nx_graph_2[0], nx_graph_2[1], nx_graph_2[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.subplot(2, 3, 3)
    plt.title(plot_titles[2])
    y1 = [py_graph_3[0], py_graph_3[1], py_graph_3[2]]
    y2 = [java_graph_3[0], java_graph_3[1], java_graph_3[2]]
    y3 = [nx_graph_3[0], nx_graph_3[1], nx_graph_3[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.subplot(2, 3, 4)
    plt.title(plot_titles[3])
    y1 = [py_graph_4[0], py_graph_4[1], py_graph_4[2]]
    y2 = [java_graph_4[0], java_graph_4[1], java_graph_4[2]]
    y3 = [nx_graph_4[0], nx_graph_4[1], nx_graph_4[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.subplot(2, 3, 5)
    plt.title(plot_titles[4])
    y1 = [py_graph_5[0], py_graph_5[1], py_graph_5[2]]
    y2 = [java_graph_5[0], java_graph_5[1], java_graph_5[2]]
    y3 = [nx_graph_5[0], nx_graph_5[1], nx_graph_5[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.subplot(2, 3, 6)
    plt.title(plot_titles[5])
    y1 = [py_graph_6[0], py_graph_6[1], py_graph_6[2]]
    y2 = [java_graph_6[0], java_graph_6[1], java_graph_6[2]]
    y3 = [nx_graph_6[0], nx_graph_6[1], nx_graph_6[2]]
    plt.yscale('log')
    plt.bar(x-width, y1, width, label='Python', color='red')
    plt.bar(x, y2, width, label='Java', color='mediumblue')
    plt.bar(x+width, y3, width, label='NetworkX', color='green')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best', prop={'size': 6})

    plt.tight_layout()
    fig.tight_layout()
    plt.savefig("Comparison2.png")
    plt.show()


if __name__ == '__main__':
    plot_comparison_results()

