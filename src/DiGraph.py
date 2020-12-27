from src.GraphInterface import GraphInteface
import math


class GeoLocation:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # Distance from another node location
    def distance(self, other):
        return math.sqrt((other.x - self.x) ** 2 +
                         (other.y - self.y) ** 2 +
                         (other.z - self.z) ** 2)


class Node:

    def __init__(self, node_id, loc=None):
        self.id = node_id
        self.info = ""
        self.tag = 0
        self.loc = loc

    def get_id(self):
        return self.id

    def set_loc(self, loc):
        self.loc = loc

    def get_loc(self):
        return self.loc

    def set_tag(self, tag):
        self.tag = tag

    def get_tag(self):
        return self.tag

    def set_info(self, info):
        self.info = info

    def get_info(self):
        return self.info

    def __str__(self):
        return "ID: "+str(self.id)+" Location: "+str(self.loc)


class Edge:

    def __init__(self, src, dest, weight):
        self.src = src
        self.dest = dest
        self.weight = weight

    def get_src(self):
        return self.src

    def get_dest(self):
        return self.dest

    def get_weight(self):
        return self.weight

    def __str__(self):
        return "(src:" + str(self.src) + ", dest:" + str(self.dest) + ", weight:" + str(self.weight) + ")"


class DiGraph(GraphInteface):

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
        return self.NodesWithReceivingEdges[id1]

    def all_out_edges_of_node(self, id1):
        return self.NodesWithOutputEdges[id1]

    def get_mc(self):
        return self.MC

    def add_edge(self, id1, id2, weight):
        if (id1 not in self.NodesInGraph.keys()) or (id2 not in self.NodesInGraph.keys()):
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
        if node_id in self.NodesInGraph:
            return False
        node = Node(node_id, pos)
        self.NodesInGraph[node_id] = node
        self.NodesWithOutputEdges[node_id] = {}
        self.NodesWithReceivingEdges[node_id] = {}
        self.MC += 1
        return True

    def remove_node(self, node_id):
        if node_id not in self.NodesInGraph:
            return False

        # TO DELETE: MADE IT SHORTER FOR HANANEL
        # if (node_id not in self.NodesWithOutputEdges) and (node_id not in self.NodesWithReceivingEdges):
        #     self.NodesInGraph.pop(node_id)
        #     self.MC += 1
        #     return True

        numOfNeighbours = len(self.NodesWithOutputEdges[node_id])
        del self.NodesWithOutputEdges[node_id]
        self.MC += numOfNeighbours
        self.EdgeCounter -= numOfNeighbours

        for key in self.NodesWithReceivingEdges[node_id]:
            del self.NodesWithOutputEdges[key][node_id]
            self.MC += 1
            self.EdgeCounter -= 1

        del self.NodesWithReceivingEdges[node_id]
        self.NodesInGraph.pop(node_id)
        self.MC += 1
        return True

    def remove_edge(self, node_id1, node_id2):
        if node_id1 not in self.NodesWithOutputEdges:
            return False
        elif node_id2 not in self.NodesWithOutputEdges[node_id1]:
            return False
        del self.NodesWithOutputEdges[node_id1][node_id2]
        self.MC += 1
        self.EdgeCounter -= 1
        return True

    def __str__(self):
        result = ""
        for node in self.NodesInGraph.keys():
            result += "Node: %s, Neighbours: %s \n" %(node, str(self.NodesWithOutputEdges[node]))
        return result

