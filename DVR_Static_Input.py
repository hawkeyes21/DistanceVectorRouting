import time


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

        node_names = ['A', 'B', 'C', 'D', 'E']
        node_neighbors = ['B', 'A C E', 'B D', 'C E', 'B D']
        node_neighbors_dist = [[1], [1, 6, 3], [6, 2], [2, 4], [3, 4]]

        for n in range(len(node_names)):
            test = NodeStructure()
            test.set_node_name(node_names[n])
            self.nodes_list.append(test)

        for n in range(len(node_names)):
            self.nodes_list[n].set_neighbor(node_neighbors[n])

        for n in range(5):
            self.nodes_list[n].set_neighbor_distance(node_neighbors_dist[n])

        for n in self.nodes_list:
            n.set_next()
        
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
            print("-" * 40)
            print("Updating table of: {}... (neighbors: {})".format(working_node_name, working_node_neighbors))
            time.sleep(3)
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
                print("Exchanging tables between: {} and {}".format(working_node_name, neighbor_node_name))
                for _ in range(3):
                    print(".", end='')
                    time.sleep(1)
                for nn in neighbor_node_neighbors:
                    # all the checks are implemented.
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
                print("Exchange success...")
            time.sleep(1)
            print("Exchange complete for: {}".format(working_node_name))
            print("-" * 40)
            print("\n")
            time.sleep(3)

    def generate_final_routing_table(self):
        GenerateRoutingTables.pass_count += 1
        print("Starting exchange of routing tables soon. Iteration: {}".format(GenerateRoutingTables.pass_count))
        for _ in range(8):
            print(".", end='')
            time.sleep(1)
        print("\n")
        #  implementing bellman_ford_algorithm...
        self.implement_bellman_ford_algorithm()
        print("Iteration {} completed. Printing routing tables soon...".format(GenerateRoutingTables.pass_count))
        time.sleep(6)
        print("{} {}{} {}".format("*" * 34, "Iteration: ", GenerateRoutingTables.pass_count, "*" * 34))
        for i in self.nodes_dictionary.keys():
            print("{:81}{}".format("*", "*"))
            print("{:8}{}{:>8}".format("*", "*" * 66, "*"))
            print("{:8}{}{:>20}{}{}){:>23}{:>8}".format("*", "*", i, "'s Routing Table (i=", str(GenerateRoutingTables.pass_count), "*", "*"))
            print("{:8}{}{:>8}".format("*", "*" * 66, "*"))
            print("{:8}{} {:20} {:20} {:20} {}{:>8}".format("*", "*", "Destination", "Distance", "Next", "*", "*"))
            for j in range(len(self.nodes_dictionary)):
                node_obj = self.nodes_dictionary.get(i)
                node_name = self.nodes_list[j].get_node_name()
                node_dist = node_obj.get_neighbor_distance()[j]
                node_next = node_obj.get_next()[j]
                if node_next == '\0':
                    node_next = "NULL"
                print("{:8}{} {:20} {:20} {:20} {}{:>8}".format("*", "*", node_name, str(node_dist), node_next, "*", "*"))
            print("{:8}{}{:>8}".format("*", "*" * 66, "*"))
        print("{:81}{}".format("*", "*"))
        print("*" * 82)


def main():
    nodes = []
    input_obj = GetData(nodes)
    nodes = input_obj.get_data_from_user()
    dvr_obj = GenerateRoutingTables(nodes)
    # dvr_obj.implement_bellman_ford_algorithm()
    dvr_obj.generate_initial_routing_table()
    for iter_count in range(3):
        dvr_obj.generate_final_routing_table()


if __name__ == '__main__':
    main()
