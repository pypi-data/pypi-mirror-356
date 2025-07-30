import unittest
from GraphePython import Graph

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.graph.add_node("A")
        self.graph.add_node("B")
        self.graph.add_edge("A", "B", 5)

    def test_add_node(self):
        self.graph.add_node("C")
        self.assertIn("C", self.graph.graph)

    def test_add_edge(self):
        self.graph.add_node("C")    
        self.graph.add_edge("A", "C", 10)
        self.assertIn("C", self.graph.graph["A"])
        self.assertEqual(self.graph.get_edge_weight("A", "C"), 10)

    def test_get_edge_weight(self):
        weight = self.graph.get_edge_weight("A", "B")
        self.assertEqual(weight, 5)

    def test_get_path(self):
        self.graph.add_node("C")
        self.graph.add_edge("A", "C", 10)
        self.graph.add_edge("B", "C", 5)
        self.graph.add_edge("A", "B", 25)
        path = self.graph.get_path("A", "B", True)
        self.assertEqual(path, ["A", "C", "B"])
        path = self.graph.get_path("A", "C", False)
        self.assertEqual(path, ["A", "C"])

    def test_save_graph(self) :
        self.graph.save_graph("test.txt", "tests/")

    def test_load_graph(self) :
        self.graph.load_graph("graph1.txt", "tests/")
        self.assertIn("A", self.graph.graph)
        self.assertIn("B", self.graph.graph["A"])

        self.graph.draw_graph([], "Here's the loaded graph")

    def test_generate_graph(self) :
        self.graph.generate_random_graph(15, 20, (0.5, 78))
        self.assertEqual(len(self.graph.get_graph_nodes()), 15)
        self.assertGreaterEqual(len(self.graph.G.edges), 20)
        self.graph.draw_graph([], "Here's the generated graph")

    def test_generate_graph_with_integer_weights(self) :
        self.graph.generate_random_graph(15, 20, (0.5, 78), integer=True)
        self.assertEqual(len(self.graph.get_graph_nodes()), 15)
        self.assertGreaterEqual(len(self.graph.G.edges), 20)
        self.graph.draw_graph([], "Here's the generated graph")


    def test_invalid_graph_generation(self):
        with self.assertRaises(ValueError):
            self.graph.generate_random_graph(5, 50)  # Too many edges for 5 nodes
    
    def test_large_graph(self):
        self.graph.generate_random_graph(1000, 5000, (1, 10))
        self.assertEqual(len(self.graph.get_graph_nodes()), 1000)
        self.assertGreaterEqual(len(self.graph.G.edges), 5000)


if __name__ == "__main__":
    unittest.main()