import networkx as nx
import time
import random
import os, re
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

    for edge in range(num_of_nodes*2):
        weight = random.uniform(0, 10)
        nodeA = random.randint(0, num_of_nodes-1)
        nodeB = random.randint(0, num_of_nodes-1)
        while (nodeA == nodeB) or (nodeB in graph.all_out_edges_of_node(nodeA)):
            nodeB = random.randint(0, num_of_nodes-1)
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

    graph = DiGraph()
    algo = GraphAlgo(graph)
    my_graphs = list()
    for file in os.listdir('data'):
        if re.match('G_*', file):
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
    nx_connected_comp_results = dict()

    for my_graph in get_json_graphs():
        index = 0
        shortest_path_results[index] = list()
        connected_components_results[index] = list()
        connected_comp_results[index] = list()
        nx_shortest_path_results[index] = list()
        nx_connected_components_results[index] = list()
        nx_connected_comp_results[index] = list()
        algo = GraphAlgo(my_graph)
        nx_graph = create_nx_graph(my_graph)

        # Shortest Path:
        print("Starting shortest path on python graph")
        start = time.time()
        algo.shortest_path(4, 9)
        end = time.time()
        result = end - start
        shortest_path_results[index].append(result)
        print("Starting shortest path on networkx graph")
        start = time.time()
        nx.dijkstra_path_length(nx_graph, 4, 9)
        end = time.time()
        nx_result = end - start
        nx_shortest_path_results[index].append(nx_result)

        # Connected Components:
        print("Starting connected components on python graph")
        start = time.time()
        algo.connected_components()
        end = time.time()
        result = end - start
        connected_components_results[index].append(result)

        print("Starting connected components on networkx graph")
        start = time.time()
        nx.strongly_connected_components(nx_graph)
        end = time.time()
        nx_result = end - start
        nx_connected_components_results[index].append(nx_result)

        # Connected Component:
        print("Starting connected component on python graph")
        start = time.time()
        algo.connected_component(27)
        end = time.time()
        result = end - start
        connected_comp_results[index].append(result)

        print("Starting connected components on networkx graph")
        start = time.time()
        nx.strongly_connected_components(nx_graph)
        end = time.time()
        nx_result = end - start
        connected_comp_results[index].append(nx_result)

        index += 1

    return shortest_path_results, connected_components_results, connected_comp_results


def plot_comparison_results():

    time_results = compare_graph_algorithms()
    labels = ['Python', 'NetworkX']  # Add Java as third label
    labels2 = ['SP', 'CCS', 'CC']
    # lists are labeled as: function()[algorithm_dictionary][num_of_nodes][python/networkx/java]
    py_graph_results_hun = [time_results[0][100][0], time_results[1][100][0], time_results[2][100][0]]
    py_graph_results_thou = [time_results[0][10000][0], time_results[1][10000][0], time_results[2][10000][0]]
    #py_graph_results_mil = [time_results[0][1000000][0], time_results[1][1000000][0], time_results[2][1000000][0]]

    nx_graph_results_hun = [time_results[0][100][1], time_results[1][100][1], time_results[2][100][1]]
    nx_graph_results_thou = [time_results[0][10000][1], time_results[1][10000][1], time_results[2][10000][1]]
    #nx_graph_results_mil = [time_results[0][1000000][1], time_results[1][1000000][1], time_results[2][1000000][1]]

    x = np.arange(len(labels2))  # the label locations
    width = 0.35  # the width of the bars
    fig, ax = plt.subplots(2, figsize=(9, 6))
    # Add Java as third subplot
    plt.subplot(1,2,1)
    plt.title(labels[0])
    y1 = [py_graph_results_hun[0], py_graph_results_hun[1],py_graph_results_hun[2]]
    y2 = [py_graph_results_thou[0], py_graph_results_thou[1],py_graph_results_thou[2]]
    plt.yscale('log')
    plt.bar(x - width / 2, y1, width, label='10^2 nodes', color='navy')
    plt.bar(x + width / 2, y2, width, label='10^4 nodes', color='g')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best')


    # Add Java as third subplot
    plt.subplot(1,2,2)
    plt.title(labels[1])
    y3 = [nx_graph_results_hun[0], nx_graph_results_hun[1], nx_graph_results_hun[2]]
    y4 = [nx_graph_results_thou[0], nx_graph_results_thou[1], nx_graph_results_thou[2]]
    plt.yscale('log')
    plt.bar(x - width / 2, y3, width, label='10^2 nodes', color='darkred')
    plt.bar(x + width / 2, y4, width, label='10^4 nodes', color='gold')
    plt.xlabel('Algorithm')
    plt.ylabel('Time Taken in seconds')
    plt.xticks(range(len(labels2)), labels2, rotation=45)
    plt.legend(loc='best')


    plt.tight_layout()
    fig.tight_layout()
    plt.savefig("Comparison.png")
    plt.show()


if __name__ == '__main__':

    plot_comparison_results()

