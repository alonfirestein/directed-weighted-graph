from src.GraphInterface import GraphInteface
import math


class GeoLocation:
    """
    This class was created in order to implement the location of each node with x,y,z coordinates.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        """
        Calculating the distance between two node locations
        :param other: the second node
        :return:
        """
        return math.sqrt((other.x - self.x) ** 2 +
                         (other.y - self.y) ** 2 +
                         (other.z - self.z) ** 2)


class Node:
    """
    This class was created in order to implement a node in a directed weighted graph.
    """

    def __init__(self, node_id, pos=None):
        self.id = node_id
        self.info = ""
        self.tag = 0
        self.pos = pos

    def __repr__(self):
        return "{}".format(self.id)


class Edge:
    """
    This class was created in order to implement an edge in a directed weighted graph.
    """

    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

    def __str__(self):
        return "(src:" + str(self.src) + ", dest:" + str(self.dest) + ", weight:" + str(self.weight) + ")"


class DiGraph(GraphInteface):
    """
    Using the previous classes, the DiGraph class is built to implement a directed weighted graph, mostly using dictionaries
    to store the values of different types of data needed in order to properly build the graph.
    """

    def __init__(self):
        self.NodesInGraph = {}
        self.NodesWithOutputEdges = {}
        self.NodesWithReceivingEdges = {}
        self.MC = 0
        self.EdgeCounter = 0

    def v_size(self):
        return len(self.NodesInGraph.keys())

    def e_size(self):
        return self.EdgeCounter

    def get_all_v(self):
        return self.NodesInGraph

    def all_in_edges_of_node(self, id1):
        """
        Returning a list of all the nodes that are connected id1, and their edges are directed towards the node with id1.
        :param id1: the id of the node.
        :return: list of id1's neighbours that have an edge directed towards id1.
        """
        if id1 not in self.NodesWithReceivingEdges:
            return None
        return self.NodesWithReceivingEdges[id1]

    def all_out_edges_of_node(self, id1):
        """
        Returning a list of all the nodes that are connected id1, and their edges are directed away from the node with id1.
        :param id1: the id of the node.
        :return: list of id1's neighbours that have an edge directed away from id1.
        """
        if id1 not in self.NodesWithOutputEdges:
            return None
        return self.NodesWithOutputEdges[id1]

    def get_mc(self):
        return self.MC

    def getNode(self, id):
        if id not in  self.NodesInGraph:
            return None
        return self.NodesInGraph[id]

    def add_edge(self, id1, id2, weight):
        """
        Connecting an edge between two nodes in a directed weighted graph.
        :param id1: the source node of the edge
        :param id2: the destination node of the edge
        :param weight: the weigh of the edge
        :return: (True/False) if the edge was successfully connected or not
        """
        if (id1 not in self.NodesInGraph.keys()) or (id2 not in self.NodesInGraph.keys()):
            return False
        if id1 == id2:
            return False
        # If edge exists then we do nothing
        if id2 in self.NodesWithOutputEdges[id1]:
            return False
        self.NodesWithOutputEdges[id1][id2] = weight
        self.NodesWithReceivingEdges[id2][id1] = weight
        self.MC += 1
        self.EdgeCounter += 1
        return True

    def add_node(self, node_id, pos: tuple = None):
        """
        Creating a new node and adding it to the graph.
        :param node_id: the id number of the new node to create
        :param pos: the position of the node in graph
        :return: (True/False) if the node was successfully added to the graph or not.
        """
        if node_id in self.NodesInGraph:
            return False
        node = Node(node_id, pos)
        self.NodesInGraph[node_id] = node
        self.NodesWithOutputEdges[node_id] = {}
        self.NodesWithReceivingEdges[node_id] = {}
        self.MC += 1
        return True

    def remove_node(self, node_id):
        """
        Removing a node from the graph, therefore needing to remove all the edges connected to him (if such exist).
        :param node_id: the id of the node to remove from the graph.
        :return: (True/False) if the node was successfully removed or not.
        """
        if node_id not in self.NodesInGraph:
            return False

        for key in self.NodesWithOutputEdges[node_id]:
            del self.NodesWithReceivingEdges[key][node_id]
            self.EdgeCounter -= 1
        del self.NodesWithOutputEdges[node_id]

        for key in self.NodesWithReceivingEdges[node_id]:
            del self.NodesWithOutputEdges[key][node_id]
            self.EdgeCounter -= 1
        del self.NodesWithReceivingEdges[node_id]

        del self.NodesInGraph[node_id]
        self.MC += 1
        return True

    def remove_edge(self, node_id1, node_id2):
        """
        Removing an edge between two nodes from the graph (if such exist).
        :param node_id1: the source node of the edge
        :param node_id2: the destination node of the edge
        :return: (True/False) if the edge was successfully removed or not.
        """
        if node_id1 not in self.NodesWithOutputEdges:
            return False
        elif node_id2 not in self.NodesWithOutputEdges[node_id1]:
            return False
        del self.NodesWithOutputEdges[node_id1][node_id2]
        del self.NodesWithReceivingEdges[node_id2][node_id1]
        self.MC += 1
        self.EdgeCounter -= 1
        return True

    def __str__(self):
        result = ""
        for node in self.NodesInGraph.keys():
            result += "Node: %s, Neighbours: %s \n" %(node, str(self.NodesWithOutputEdges[node]))
        return result
