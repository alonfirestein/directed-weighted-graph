from typing import List
from src import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from src.DiGraph import DiGraph
from queue import PriorityQueue
import json
import math
import random
import matplotlib.pyplot as plt
from matplotlib.patches import ConnectionPatch


INFINITY = math.inf


class GraphAlgo(GraphAlgoInterface):
    """
    This class was created in order to implement a number of different algorithms in a directed weighted graph.
    """
    def __init__(self, graph=DiGraph()):
        self.graph = graph

    def get_graph(self) -> GraphInterface:
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loading a graph that was saved as in a JSON file format.
        :param file_name: the name of the file that we want to load
        :return: (True/False) if the graph was successfully loaded from the file or not.
        """
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

    def save_to_json(self, file_name: str) -> bool:
        """
        Saving a graph in a JSON file format.
        :param file_name: the name of the file that we want to save it as.
        :return: (True/False) if the graph was successfully saved in the file or not.
        """
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
                    for neighbour_key, weight in self.graph.all_out_edges_of_node(node_key).items():
                        JSONgraph["Edges"].append({"src": node_key, "w": weight, "dest": neighbour_key})

                json.dump(JSONgraph, file, default=lambda x: x.__dict__)
                return True

        except IOError:
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Using dijkstra's algorithm, this function calculates the shortest path between two nodes in a directed weighted
        graph, a
        :param id1: the source node of the path
        :param id2: the destination node of the path
        :return: a tuple containing the sum weight of the path,
        and a list of all the nodes that were visited during the traversal between the two nodes.
        """
        if id1 == id2:
            return 0, []

        parentsList = dict()
        distanceList = dict()
        visitedNodes = set()
        graph_nodes = self.graph.get_all_v()

        if (id1 not in graph_nodes) or (id1 not in graph_nodes):
            return INFINITY, None

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
            return INFINITY, None

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
        if id1 not in self.get_graph().NodesInGraph:
            return None  # asq Boaz

        node = self.get_graph().getNode(id1)
        MyList = list()
        node.tag = 1
        MyList.append(node)
        while len(MyList) != 0:
            tempNode = MyList.pop()
            for ni in self.get_graph().NodesWithOutputEdges[tempNode.id].keys():
                tempNode2 = self.get_graph().getNode(ni)
                if tempNode2.tag == 0:
                    tempNode2.tag = 1
                    MyList.append(tempNode2)

        ans = [node]
        node.tag = 2
        MyList.append(node)
        while len(MyList) != 0:
            tempNode = MyList.pop()
            for Ni in self.get_graph().NodesWithReceivingEdges[tempNode.id].keys():
                reversNi = self.get_graph().getNode(Ni)
                if reversNi.tag == 1:
                    reversNi.tag = 2
                    ans.append(reversNi)
        return ans

    def connected_components(self) -> List[list]:
        ans = []
        for node in self.get_graph().NodesInGraph.values():
            if node.tag == 2:
                continue
            else:
                ans.append(self.connected_component(node.id))
            for node1 in self.get_graph().NodesInGraph.values():
                if node1.tag != 2:
                    node1.tag = 0
        return ans

    def plot_graph(self) -> None:
        """
        Using the matplotlib library, this function plots a directed weighted graph in order to properly
        visualize a representation of the graph.
        :return: None - just opens up the pop up window containing the graph visualization.
        """
        x = self.get_all_node_pos()[0]
        y = self.get_all_node_pos()[1]
        fig, ax = plt.subplots(1, 1, figsize=(8, 7))
        coordsA, coordsB = "data", "data"
        for i in range(self.graph.v_size()):
            if self.graph.getNode(i).pos is None:
                self.graph.getNode(i).pos = self.generate_random_pos()
            for j in self.graph.all_out_edges_of_node(i):
                xy1 = (self.graph.getNode(i).pos[0], self.graph.getNode(i).pos[1])
                xy2 = (self.graph.getNode(j).pos[0], self.graph.getNode(j).pos[1])
                con = ConnectionPatch(xy1, xy2, coordsA, coordsB,
                                      arrowstyle="->", shrinkA=5, shrinkB=5, fc="w")
                #ax.plot([xy1[0], xy2[0]], [xy1[1], xy2[1]], "o")
                ax.add_artist(con)
                ax.plot(x, y, "o")
        plt.title("Graph Representation:")
        plt.xlabel("X position of node")
        plt.ylabel("Y position of node")
        plt.xlim(self.get_node_pos_limits()[1]-0.0008, self.get_node_pos_limits()[0]+0.0008)
        plt.ylim(self.get_node_pos_limits()[3]-0.0008, self.get_node_pos_limits()[2]+0.0008)
        plt.tight_layout()
        plt.show()

    def get_node_pos_limits(self):
        """
        Getting the limits of the X/Y axis using the position of all the nodes in graph.
        :return: the maximum and minimum X/Y values from all the node positions in the graph.
        """
        x = random.uniform(35.1800000000, 35.2500000000)
        y = random.uniform(32.1000000000, 32.1100000000)
        x_positions, y_positions = list(), list()
        for node in self.graph.get_all_v().values():
            if node.pos is None:
                node.pos = (x,y,0)
            x_positions.append(node.pos[0])
            y_positions.append(node.pos[1])
        return max(x_positions), min(x_positions), max(y_positions), min(y_positions)

    def get_all_node_pos(self):
        """
        Getting the positions of all the nodes in the graph.
        :return: two lists, containing the X positions of all the nodes, and the Y positions of all the nodes.
        """
        x_positions, y_positions = list(), list()
        for node in self.graph.get_all_v().values():
            if node.pos is None:
                node.pos = self.generate_random_pos()
            x_positions.append(node.pos[0])
            y_positions.append(node.pos[1])
        return x_positions, y_positions

    def generate_random_pos(self):
        """
        In case a node does not have a position/geolocation, therefore this function will generate a random position
        for him using the random library, and the minimum/maximum limits from the rest of the nodes in the graph.
        :return: a random position in the graph
        """
        x_max, x_min, y_max, y_min = self.get_node_pos_limits()[0], self.get_node_pos_limits()[1],\
                                     self.get_node_pos_limits()[2], self.get_node_pos_limits()[3]
        x = random.uniform(x_min, x_max)
        y = random.uniform(y_min, y_max)
        z = 0
        return x, y, z
