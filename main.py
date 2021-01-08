import numpy as np
import matplotlib.pyplot as plt
from src.DiGraph import DiGraph
import random
from src.GraphAlgo import GraphAlgo
import networkx as nx
import os, re


def get_json_graphs():
    my_graphs = list()
    for file in os.listdir("data"):
        if file.startswith("G_"):
            # graph = DiGraph()
            # algo = GraphAlgo(graph)
            # algo.load_from_json(file)
            # graph = algo.get_graph()
            my_graphs.append(file)

    return my_graphs

def main():

    graph = DiGraph()
    algo = GraphAlgo(graph)
    algo.load_from_json("data/G_10_80_0")
    graph = algo.get_graph()
    print(graph)


if __name__ == '__main__':
    main()