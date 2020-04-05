import ExceptionList


class NodeStructure:
    """
    This class defines the structure of each node.
    Properties like NodeName, NodeNeighbors, NeighborDistance are specified.
    """
    # Static variable, which contains names of all the nodes in the network
    list_of_nodes = []

    def __init__(self):
        self.neighbors = []
        self.neighbors_distance = []
        self.node_name = "random_name"
        self.node_next = []

    def set_node_name(self, name):
        self.node_name = name
        NodeStructure.list_of_nodes.append(name)  # adding the name of the node inside the static variable

    # change input to *neighbors, and make a list from that
    def set_neighbor(self, neighbors):
        """ It is expected that the user will SPECIFY proper neighbor list for each node, in proper order."""
        neighbors = neighbors.split()
        for n in NodeStructure.list_of_nodes:
            if n in neighbors:
                self.neighbors.append(n)
            else:
                self.neighbors.append("\0")
            # self.node_next.append("\0")

    # change input to *neighbors_distance, and make a list from that
    def set_neighbor_distance(self, neighbors_distance):
        # neighbors_distance = neighbors_distance.split(' ')
        count = 0
        for neighbor in NodeStructure.list_of_nodes:
            if neighbor == self.get_node_name():
                self.neighbors_distance.append(0)  # self-node = 0 distance
            elif neighbor in self.get_neighbors():
                self.neighbors_distance.append(int(neighbors_distance[count]))
                count = count + 1  # the count should be incremented only here because the input of distances from user
                # will not contain -1's and 0's i.e. n(distance) = n(neighbors)
            else:
                self.neighbors_distance.append(-1)  # -1 = infinite distance

    def set_next(self):
        count = 0
        for n in self.list_of_nodes:
            if n in self.neighbors or n == self.get_node_name():
                self.node_next.append(n)
            else:
                self.node_next.append("\0")
        # for n in self.list_of_nodes:
        #     if n == self.node_name or n in self.neighbors:
        #         self.node_next.append(n)
        #     else:
        #         self.node_next.append('\0')
        #     count = count + 1

    def get_node_name(self):
        return self.node_name

    def get_neighbors(self):
        return self.neighbors

    def get_neighbor_distance(self):
        return self.neighbors_distance

    def get_next(self):
        return self.node_next

    def get_node_instance(self, node_name):
        if node_name == self.get_node_name():
            return self


class GetData:
    """ Gets the network data from user
        Input constraints and checks are taken care of here
    """
    def __init__(self, nodes_list):
        self.nodes_list = nodes_list

    def get_data_from_user(self):
        n = 0
        while True:
            try:
                n = int(input("How many nodes in the network?: "))
                if n < 0:
                    raise ValueError
                print(type(n))
                break
            except ValueError:
                print(">>ERROR: Enter a positive integer!")
                continue

        print("***** GETTING NODE NAMES ******")
        for i in range(n):
            test = NodeStructure()
            while True:
                try:
                    node_name = input("Enter name for node {}: ".format(i+1)).strip()
                    if node_name in test.list_of_nodes:
                        raise ExceptionList.NodeAlreadyPresent
                    if node_name == '' or node_name == "\0":
                        raise  ExceptionList.NullNodeName
                    test.set_node_name(node_name)
                    self.nodes_list.append(test)
                    break
                except ExceptionList.NodeAlreadyPresent:
                    print("Node with same name already present! Try again...")
                    continue
                except ExceptionList.NullNodeName:
                    print("Invalid Node Name! Try again...")
                    continue
        print("***** GETTING NODE NEIGHBORS ******")
        for i in range(n):
            while True:
                node_neighbors = input("Enter neighbors for node {} (space separated, in proper order e.g. a b c): ".format(self.nodes_list[i].get_node_name()))
                n_n_list = node_neighbors.split()
                try:

                    if len(n_n_list) > n-1:
                        raise ExceptionList.TooManyNeighbors
                    for nn in n_n_list:
                        if nn not in NodeStructure.list_of_nodes:
                            raise ExceptionList.InvalidNeighbor
                    if len(n_n_list) != len(set(n_n_list)):
                        raise ExceptionList.NodeAlreadyPresent
                    self.nodes_list[i].set_neighbor(node_neighbors)
                    break
                except ExceptionList.NodeAlreadyPresent:
                    print("Repetition of nodes not allowed! Try again...")
                    continue
                except ExceptionList.TooManyNeighbors:
                    print("Number of neighbors exceed total nodes! Try again...")
                    continue
                except ExceptionList.InvalidNeighbor:
                    print("One of the neighbor node not found in the network! Try again...")
                    continue

        print("***** GETTING NODE NEIGHBORS DISTANCE ******")
        for i in range(n):
            neighbor_list = []
            for j in self.nodes_list[i].get_neighbors():
                if j == "\0":
                    continue
                while True:
                    try:
                        dist = int(input("Distance: {} to {}: ".format(self.nodes_list[i].get_node_name(), j)))
                        if dist <= 0:
                            raise ValueError
                        neighbor_list.append(dist)
                        break
                    except ValueError:
                        print("Invalid distance! Try again...")
                        continue
            self.nodes_list[i].set_neighbor_distance(neighbor_list)
        for nn in self.nodes_list:
            nn.set_next()
        print("All set...")
        return self.nodes_list


class GenerateRoutingTables:
    """
    Prints initial Routing table
    Also prints the routing tables after the neighbor nodes have exchanged data
    """
    pass_count = 0

    def __init__(self, nodes_list):
        """
        Initialize the node_list and create a dictionary of nodes
        :param nodes_list: a list of NodeStructure() objects obtained from main() method
        """
        self.nodes_list = nodes_list
        self.nodes_dictionary = dict()
        for n in self.nodes_list:
            self.nodes_dictionary[n.get_node_name()] = n

    # def create_node_dict(self):
    #     for n in self.nodes_list:
    #         self.nodes_dictionary[n.get_node_name()] = n

    def generate_initial_routing_table(self):
        # print("*"*102)
        for i in self.nodes_dictionary.keys():
            print("*" * 66)
            print("{} {:>20}{} {:>19}".format("*", i, "'s initial routing table", "*"))
            print("*" * 66)
            # print("*"*102)
            print("{} {:20} {:20} {:20} {}".format("*", "Destination", "Distance", "Next", "*"))
            for j in range(len(self.nodes_dictionary)):
                node_obj = self.nodes_dictionary.get(i)
                node_name = self.nodes_list[j].get_node_name()
                node_dist = node_obj.get_neighbor_distance()[j]
                node_next = node_obj.get_next()[j]
                if node_next == "\0":
                    node_next = "NULL"
                print("{} {:20} {:20} {:20} {}".format("*", node_name, str(node_dist), node_next, "*"))
            print("*" * 66)
            print("\n")

    def implement_bellman_ford_algorithm(self):
        for current_node in self.nodes_list:
            working_node_name = current_node.get_node_name()
            working_node_neighbors = current_node.get_neighbors()
            working_node_neighbors_dist = current_node.get_neighbor_distance()
            for n in working_node_neighbors:
                if n == '\0':
                    continue
                count = 0
                neighbor_node_instance = self.nodes_dictionary[n]
                neighbor_node_name = neighbor_node_instance.get_node_name()
                neighbor_node_neighbors = neighbor_node_instance.get_neighbors()
                neighbor_node_distance = neighbor_node_instance.get_neighbor_distance()
                neighbor_node_hops = neighbor_node_instance.get_next()
                distance_to_working_node = neighbor_node_distance[neighbor_node_neighbors.index(working_node_name)]
                for nn in neighbor_node_neighbors:
                       # A to A                           A to B, B to A
                    if nn == working_node_name or neighbor_node_distance[count] == 0 or neighbor_node_distance[count] == -1 or neighbor_node_hops[count] == working_node_name:
                        count = count + 1
                        continue
                    else:
                        temp_dist = distance_to_working_node + neighbor_node_distance[count]
                        if working_node_neighbors_dist[count] == -1 or temp_dist < working_node_neighbors_dist[count]:
                            updated_node = self.nodes_dictionary[working_node_name]
                            updated_node.neighbors_distance[count] = temp_dist
                            updated_node.node_next[count] = neighbor_node_name
                            self.nodes_dictionary[working_node_name] = updated_node
                        count = count + 1

    def generate_final_routing_table(self):
        self.implement_bellman_ford_algorithm()
        GenerateRoutingTables.pass_count += 1
        # for i, j in self.nodes_dictionary.items():
        #     print("{} Neighbors: {} Neighbor_dist: {} Next: {}".format(j.get_node_name(), j.get_neighbors(),
        #                                                                j.get_neighbor_distance(), j.get_node_hops()))
        for i in self.nodes_dictionary.keys():
            print("*" * 66)
            print("{} {:>20}{}{} {:>19}".format("*", i, "'s final routing table(pass=", str(GenerateRoutingTables.pass_count), "*"))
            print("*" * 66)
            # print("*"*102)
            print("{} {:20} {:20} {:20} {}".format("*", "Destination", "Distance", "Next", "*"))
            for j in range(len(self.nodes_dictionary)):
                node_obj = self.nodes_dictionary.get(i)
                node_name = self.nodes_list[j].get_node_name()
                node_dist = node_obj.get_neighbor_distance()[j]
                node_next = node_obj.get_next()[j]
                if node_next == '\0':
                    node_next = "NULL"
                print("{} {:20} {:20} {:20} {}".format("*", node_name, str(node_dist), node_next, "*"))
            print("*" * 66)
            print("\n")


def main():
    nodes = []
    input_obj = GetData(nodes)
    nodes = input_obj.get_data_from_user()
    dvr_obj = GenerateRoutingTables(nodes)
    # dvr_obj.implement_bellman_ford_algorithm()
    dvr_obj.generate_initial_routing_table()
    dvr_obj.generate_final_routing_table()
    dvr_obj.generate_final_routing_table()
    dvr_obj.generate_final_routing_table()


if __name__ == '__main__':
    main()
