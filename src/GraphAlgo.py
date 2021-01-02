from typing import List

from src import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from queue import PriorityQueue
import json
import math
import matplotlib.pyplot as plt
INFINITY = math.inf


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=DiGraph()):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name):

        self.graph = DiGraph()
        try:
            with open(file_name) as file:
                JSONgraph = json.load(file)
                for node in JSONgraph["Nodes"]:
                    if "pos" in node:
                        pos = tuple(map(float, str(node["pos"]).split(",")))
                        self.graph.add_node(node["id"], pos)
                    else:
                        self.graph.add_node(node["id"])

                for edge in JSONgraph["Edges"]:
                    src = edge["src"]
                    weight = edge["w"]
                    dest = edge["dest"]
                    self.graph.add_edge(src, dest, weight)

        except Exception as e:
            print(e)
            return False

        return True

    def save_to_json(self, file_name):

        if file_name is None:
            return False

        JSONgraph = dict()
        JSONgraph["Edges"] = list()
        JSONgraph["Nodes"] = list()
        try:
            with open(file_name, "w") as file:
                graph_nodes = self.graph.get_all_v()
                for node_key, pos in graph_nodes.items():
                    JSONgraph["Nodes"].append({"pos": pos, "id": node_key})
                    for neighbour_key, weight in  self.graph.all_out_edges_of_node(node_key).items():
                        JSONgraph["Edges"].append({"src": node_key, "w": weight, "dest": neighbour_key})

                json.dump(JSONgraph, file, default=lambda x: x.__dict__)
                return True

        except IOError:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):

        if id1 == id2:
            return 0, []

        parentsList = dict()
        distanceList = dict()
        visitedNodes = set()
        graph_nodes = self.graph.get_all_v()

        if (id1 not in graph_nodes) or (id1 not in graph_nodes):
            return None

        queue = PriorityQueue()
        queue.put(graph_nodes[id1].id)
        for node in graph_nodes.keys():
            distanceList[node] = INFINITY

        parentsList[id1] = id1
        distanceList[id1] = 0

        while not queue.empty():
            currentNode = queue.get()
            if currentNode == id2:
                break
            visitedNodes.add(currentNode)

            for key, weight in self.graph.all_out_edges_of_node(currentNode).items():
                nextNode = graph_nodes[key].id
                tempWeight = weight + distanceList[currentNode]
                if tempWeight < distanceList[nextNode]:
                    distanceList[nextNode] = tempWeight
                    parentsList[nextNode] = currentNode
                    queue.put(nextNode)

        # If Path between id1 and id2 is not accessible => therefore not connected:
        if distanceList[id2] == INFINITY:
            return None

        path = []
        BackTrackPath = id2
        while distanceList[BackTrackPath] != 0:
            path.append(graph_nodes[BackTrackPath].id)
            if parentsList[BackTrackPath] != BackTrackPath:
                BackTrackPath = parentsList[BackTrackPath]
        path.append(BackTrackPath)
        path = path[::-1]
        return distanceList[id2], path

    def connected_component(self, id1: int) -> list:
        pass

    def connected_components(self) -> List[list]:
        pass

    def plot_graph(self) -> None:
        pass



