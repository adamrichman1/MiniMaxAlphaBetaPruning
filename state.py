class State:
    def __init__(self, node_id, value, node_type):
        self.node_id = node_id
        self.value = value
        self.children = []
        self.node_type = node_type

    def __str__(self):
        child_string = ""
        children = ""
        for i, child in enumerate(self.children):
            child_string += State.__get_child_string(child)
            if i < len(self.children) - 1:
                child_string += ", "
            children += str(child)
        return ("(" + self.node_id + ")" if self.value is None else "(" + self.node_id + ", " + str(self.value) + ")") \
               + " --> " + child_string + "\n" + children

    @staticmethod
    def __get_child_string(node):
        node_id = node.get_node_id()
        val = node.get_value()
        return "(" + node_id + ")" if val is None else "(" + node_id + ", " + str(val) + ")"

    def get_children(self):
        return self.children

    def add_child(self, state):
        self.children.append(state)

    def get_value(self):
        return self.value

    def get_node_id(self):
        return self.node_id

    def is_leaf(self):
        return self.value is not None

    def get_node_type(self):
        return self.node_type
