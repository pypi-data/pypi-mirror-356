# This part of GraphePython is used for utility functions that are not directly related to the main Graph class

# Importing the stantard python library needed for the utility functions to work
import os
import enum
import random

# Main code

def get_file_path(relative_file_path : str, file_name : str) -> str :
    """
    This function is used to get a file absolute path on the user's computer

    Parameters :
    relative_file_path(str) : the relative path of the file from the script directory
    file_name(str) : the name of the file to get the path to

    Returns :
    final_file_path(str) : the path to the file
    """

    script_path = os.path.dirname(os.path.realpath('__file__'))
    final_file_path = os.path.join(script_path, relative_file_path, file_name)

    return final_file_path

class node_naming_method(enum.Enum) :
    LETTERS = 1
    NUMBERS = 2
    LIST = 3
    LIST_RANDOM = 4

def string_to_naming_method(source_string : str) -> node_naming_method :
    """
    This function  is used to convert a string to a naming method

    Parameters :
    source_string(str) : the string to convert

    Returns :
    (node_naming_method) : the method obained from the string
    """

    if source_string.lower() == "letters" :
        return node_naming_method.LETTERS
    if source_string.lower() == "numbers" :
        return node_naming_method.NUMBERS
    if source_string.lower() == "list" :
        return node_naming_method.LIST
    if source_string.lower() == "list_random" :
        return node_naming_method.LIST_RANDOM
    
    else :
        raise ValueError(f"Invalid source string value : {source_string}. Expected : letters, numbers, list or list_random")

def get_nodes_names_from_method(method : node_naming_method, number_of_nodes : int, *array : list[str]) -> list[str] :
    """
    This function generates a list of names for the nodes of the graph from a specified method.

    Parameters :
    method(node_naming_method) : the method that is used to generate the names. There are 4 types of method :
    - LETTERS will name the nodes in an alphabetical order and will continue with AA, AB, AC, ... if the number of nodes is greater than 26.
    - NUMBERS will name the nodes with the number from 1 to the number of nodes
    - LIST will name the nodes using a provided list of names in the array parameter
    - LIST_RANDOM will name the nodes using random names from a provided list of names in the array parameter
    number_of_nodes(int) : the number of nodes of the graph
    array(list[str]) : an optionnal argument that is only used for the LIST and LISY_RANDOM methods

    Returns :
    names(list[str]) : the list of names for the nodes
    """
    
    names = []
    
    if method.name == "LETTERS" :
        for n in range(number_of_nodes) :
            name = ""
            i = n
            while True :
                i, r = divmod(i, 26)
                name = chr(65 + r) + name # 65 is the ASCII code for A, then we offset it to get the right letter and adding the name to it to continue (Z, AA, AB, ...)

                if i == 0 :
                    break

                i -= 1 # Decrementing i to get the right letter (A, B, C, ...)
            names.append(name)

    if method.name == "NUMBERS" :
        names = [str(i + 1) for i in range(number_of_nodes)]

    if method.name == "LIST" :
        if not array or not array[0] :
            raise ValueError("The provided list of names is empty")
        
        if len(array[0]) < number_of_nodes :
            raise ValueError("The provided array is not long enough. If you want to pick random names among a list, you should try the LIST_RANDOM method.")
        
        else :
            names = [array[0][i] for i  in range(number_of_nodes)]

    if method.name == "LIST_RANDOM" :
        if not array or not array[0] :
            raise ValueError("The provided list of names is empty")
        
        else :
            names = [array[0][random.randint(0, len(array[0]) - 1)] for _ in range(number_of_nodes)]

    return names
        

