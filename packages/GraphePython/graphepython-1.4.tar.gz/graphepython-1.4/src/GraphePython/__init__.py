# Importing necessary libraries
import matplotlib.pyplot as plt
import networkx as nx
import json
from . import utils
import random
import math

# This program is an implementation of Dijkstra's algorithm to find the shortest path in a graph.
# The graph is represented as a dictionary, and the program uses NetworkX for visualisation.
# A graph is a collection of nodes that are connected by edges.
# Each edge has a weight, which represents the cost of traversing that edge.
# A graph can be oriented which means that an edge can go from A to B but not necessary from B to A.
# It can also be undirected which means that all edges go in both directions.
# Here, to simplify the implementation of the algorithm, the graph is undirected
# The following class is used to initialize the graph. You can then run functions on it to add nodes and edges, and to find the shortest path between two nodes.
# You can also visualize the graph and the shortest path between two nodes.
class Graph :
    # Function to initialize the graph's properties
    def __init__(self):
        self.graph = {} # Dictionary to store the graph properties
        self.path_graph = {} # Dictionary to store the shortest path from a node to all other nodes e.g : {A : {A : 0, B : 45, C : 12}, etc...}
        self.G = nx.Graph()
        self.edges_labels = {}
        self.figure = plt.Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111)

    # Function to add a single node which name is a string. A graph cannot have two nodes with the same name
    def add_node(self, node : str) -> None:
        """
        Adds a single node to the graph.

        Parameters:
        node (str): The name of the node to be added.

        Returns:
        None
        """

        if not node in self.graph : # Check if the node is not already in the graph
            # Initialize the properties of the node
            self.graph[node] = {}
            self.path_graph[node] = {}
            self.G.add_node(node)
        
        return

    # Function to add multiple nodes at once from an array which contains all nodes names
    def add_nodes_from_array(self, nodes : list[str]) -> None:
        """
        Adds multiple nodes to the graph from an array.

        Parameters:
        nodes (list[str]): The list of node names to be added.

        Returns:
        None
        """
        for node in nodes :
            self.add_node(node) # Call the function to add a single node for each node in the array

        return

    # Function to add an edge between two nodes with the provided weight
    def add_edge(self, node1 : str, node2 : str, weight : float) -> None:
        """
        Adds an edge between two nodes with the specified weight.
        
        Parameters:
        node1 (str): The name of the first node.
        node2 (str): The name of the second node.
        weight (float): The weight of the edge between the two nodes.

        Returns:
        None
        """

        if node1 in self.graph and node2 in self.graph : # Check if both nodes are in the graph
            # Add the edge to the graph and add a label for the weight of the edge to be seen in the graph visualization
            self.graph[node1][node2] = weight
            self.graph[node2][node1] = weight
            self.G.add_edge(node1, node2, weight = weight)
            self.edges_labels[(node1, node2)] = round(weight, 1) # Rounding the shown weight to 1 digit to avoid messy graph display when drawing it
        
        return

    # Function to get the weight of a provided edge between two nodes. If the edge doesn't exit it returns 0
    def get_edge_weight(self, node1 : str, node2 : str) -> int:
        if node1 in self.graph and node2 in self.graph and self.graph.get(node1).get(node2) is not None:
            return int(self.graph.get(node1).get(node2))

        else :
            return 0
        
    def get_graph_nodes(self) :
        return list(self.graph.keys())

    # Function to get all edges from a node
    def get_neighbors(self, node : str) -> list[str]:
        """
        Returns all naighbors of a node.

        Parameters:
        node (str): The name of the node.

        Returns:
        list[str]: A list of edges from the node.
        """

        if node in self.graph :
            return self.graph.get(node)
        
        else :
            return []

    # Function to visualize the graph and a path between two nodes
    def draw_graph(self, path : list[str], path_text : str) -> None:
        """
        Draws the graph and highlights the path between two nodes.

        Parameters:
        path (list[str]): The list of nodes representing the path.
        path_text (str): The text to be displayed as the title of the graph.

        Returns:
        None
        """

        self.ax.clear() # Make sure the figure is empty before drawing the graph

        # Store all the edges in the path to highlight them
        path_edges = []
        for node1, node2 in zip(path, path[1:]):  # Iterate over consecutive pairs of nodes
            if node1 in self.graph and node2 in self.graph[node1]:  # Check if the edge is in the graph
                path_edges.append((node1, node2))

        other_edges = self.G.edges() - path_edges # Storing all the edges that are not in the path to draw them in a different color
        
        pos = nx.spring_layout(self.G) # Initializing the graph layout
        nx.draw_networkx_nodes(self.G, pos) # Drawing the nodes
        nx.draw_networkx_labels(self.G, pos) # Adding labbels to each node
        nx.draw_networkx_edges(self.G, pos, edgelist=other_edges, edge_color='black', arrows=True) # Drawing the edges that are not in the path in black
        nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='r', arrows=True) # Drawing the edges in the path in red after the other edges to avoid some errors due to order in the pairs of the nx graph (e.g : ('A', 'B') and ('B', 'A'))
        nx.draw_spring(self.G, with_labels=True, font_weight='bold', ax=self.ax) # Drawing the graph
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=self.edges_labels) # Adding the weight labels to the edges

        plt.suptitle(t=path_text, fontsize=14) # Adding the graph title

        plt.show()

        return

    # Function to find the shortest path between two nodes using Dijkstra's algorithm
    def get_path(self, start : str, finish : str, draw : bool) -> list[str]:
        """
        Finds the shortest path between two nodes using Dijkstra's algorithm.

        Parameters:
        start (str): The name of the starting node.
        finish (str): The name of the ending node.

        Returns :
        path (list[str]) : The list of nodes representing the shortest path between the two nodes.
        """

        if start in self.path_graph and finish in self.path_graph[start] : # Check if the path between the two nodes is already calculated
            path = []
            predecessor = self.path_graph[start][1] # Get the predecessors of the nodes
            weights = self.path_graph[start][0] # Get the weights of the nodes
            path.insert(0, finish) # Add the finish node to the path

            while path[0] != start :
                path.insert(0, predecessor[path[0]])

            if draw :
                # Drawing the graph with the path between the two nodes
                self.draw_graph(
                    path_text=f"The shortest path between {start} and {finish} is {path} that costs {weights[finish]}", path=path)
            
            return path # Return the path if it is already calculated

        # Initializing the variables
        queue = []
        weights = {}
        
        for i in self.graph.keys() : # Adding all the nodes in the queue except the start node
            weights[i] = float("inf") # Initializing the weight of each node to infinity
            queue.append(i)

        
        weights[start] = 0
        path = []
        predecessor = {}

        # Main loop that executes until it has gone through all the nodes to find the shortest path from the start node
        while queue :
            current_node = queue[0]
            neighbors = self.get_neighbors(current_node)
            for neighbor in neighbors :
                # Adding the edge into the weight dictionary if it is not already present
                if not neighbor in weights :
                    weights[neighbor] = self.get_edge_weight(current_node, neighbor) + weights[current_node]
                    predecessor[neighbor] = current_node

                # Updating the cost of the current edge if we find a shorter path and adding the current edge and node into the queue to reprocess them
                elif (neighbor in weights) and (current_node in weights) :
                    if weights[neighbor] > self.get_edge_weight(current_node, neighbor) + weights[current_node] :
                        weights[neighbor] = self.get_edge_weight(current_node, neighbor) + weights[current_node]
                        queue.insert(0, neighbor)
                        queue.insert(0, current_node)
                        predecessor[neighbor] = current_node

            # Removing the current node from the queue and adding the next node to process
            queue.remove(current_node)
            if current_node == finish :
                break
            max_distance = max(weights.values())
            for node in weights :
                if weights[node] == max_distance and node not in queue :
                    queue.insert(0, node)

        path.insert(0, finish)

        while path[0] != start :
            path.insert(0, predecessor[path[0]])

        self.path_graph[start] = (weights, predecessor) # Storing the path data to be able to use it later if needed
        
        # If the path is empty, it means that there is no path between the two nodes

        if draw :
            # Drawing the graph with the path between the two nodes
            self.draw_graph(
                path_text=f"The shortest path between {start} and {finish} is {path} that costs {weights[finish]}", path=path)

        return path
    
    # Function to save the graph
    def save_graph(self, name : str, path : str = "") -> None :
        """
        Saves the graph to a text file in the provided path

        Parameters :
        path(str) : the path for the file to be saved
        name(str) : the name of the file to save the graph to (default : "" which means that the file will be saved to the current directory)


        Returns : 
        None
        """
        file = open((utils.get_file_path(path, name) if path != "" else name), "w")

        file.write(json.dumps(self.graph))

        return
    
    # Function to load a graph
    def load_graph(self, name : str, path : str = "") -> None :
        """
        Loads a graph from a text file in the provided path

        Parameters :
        name(str) : the name of the text file to be loaded
        path(str) : the path of the file to be loaded from (default : "" which means that the file will be loaded from the current directory)

        Returns :
        None
        """

        file = open((utils.get_file_path(path, name) if path != "" else name), "r").read()

        # Resets the graph
        self.graph = {}
        self.path_graph = {}
        self.G = nx.Graph()
        self.edges_labels = {}

        loaded_graph = dict(json.loads(file))

        for node in loaded_graph.keys() :
            self.add_node(node)

            for neighbour in loaded_graph[node] :
                self.add_edge(node, neighbour, loaded_graph[node][neighbour])

        return

    # Function to generate a random connected graph
    def generate_random_graph(self, number_of_nodes : int, number_of_edges : int, weight_range : tuple[float, float] = (1, 5), node_naming_method : str = "letters", array : list[str] = [], integer : bool = False) -> None:
        """
        This function allows you to generate random graphs that will always be connected. This ensures that you can find a path between two nodes

        Parameters :
        number_of_nodes(int) : the desired number of nodes for the graph
        number_of_edges(int) : the desired number of edges for the graph
        weight_range(tuple[float, float]) : the minimum and maximum weight for the graph edges (default : (1, 5))
        node_naming_method(str) : the method that should be used to name the nodes of the graph. There are 4 types of naming method :
        - LETTERS will name the nodes in an alphabetical order and will continue with AA, AB, AC, ... if the number of nodes is greater than 26.
        - NUMBERS will name the nodes with the number from 1 to the number of nodes
        - LIST will name the nodes using a provided list of names in the array parameter
        - LIST_RANDOM will name the nodes using random names from a provided list of names in the array parameter
        array(list[str]) : the list of names to be used if the naming method is either LIST or LIST_RANDOM
        integer(bool) : defines weither or not the random weights should be rounded to nearest intager or be float(2 digits), default is false(float weights)

        Returns :
        None
        """

        if number_of_edges not in range(number_of_nodes - 1, math.ceil((number_of_nodes*(number_of_nodes - 1))/2)) : # Checks if the number of edges is valid (not too high or too low)
            raise ValueError("Invalid number of edges")
        
        nodes_names = utils.get_nodes_names_from_method(utils.string_to_naming_method(node_naming_method), number_of_nodes, array)
        
        # Resets the graph
        self.graph = {}
        self.path_graph = {}
        self.G = nx.Graph()
        self.edges_labels = {}

        not_visited_nodes, visited_nodes = nodes_names, list()
        self.add_nodes_from_array(nodes_names)

        # Pick a random node and mark as visited, then set it as the current node
        current_node = random.sample(not_visited_nodes, 1).pop()
        not_visited_nodes.remove(current_node)
        visited_nodes.append(current_node)
        existing_edges = []

        while not_visited_nodes :
            # Randomly pick the next node to visit. This node will be one of the neighbors of the current node.
            # If this node has not already been visited, we create a new edge between this node and the current node.

            neighbor_node = random.sample(not_visited_nodes, 1).pop()

            if neighbor_node not in visited_nodes :
                self.add_edge(current_node, neighbor_node, int(random.uniform(weight_range[0], weight_range[1])) if integer else random.uniform(weight_range[0], weight_range[1]))
                existing_edges.append((current_node, neighbor_node))
                existing_edges.append((neighbor_node, current_node))

                not_visited_nodes.remove(neighbor_node)
                visited_nodes.append(neighbor_node)
            
            # Set the new neighbor node to the current node
            current_node = neighbor_node

        nodes = self.get_graph_nodes()
        max_attemps = 1000000
        attemps = 0
        # Add random edges until the desired number is reached
        while len(existing_edges) / 2 < number_of_edges : # We divide the length by two because each edge is represented as 2 differents tuples in existing edges
            # Pick two random nodes
            node1 = random.sample(nodes, 1).pop()
            node2 = random.sample(nodes, 1).pop()

            # Check if there is already an edge between the two nodes and if the nodes are different
            if (node1, node2) not in existing_edges and node1 != node2:
                self.add_edge(node1, node2, int(random.uniform(weight_range[0], weight_range[1])) if integer else random.uniform(weight_range[0], weight_range[1]))
                existing_edges.append((node1, node2))
                existing_edges.append((node2, node1))
            attemps += 1

            if attemps == max_attemps :
                raise Warning("Could not add all edges to the graph due to saturation")

        return
