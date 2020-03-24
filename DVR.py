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
        self._node_hops = []

    def set_node_name(self, name):
        self._node_name = name
        NodeStructure.list_of_nodes.append(name)  # adding the name of the node inside the static variable

    # change input to *neighbors, and make a list from that
    def set_neighbor(self, neighbors):
        """ It is expected that the user will SPECIFY proper neighbor list for each node, in proper order."""
        neighbors = neighbors.split(' ')
        for n in NodeStructure.list_of_nodes:
            if n in neighbors:
                self._neighbors.append(n)
            else:
                self._neighbors.append("\0")
            self._node_hops.append("\0")
        # for neighbor in neighbors:
        #     # need to set certain conditions like - is the neighbor present in the network?, neighbor repetition, etc.
        #     self._neighbors.append(neighbor)

    # change input to *neighbors_distance, and make a list from that
    def set_neighbor_distance(self, neighbors_distance):
        neighbors_distance = neighbors_distance.split(' ')
        count = 0
        for neighbor in NodeStructure.list_of_nodes:
            if neighbor == self.get_node_name():
                self._neighbors_distance.append(0)  # self-node = 0 distance
            elif neighbor in self.get_neighbors():
                self._neighbors_distance.append(int(neighbors_distance[count]))
                count = count + 1  # the count should be incremented only here because the input of distances from user
                # will not contain -1's and 0's i.e. n(distance) = n(neighbors)
            else:
                self._neighbors_distance.append(-1)  # -1 = infinite distance

    def get_node_name(self):
        return self._node_name

    def get_neighbors(self):
        return self._neighbors

    def get_neighbor_distance(self):
        return self._neighbors_distance

    def get_node_hops(self):
        return self._node_hops

    def get_node_instance(self, node_name):
        if node_name == self.get_node_name():
            return self


class GenerateRoutingTables:
    """
    Prints initial Routing table
    Also prints the routing tables after the neighbor nodes have exchanged data
    """
    def __init__(self, nodes_list):
        self.nodes_list = nodes_list
        self.nodes_dict = dict()

    def create_node_dict(self):
        for n in self.nodes_list:
            self.nodes_dict[n.get_node_name()] = n

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
                else:
                    print("{:<20}{:<20}{:<20}".format(node_name, j, node_neighbors_distance[k]))
                k = k + 1  # k gets incremented here because the 'node_neighbors_distance' contains all the distances
                # i.e. -1's, 0's and the actual neighbor distance.
            print("{}\n".format("*" * 60))

    def implement_bellman_ford_algorithm(self):
        for current_node in self.nodes_list:
            working_node_name = current_node.get_node_name()
            working_node_neighbors = current_node.get_neighbors()
            working_node_neighbors_dist = current_node.get_neighbor_distance()
            working_node_hops = current_node.get_node_hops()
            for n in working_node_neighbors:
                if n == '\0':
                    continue
                count = 0
                neighbor_node_instance = self.nodes_dict[n]
                neighbor_node_name = neighbor_node_instance.get_node_name()
                neighbor_node_neighbors = neighbor_node_instance.get_neighbors()
                neighbor_node_distance = neighbor_node_instance.get_neighbor_distance()
                distance_to_working_node = neighbor_node_distance[neighbor_node_neighbors.index(working_node_name)]
                for nn in neighbor_node_neighbors:
                    if nn == '\0' or nn == neighbor_node_name or nn == working_node_name:
                        count = count + 1
                        continue
                    else:
                        if working_node_neighbors_dist[count] == -1:
                            temp_instance = self.nodes_dict[working_node_name]
                            temp_instance._neighbors_distance[count] = distance_to_working_node + neighbor_node_distance[count]
                            temp_instance._node_hops[count] = neighbor_node_name
                            self.nodes_dict[working_node_name] = temp_instance
                            count = count + 1
                        else:
                            temp_dist = distance_to_working_node + neighbor_node_distance[count]
                            if temp_dist < working_node_neighbors_dist[count]:
                                temp_instance = self.nodes_dict[working_node_name]
                                temp_instance._neighbors_distance[count] = temp_dist
                                temp_instance._node_hops[count] = neighbor_node_name
                                self.nodes_dict[working_node_name] = temp_instance
                                count = count + 1
                        pass

    def generate_final_routing_table(self):
        self.implement_bellman_ford_algorithm()
        for i, j in self.nodes_dict.items():

            print("{} Neighbbors: {} Neighbor_dist: {} Hops: {}".format(j.get_node_name(), j.get_neighbors(), j.get_neighbor_distance(), j.get_node_hops()))

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
def main():
    nodes_neighbors = ['B', 'A C E', 'B D', 'C E', 'B D']
    nodes_distance = ['2', '2 4 3', '4 6', '6 5', '3 5']
    for n in range(5):  # append all the nodes and their names to the list.
        # IMPORTANT - DO NOT ADD NEIGHBORS AND DISTANCES AT THIS STAGE, BECAUSE ALL THE NODES HAVEN'T BEEN ADDED TO THE
        # LIST YET! IGNORING THE INSTRUCTION LEADS TO LOGICAL ERROR!
        test = NodeStructure()
        test.set_node_name(nodes_name[n])
        nodes.append(test)
    for n in range(5):  # Adding other relevant information about the nodes...
        nodes[n].set_neighbor(nodes_neighbors[n])
        nodes[n].set_neighbor_distance(nodes_distance[n])
    gen = GenerateRoutingTables(nodes)
    # gen.generate_initial_routing_table()
    gen.create_node_dict()
    gen.generate_final_routing_table()
    gen.generate_final_routing_table()
    gen.generate_final_routing_table()

if __name__ == '__main__':
    main()

