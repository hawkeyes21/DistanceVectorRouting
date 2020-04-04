class Error(Exception):
    """Base class for all other exceptions"""
    pass


class InvalidNeighbor(Error):
    """Raised when a neighbor node is not found in the list of nodes"""
    pass


class TooManyNeighbors(Error):
    """Raised when number of neighbors exceed the total neighbors"""
    pass


class NodeAlreadyPresent(Error):
    """Raised when the node is already present in the list of nodes, i.e. prevents repetition of nodes"""
    pass


class NullNodeName(Error):
    """Raised when the name of the node is empty or null"""
    pass