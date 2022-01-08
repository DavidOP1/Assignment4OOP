from src.Location import Location
from src import EdgeData
class NodeData:
    #dont dorget we need to think of a data structure to store o
    #Maybe have another dict the will store the nodes coming into this current node.
    Node:dict[int:EdgeData]={}
    InNode:dict[int:EdgeData]={}
    def __init__(self,x,y,z,id):
        self.id=id;
        self.location= Location(x,y,z)
        self.Node:dict[int:EdgeData]={}#This will store all edges coming out of node.
        self.InNode: dict[int:EdgeData] = {}#This will store all edges coming inside the node.
        #This dictionary will store data the following format : destination id of the edge : edgeData object.
    def getKey(self):
        return self.id
    def getLocation(self):
        return self.location
    def setLocation(self,p):
        self.location=p

