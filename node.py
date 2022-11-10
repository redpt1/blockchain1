from block import *

class Node:
    def __init__(self):
        self.port = 0
        self.neighbor = []
        self.blockchain = Blockchain()

    def setPort(self,port):
        self.port = port
        self.neighbor.append(self.port)#把自己加进去

    def addNeighbor(self,neighbor):
        self.neighbor.append(neighbor)


def NewNode():
    new_node = Node()
    return new_node