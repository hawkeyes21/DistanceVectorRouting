class NodeStructure:
    """
    This class defines the structure of each node.
    Properties like NodeName, NodeNeighbors, NeighborDistance are specified.
    """

    list_of_nodes = []

    def __init__(self):
        self._neighbors = []
        self._neighbors_distance = []
        self._node_name = "random_name"

    def set_node_name(self, name):
        self._node_name = name
        NodeStructure.list_of_nodes.append(name)  # LIST IS NOT SAME FOR ALL INSTANCES!
        print("NodeStructure value after adding {}: {}".format(name, NodeStructure.list_of_nodes))

    def set_neighbor(self, neighbors):
        neighbors = neighbors.split(' ')
        for neighbor in neighbors:
            if neighbor in NodeStructure.list_of_nodes:
                self._neighbors.append(neighbor)
            # else:
            #     print("{} node not found!".format(neighbor))

    def set_neighbor_distance(self, neighbors_distance):
        neighbors_distance = neighbors_distance.split(' ')
        count = 0
        print(NodeStructure.list_of_nodes)  # ***** some problem here **********
        for neighbor in NodeStructure.list_of_nodes:
            if neighbor == self.get_node_name():
                self._neighbors_distance.append('0')  # self-node = 0 distance
            elif neighbor in self.get_neighbors():
                self._neighbors_distance.append(neighbors_distance[count])
                count = count + 1
            else:
                self._neighbors_distance.append('-1')  # -1 = infinite distance

    def get_node_name(self):
        return self._node_name

    def get_neighbors(self):
        return self._neighbors

    def get_neighbor_distance(self):
        return self._neighbors_distance

class Test:
    def __init__(self):
        pass

    def get_list_of_nodes(self):
        return NodeStructure.list_of_nodes

def main():
    nodes = []
    nodes_name = ['A', 'B', 'C', 'D', 'E']
    nodes_neighbors = ['B', 'C E', 'B D', 'C E', 'B D']
    nodes_distance = ['2', '4 3', '4 6', '6 5', '3 5']
    for n in range(5):
        test = NodeStructure()
        test.set_node_name(nodes_name[n])

        # test.set_neighbor(nodes_neighbors[n])
        # test.set_neighbor_distance(nodes_distance[n])
        nodes.append(test)
    print("Final NodeStructure value through node {} from main(): {}".format(nodes[0].get_node_name(), nodes[0].list_of_nodes))
    print("Final NodeStructure value through node {} from main(): {}".format(nodes[1].get_node_name(), nodes[1].list_of_nodes))
    print("Final NodeStructure value through node {} from main(): {}".format(nodes[2].get_node_name(), nodes[2].list_of_nodes))
    print("Final NodeStructure value through node {} from main(): {}".format(nodes[3].get_node_name(), nodes[3].list_of_nodes))
    print("Final NodeStructure value through node {} from main(): {}".format(nodes[4].get_node_name(), nodes[4].list_of_nodes))
    test1 = Test()
    print("NodeStructure value through another class main(): {}".format(test1.get_list_of_nodes()))

if __name__ == '__main__':
    main()