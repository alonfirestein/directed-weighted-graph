import unittest
from src.DiGraph import DiGraph


# Create simple graph
def create_graph():
    default_weight = 10
    graph = DiGraph()
    for node in range(20):
        graph.add_node(node)
    for node in range(19):
        graph.add_edge(node,node+1,default_weight)
    return graph


class MyTestCase(unittest.TestCase):

    def test_node(self):
        graph = create_graph()
        self.assertEqual(graph.v_size(), 20)
        for node in range(5):
            graph.remove_node(node)
        self.assertEqual(graph.v_size(), 15)

    def test_edge(self):
        graph = create_graph()
        self.assertEqual(graph.e_size(), 19)
        for node in range(5):
            graph.remove_edge(node,node+1)
        self.assertEqual(graph.e_size(), 14)
        graph.remove_node(15)
        self.assertEqual(graph.e_size(), 12)

    def test_mc(self):
        graph = create_graph()
        self.assertEqual(graph.get_mc(), 39)
        for node in range(5):
            graph.remove_edge(node,node+1)
        self.assertEqual(graph.get_mc(), 44)
        graph.remove_node(15)
        graph.remove_node(18)
        self.assertEqual(graph.get_mc(), 50)


if __name__ == '__main__':
    unittest.main()
