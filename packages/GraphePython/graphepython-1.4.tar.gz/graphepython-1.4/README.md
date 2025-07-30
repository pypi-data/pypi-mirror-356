# GraphePython

**GraphePython** is a Python library for creating and analyzing graphs. It provides an implementation of Dijkstra's algorithm to find the shortest path in an undirected graph, along with tools for graph visualization and random graph generation.

## Table of Contents

- [Functionalities](#functionalities)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Tests](#tests)
- [Example Codes](#example-codes)
  - [The Basics](#the-basics)
  - [Finding the Shortest Path](#finding-the-shortest-path)
  - [Random Graphs Generation](#random-graphs-generation)
  - [Saving and Loading Graphs](#saving-and-loading-graphs)
- [License](#license)

## Features

- Create graphs with nodes and weighted edges
- Find the shortest path in an undirected graph
- Visualize graphs with NetworkX and Matplotlib
- Generate random connected graphs

### Prerequisites

- Python 3.7 or higher
- You must have the following libraries installed :
  - `matplotlib` 3.0 or higher
  - `networkx` 2.0 or higher

## Installation

You can install **GraphePython** via pip by running the following command :

```bash
pip install GraphePython
```

### Tests

If you want to run some tests to check if the module is working correctly, you can use the tests in the tests folder and run the following command :

```bash
python -m unittest discover tests
```

## Exemple codes

### The basics

To use **GraphePython**, you first have to import it and create a new graph :

```python
import GraphePython as gp

graph = gp.Graph()
```

The next step is to add nodes to your graph. You can either add them one by one or from an array :

```python
graph.add_node("A") # Adding a single node
graph.add_nodes_from_array(["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]) # Adding all the nodes from B to K at once
```

Now that you have multiple nodes you can connect them by adding edges. Unlike nodes, edges can only be added one at a time :

```python
graph.add_edge("A", "B", 18) # Adds an edge from A to B (and from B to A) with a weight (or cost) of 18
graph.add_edge("A", "C", 22)
graph.add_edge("B", "C", 31)
graph.add_edge("C", "F", 17)
graph.add_edge("B", "E", 26)
graph.add_edge("B", "D", 12)
graph.add_edge("E", "F", 12)
graph.add_edge("D", "G", 24)
graph.add_edge("H", "G", 12)
graph.add_edge("H", "I", 7)
graph.add_edge("H", "K", 24)
graph.add_edge("K", "J", 18)
graph.add_edge("I", "J", 12)
graph.add_edge("F", "I", 13)
graph.add_edge("G", "E", 9)
```

You can also see your graph by setting the `draw` input to `True` or by calling the `draw_graph` function :

```python
graph.get_path("A", "K", draw=True) # Returns the shortest path and shows it in a Matplotlib window
graph.draw_graph(path = [], path_text = "Graph title") # This creates a new window. You can provide any path you want and it will be highlighted in red (e.g : ['A', 'B', 'E']) You can also provide a text that will be displayed above the graph in the window.
```

This should give you something like this :

![Figure : graph visualization exemple using Matplotlib](demo_images/GraphePython-demo.png)

### Finding the shortest path

You can get the shortest path between two nodes by using the `get_path` function :

```python
graph.get_path("A", "K", draw=False) # Returns the shortest path between A and K in an array here : ['A', 'C', 'F', 'I', 'J', 'K']
```

### Random graphs generation

You can also generate random graphs with **GraphePython**. Here's an example:

```python
import GraphePython as gp

# Create a new graph instance
graph = gp.Graph()

# Generate a random graph with the following parameters:
# - 10 nodes
# - 15 edges
# - Edge weights ranging from 1 to 10
# - Node naming method: LETTERS (nodes will be named A, B, C, ...)
graph.generate_random_graph(
    number_of_nodes=10,
    number_of_edges=15,
    weight_range=(1, 10),
    node_naming_method="LETTERS"
)

# Visualize the generated graph
graph.draw_graph(path=[], path_text="Randomly Generated Graph")

# Save the generated graph to a file
graph.save_graph("random_graph.txt", "myGraphs/")

# Load the graph back from the file (to verify saving/loading works)
graph.load_graph("random_graph.txt", "myGraphs/")
graph.draw_graph(path=[], path_text="Loaded Random Graph")
```

This will generate a random graph, visualize it, save it to a file, and reload it for further use.

### Saving and loading graphs

As mentioned above, you can save your graphs into text files :

```python
graph.save_graph("graph.txt", "myGraphs/") # This will save the current graph into the graph.txt file in the myGraphs folder
graph.load_graph("graph.txt", "myGraphs/") # This loads the previously saved graph
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
