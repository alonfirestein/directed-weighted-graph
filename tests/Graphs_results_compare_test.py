import unittest
from tests.run_time_compare_test import create_nx_graph
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo
import networkx as nx


class MyTestCase(unittest.TestCase):
    """
    This unittest class was built in order to check that the results of the graph algorithms in our implementation
    was the same as the results of the algorithms in the NetworkX library.
    """
    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = algo.shortest_path(7, 15)
        nx_result = (nx.dijkstra_path_length(nx_graph, 7, 15), nx.shortest_path(nx_graph, 7, 15))
        self.assertEqual(nx_result, graph_result)
        graph_result = algo.shortest_path(32, 32)
        nx_result = (nx.dijkstra_path_length(nx_graph, 32, 32), nx.shortest_path(nx_graph, 32, 32))
        self.assertEqual(nx_result, graph_result)

        algo.load_from_json("../data/A3")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = algo.shortest_path(13, 36)
        nx_result = (nx.dijkstra_path_length(nx_graph, 13, 36), nx.shortest_path(nx_graph, 13, 36))
        self.assertEqual(nx_result, graph_result)

        algo.load_from_json("../data/Graphs_on_circle/G_100_800_1.json")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = algo.shortest_path(42, 95)
        nx_result = (nx.dijkstra_path_length(nx_graph, 42, 95), nx.shortest_path(nx_graph, 42, 95))
        self.assertEqual(nx_result, graph_result)

    def test_connected_components(self):
        algo = GraphAlgo()
        algo.load_from_json("../data/A5")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = algo.connected_components()
        nx_result = list(nx.strongly_connected_components(nx_graph))
        for node in graph_result[0]:
            self.assertTrue(node in nx_result[0])
        graph_result = len(algo.connected_components()) == 1
        nx_result = nx.is_strongly_connected(nx_graph)
        self.assertEqual(nx_result, graph_result)

        algo.load_from_json("../data/A3")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = algo.connected_components()
        nx_result = list(nx.strongly_connected_components(nx_graph))
        for node in graph_result[0]:
            self.assertTrue(node in nx_result[0])
        graph_result = len(algo.connected_components()) == 1
        nx_result = nx.is_strongly_connected(nx_graph)
        self.assertEqual(nx_result, graph_result)

        algo.load_from_json("../data/Graphs_on_circle/G_1000_8000_1.json")
        graph = algo.get_graph()
        nx_graph = create_nx_graph(graph)
        graph_result = len(algo.connected_components()) == 1
        nx_result = nx.is_strongly_connected(nx_graph)
        self.assertEqual(nx_result, graph_result)


if __name__ == '__main__':
    unittest.main()
