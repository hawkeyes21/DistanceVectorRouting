class NodeStructure:
    """
    This class defines the structure of each node.
    Properties like NodeName, NodeNeighbors, NeighborDistance are specified.
    """
    # Static variable, which contains names of all the nodes in the network
    list_of_nodes = []

    def __init__(self):
        self._neighbors = []
        self._neighbors_distance = []
        self._node_name = "random_name"

    def set_node_name(self, name):
        self._node_name = name
        NodeStructure.list_of_nodes.append(name)  # adding the name of the node inside the static variable

    def set_neighbor(self, neighbors):
        neighbors = neighbors.split(' ')
        for neighbor in neighbors:
            # need to set certain conditions like - is the neighbor present in the network?, neighbor repetition, etc.
            self._neighbors.append(neighbor)

    def set_neighbor_distance(self, neighbors_distance):
        neighbors_distance = neighbors_distance.split(' ')
        count = 0
        for neighbor in NodeStructure.list_of_nodes:
            if neighbor == self.get_node_name():
                self._neighbors_distance.append('0')  # self-node = 0 distance
            elif neighbor in self.get_neighbors():
                self._neighbors_distance.append(neighbors_distance[count])
                count = count + 1  # the count should be incremented only here because the input of distances from user
                # will not contain -1's and 0's i.e. n(distance) = n(neighbors)
            else:
                self._neighbors_distance.append('-1')  # -1 = infinite distance

    def get_node_name(self):
        return self._node_name

    def get_neighbors(self):
        return self._neighbors

    def get_neighbor_distance(self):
        return self._neighbors_distance


class GenerateRoutingTables:
    """
    Prints initial Routing table
    Also prints the routing tables after the neighbor nodes have exchanged data
    """
    def __init__(self, nodes_list):
        self.nodes_list = nodes_list
        self.nodes_dict = dict

    def generate_initial_routing_table(self):
        for i in range(5):
            k = 0
            node = self.nodes_list[i]
            node_name = node.get_node_name()
            node_neighbors = node.get_neighbors()
            node_neighbors_distance = node.get_neighbor_distance()
            print("{}".format("*" * 60))
            print("{:<10}{:>20} {:<20}{:>9}".format("*", 'NODE', node_name, "*"))
            print("{}".format("*" * 60))
            print("{:<20}{:<20}{:<20}".format("FROM", "TO", "DISTANCE"))
            for j in NodeStructure.list_of_nodes:
                if j == node_name:
                    print("{:<20}{:<20}{:<20}".format(node_name, node_name, node_neighbors_distance[k]))
                elif j in node_neighbors:
                    print("{:<20}{:<20}{:<20}".format(node_name, j, node_neighbors_distance[k]))
                else:
                    print("{:<20}{:<20}{:<20}".format(node_name, j, node_neighbors_distance[k]))
                k = k + 1  # k gets incremented here because the 'node_neighbors_distance' contains all the distances
                # i.e. -1's, 0's and the actual neighbor distance.
            print("{}\n".format("*" * 60))

    def print_routing_table(self):
        print("{}".format("*" * 50))
        print("{}   {}  {}  {}".format("*", "Name", "Distance", "Hop"))
        for node in self.nodes_list:
            pass


def main():
    nodes = []
    # n = int(input("Number of nodes: "))
    # print("***** GETTING NODE NAMES ******")
    # for i in range(n):
    #     test = NodeStructure()
    #     test.set_node_name(input("Enter name for node {}: ".format(i+1)))
    #     nodes.append(test)
    # print("***** GETTING NODE NEIGHBORS ******")
    # for i in range(n):
    #     nodes[i].set_neighbor(input("Enter neighbors for node {}: ".format(i+1)))
    # print("***** GETTING NODE NEIGHBORS DISTANCE ******")
    # for i in range(n):
    #     nodes[i].set_neighbor_distance(input("Enter neighbors distance for node {}: ".format(i+1)))
    # print("***** PRINTING STUFF ******")
    # for i in range(n):
    #     print("***** NODE {} *****".format(nodes[i].get_node_name()))
    #     print("NEIGHBORS: {} ".format(nodes[i].get_neighbors()))
    #     print("NEIGHBORS DISTANCE: {} ".format(nodes[i].get_neighbor_distance()))
    nodes_name = ['A', 'B', 'C', 'D', 'E']
    nodes_neighbors = ['B', 'C E', 'B D', 'C E', 'B D']
    nodes_distance = ['2', '4 3', '4 6', '6 5', '3 5']
    for n in range(5):  # append all the nodes and their names to the list.
        # IMPORTANT - DO NOT ADD NEIGHBORS AND DISTANCES AT THIS STAGE, BECAUSE ALL THE NODES HAVEN'T BEEN ADDED TO THE
        # LIST YET! IGNORING THE INSTRUCTION LEADS TO LOGIC ERROR!
        test = NodeStructure()
        test.set_node_name(nodes_name[n])
        nodes.append(test)
    for n in range(5):  # Adding other relevant information about the nodes...
        nodes[n].set_neighbor(nodes_neighbors[n])
        nodes[n].set_neighbor_distance(nodes_distance[n])
    gen = GenerateRoutingTables(nodes)
    gen.generate_initial_routing_table()


if __name__ == '__main__':
    main()

