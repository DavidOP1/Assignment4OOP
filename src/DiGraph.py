from src import GraphInterface
from src import NodeData
from src import EdgeData
import random
class DiGraph(GraphInterface.GraphInterface):
    #################################################################################################################################################
    # this dictionary will keep data in this format , id: Node object
    graph:dict[int:NodeData.NodeData]={}
    nodeCount=0
    edgeCount=0
    MC=0
    #################################################################################################################################################
    def __init__(self, graphNew=None):
        if graphNew==None:
          self.graph: dict[int:NodeData.NodeData] = {}
          self.nodeCount: int = 0
          self.edgeCount: int = 0
          self.MC: int = 0
        else:
          self.graph:dict[int:NodeData.NodeData]=graphNew.graph
          self.nodeCount:int=graphNew.nodeCount
          self.edgeCount:int=graphNew.edgeCount
          self.MC:int=graphNew.MC

    #################################################################################################################################################
    def getNode(self,id:int)->NodeData.NodeData:
        return self.graph.get(id)

    #################################################################################################################################################
    def getNodeDict(self)-> dict[int:NodeData.NodeData]:
        return self.graph

    #################################################################################################################################################
    def getEdge(self,src:int,dest:int):
        node:NodeData=self.graph.get(src)
        return node.Node.get(dest)

    #################################################################################################################################################
    def v_size(self)-> int:
        return len(self.graph)

    #################################################################################################################################################
    def e_size(self)->int:
        return self.edgeCount

    #################################################################################################################################################
    def get_all_v(self)-> dict:# return dict {node id : tuple(number of nodes in , number of nodes out)} , write it in the read me! REMEMEBER!
     ret={}
     for key in self.graph:
        ret[key]="{0}: |edges_out| {1} |edges in| {2}".format(key,len(self.graph.get(key).Node),len(self.graph.get(key).InNode))
     return ret
    #################################################################################################################################################
    def all_in_edges_of_node(self, id1: int) -> dict:
        edgeDict={}
        for key in self.graph.get(id1).InNode:
            edgeDict[key]=self.graph.get(id1).InNode.get(key).getWeight()
        return edgeDict

    #################################################################################################################################################
    def all_out_edges_of_node(self, id1: int) -> dict:
        #all edges coming out from node id1, return dict in format: {other node id : edge weight}
        edgeDict={}
        for key in self.graph.get(id1).Node:
            edgeDict[key]=self.graph.get(id1).Node.get(key).getWeight()
        return edgeDict

    #################################################################################################################################################
    def get_mc(self) -> int:
        return self.MC

    #################################################################################################################################################
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:#so this is like the function connect
        # If test is not None , then Im using this function for testing purposes , for example in the is connected function in the GraphAlgo file.
        node:NodeData.NodeData=self.graph.get(id1)
        nodeIN:NodeData.NodeData=self.graph.get(id2)
        if   self.graph.get(id1)==None or self.graph.get(id2)==None or node.Node.get(id2)!=None:
            return False
        else:
            node.Node[id2]= EdgeData.EdgeData(id1,id2,weight)
            nodeIN.InNode[id1]=EdgeData.EdgeData(id1,id2,weight)
            self.edgeCount += 1
            self.MC+=1
            return True

    #################################################################################################################################################
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        #If test is not None , then Im using this function for testing purposes , for example in the is connected function in the GraphAlgo file.
        if self.graph.get(node_id)!=None:
            return False
        if pos==None:
              #We have to generate rando x and y values
              x=random.uniform(35.18,35.22)
              y=random.uniform(32.10,32.12)
              self.graph[node_id] = NodeData.NodeData(x,y, 0, node_id)
              self.nodeCount += 1
              self.MC += 1
              return True
        else:
             self.graph[node_id]=NodeData.NodeData(pos[0],pos[1],pos[2],node_id)
             self.nodeCount+=1
             self.MC += 1
             return True

    #################################################################################################################################################
    def remove_node(self, node_id: int) -> bool:
        if self.graph.get(node_id)==None:#node doesn't exist
            return False
        else:
            node: NodeData.NodeData = self.graph.get(node_id)
            for key in node.Node:#Here we remove all of the nodes that go from node_id to each other vertex and delete nodes id edges from their lists.
                nodeIn: NodeData.NodeData=self.graph.get(key)
                nodeIn.InNode.pop(node_id)
            self.edgeCount -= len(node.Node)
            self.edgeCount -= len(node.InNode)
            node.Node.clear()
            node.Node.clear()
            node.InNode.clear()
            self.graph.pop(node_id)
            self.nodeCount-=1
            self.MC += 1
            return True

    #################################################################################################################################################
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if self.graph.get(node_id1)==None or self.graph.get(node_id2)==None:
            return False
        else:
            node:NodeData.NodeData=self.graph.get(node_id1)
            nodeIn:NodeData.NodeData=self.graph.get(node_id2)
            nodeIn.InNode.pop(node_id1)
            node.Node.pop(node_id2);
            self.edgeCount-=1
            self.MC += 1
            return True
    #################################################################################################################################################
    def __repr__(self):
        return "|V|={0} |E|={1}".format(self.nodeCount,self.edgeCount)

