import unittest
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


# Create simple graph
def create_graph():
    default_weight = 10
    graph = DiGraph()
    graph_algo = GraphAlgo()
    graph_algo.__init__(graph)
    for node in range(20):
        graph.add_node(node)
    for node in range(19):
        graph.add_edge(node, node + 1, default_weight)
    return graph


def create_graph_for_component():
    default_weight = 10
    graph = DiGraph()
    graph_algo = GraphAlgo()
    graph_algo.__init__(graph)
    for node in range(8):
        graph.add_node(node)
    graph.add_edge(0,2,default_weight)
    graph.add_edge(1,0,default_weight)
    graph.add_edge(1,3,default_weight)
    graph.add_edge(2,1,default_weight)
    graph.add_edge(2,3,default_weight)
    graph.add_edge(2,4,default_weight)
    graph.add_edge(3,5,default_weight)
    graph.add_edge(5,3,default_weight)
    graph.add_edge(4,5,default_weight)
    graph.add_edge(5,7,default_weight)
    graph.add_edge(6,7,default_weight)
    graph.add_edge(4,6,default_weight)
    graph.add_edge(6,4,default_weight)

    return graph


class MyTestCase(unittest.TestCase):

    def test_save_and_load(self):
        graph = create_graph()
        graph_algo = GraphAlgo(graph)
        self.assertTrue(graph_algo.save_to_json("MyGraph.json"))
        self.assertEqual(graph_algo.get_graph().v_size(), 20)
        self.assertEqual(graph_algo.get_graph().e_size(), 19)

        self.assertTrue(graph_algo.load_from_json("../data/A0"))
        graph = graph_algo.get_graph()
        self.assertEqual(graph.v_size(), 11)
        self.assertEqual(graph.e_size(), 22)
        self.assertEqual(graph.get_mc(), 33)

        self.assertTrue(graph_algo.load_from_json("../data/A3"))
        graph = graph_algo.get_graph()
        self.assertEqual(graph.v_size(), 49)
        self.assertEqual(graph.e_size(), 136)
        self.assertEqual(graph.get_mc(), 185)

        self.assertTrue(graph_algo.load_from_json("../data/A5"))
        graph = graph_algo.get_graph()
        self.assertEqual(graph.v_size(), 48)
        self.assertEqual(graph.e_size(), 166)
        self.assertEqual(graph.get_mc(), 214)

        self.assertFalse(graph_algo.load_from_json("../data/A404"))
        self.assertFalse(graph_algo.load_from_json("ThisDoesNotExist.json"))

    def test_shortest_path(self):
        graph = create_graph()
        graph_algo = GraphAlgo(graph)
        self.assertEqual(graph_algo.shortest_path(0,10), (100, [0,1,2,3,4,5,6,7,8,9,10]))

        graph_algo.load_from_json("../data/A3")
        graph = graph_algo.get_graph()
        self.assertEqual(graph_algo.shortest_path(1,15),
                         (4.743208031114117, [1, 0, 16, 15]))

        graph_algo.load_from_json("../data/A5")
        graph = graph_algo.get_graph()
        self.assertEqual(graph_algo.shortest_path(4, 9), (2.948614138644694, [4, 13, 11, 9]))
        self.assertEqual(graph_algo.shortest_path(2, 2), (0, [2]))

    def test_connected_component(self):
        graph = create_graph_for_component()
        graphAlgo = GraphAlgo(graph)
        ans1 = graphAlgo.connected_component(1)
        ans2 = graphAlgo.connected_component(7)
        ans3 = graphAlgo.connected_component(8)
        self.assertEqual(ans1, [0, 1, 2])
        self.assertEqual(ans2, [7])
        self.assertEqual(ans3, [])

    def test_connected_components(self):
        graph = create_graph_for_component()
        graphAlgo = GraphAlgo(graph)
        ans1 = graphAlgo.connected_components()
        self.assertEqual(ans1, [[0, 1, 2], [3, 5], [4, 6], [7]])


    def test_plot(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A0")
        graph = algo.get_graph()
        algo.plot_graph(graph)


if __name__ == '__main__':
    unittest.main()
