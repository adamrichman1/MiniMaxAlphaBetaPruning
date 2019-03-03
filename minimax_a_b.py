import sys
from ast import literal_eval
from state import State


def read_config_file(filename):
    return [line.rstrip('\n') for line in open(filename)]


def parse_config(config):
    return literal_eval(config[0])


def build_graph(filename):
    node_data = parse_config(read_config_file(filename))
    init_node = State(node_data[0], None, "MAX")
    construct_nodes(init_node, node_data, "MAX")
    return init_node


def construct_nodes(node, node_data, node_type):
    node_type = "MIN" if node_type == "MAX" else "MAX"
    for element in node_data:
        if type(element) is str:
            pass
        elif type(element) is list:
            child = State(element[0], None, node_type)
            node.add_child(child)
            construct_nodes(child, element, node_type)
        elif type(element) is tuple:
            leaf = State(element[0], element[1], "NA")
            node.add_child(leaf)
        else:
            print(">>> ERROR: Invalid configuration file <<<")


def vanilla_minimax(node):
    visited = []
    best_val, visited = select_max(node, visited)
    return "\nOptimal Utility Value: " + str(best_val) + "\nVisited: " + str(visited) + "\n"


def select_max(node, visited):
    # Store visited node
    visited.append(node.get_node_id())

    # Base case
    if node.is_leaf():
        return node.get_value()

    # Initialize max val
    max_val = float('-inf')

    # Iterate through children and make mutually recursive call to select_min() for each child
    children = node.get_children()
    for i, child in enumerate(children):
        score = select_min(child, visited)

        # Update max val
        if score > max_val:
            max_val = score

    return max_val, visited


def select_min(node, visited):
    # Store visited node
    visited.append(node.get_node_id())

    # Base case
    if node.is_leaf():
        return node.get_value()

    # Initialize min val
    min_val = float('inf')

    # Iterate through children and make mutually recursive call to select_max() for each child
    children = node.get_children()
    for i, child in enumerate(children):
        score = select_max(child, visited)[0]

        # Update min val
        if score < min_val:
            min_val = score
    return min_val


def alpha_beta_pruning_minimax(node):
    visited = []
    best_val, visited = select_max_ab(node, float('-inf'), float('inf'), visited)
    return "\nOptimal Utility Value: " + str(best_val) + "\nVisited: " + str(visited) + "\n"


def select_max_ab(node, alpha, beta, visited):
    # Store visited node
    visited.append(node.get_node_id())

    # Base case
    if node.is_leaf():
        return node.get_value()

    # Initialize max val
    max_val = float('-inf')

    # Iterate through children and make mutually recursive call to select_min() for each child
    children = node.get_children()
    for i, child in enumerate(children):
        score = select_min_ab(child, alpha, beta, visited)

        # Save max val
        if score > max_val:
            max_val = score

        # Prune if possible
        if max_val >= beta:
            return max_val, visited

        # Update best alternative for MAX value (Alpha)
        if max_val > alpha:
            alpha = max_val

    return max_val, visited


def select_min_ab(node, alpha, beta, visited):
    # Store visited node
    visited.append(node.get_node_id())

    # Base case
    if node.is_leaf():
        return node.get_value()

    # Initialize min val
    min_val = float('inf')

    # Iterate through children and make mutually recursive call to select_max() for each child
    children = node.get_children()
    for i, child in enumerate(children):
        score = select_max_ab(child, alpha, beta, visited)[0]

        # Save min val
        if score < min_val:
            min_val = score

        # Prune if possible
        if min_val <= alpha:
            return min_val

        # Update best alternative for MIN value (Beta)
        if min_val < beta:
            beta = min_val

    return min_val


def main():
    # Get command line args
    args = sys.argv
    num_args = len(args)

    # Confirm number of arguments is correct
    if num_args != 2:
        print(">>> ERROR: Please specify valid command line arguments <<<")
        exit(0)

    # Read config
    init_node = build_graph(args[1])

    # Run vanilla MiniMax
    val = vanilla_minimax(init_node)
    print("\n---Vanilla Minimax---" + val)

    # Run alpha-beta pruning MiniMax
    val = alpha_beta_pruning_minimax(init_node)
    print("\n---Alpha Beta Pruning Minimax---" + val)


main()
