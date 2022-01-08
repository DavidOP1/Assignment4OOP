import json
import random
import sys
from src import GraphAlgoInterface
from src import DiGraph
class GraphAlgo(GraphAlgoInterface.GraphAlgoInterface):
    #################################################################################################################################################
    graph:DiGraph.DiGraph
    def __init__(self,g:DiGraph.DiGraph=None):
        if g==None:
            self.graph=DiGraph.DiGraph()
        else:
            self.graph=g
    #################################################################################################################################################
    def isConnected(self)->bool: #function to check if it's connected.
        if self.graph.graph==None:
            return False
        visited:dict[int,bool]={}
        vert=0
        for key in self.graph.graph:
            vert=key
            break
        for key in self.graph.graph:
            visited[key]=False
        self.DFS(self.get_graph(),vert,visited)
        for key in self.graph.graph:
            if visited.get(key)==False:
                return False
        for key in self.graph.graph:
            visited[key]=False
        temp=DiGraph.DiGraph() # creating a new graph to reverse all the edges.
        for key in self.graph.graph:
            temp.add_node(self.graph.getNode(key).getKey(),None)
        for key in self.graph.graph:
            for edg in self.graph.graph.get(key).Node:
                temp.add_edge(edg,key,self.graph.graph.get(key).Node.get(edg).getWeight())
        self.DFS(temp,vert,visited)
        for key in self.graph.graph:
            if visited.get(key)==False:
                return False
        return True

    #################################################################################################################################################
    def DFS(self,g:DiGraph.DiGraph,v,visited):
        nodeStack=[]
        nodeStack.append(v)
        while(len(nodeStack)!=0):
            v=nodeStack.pop()
            if visited.get(v):
                continue
            visited[v]=True
            for key in g.graph.get(v).Node:
                if  visited.get(key)==False:
                    nodeStack.append(key)

    #################################################################################################################################################
    def get_graph(self) ->DiGraph.DiGraph:
     return self.graph

    #################################################################################################################################################
    def load_from_json(self, file_name: str) -> bool:
        my_json_file = open(file_name, "r")
        json_data = my_json_file.read()
        obj = json.loads(json_data)
        Edges = obj["Edges"]
        Nodes = obj["Nodes"]
        for i in range(len(Nodes)):
            pos = Nodes[i].get("pos")
            Id = Nodes[i].get("id")
            if pos==None:
                x=random.uniform(35.18,35.22)
                y=random.uniform(32.09,32.11)
                self.graph.add_node(Id,(x, y,0))
            else:
                pos_arr = pos.split(",")
                x = pos_arr[0]
                y = pos_arr[1]
                z = pos_arr[2]
                self.graph.add_node(Id, (x, y, z))
        for i in range(len(Edges)):
            src = Edges[i].get("src")
            w = Edges[i].get("w")
            dest = Edges[i].get("dest")
            self.graph.add_edge(src, dest, w)
    ##############################################################################################################################################
    def save_to_json(self, file_name: str) -> bool:

        data = {}
        data['Edges'] = []

        for key in self.graph.graph:
            if self.graph.graph.get(key).Node != None:
                for index in self.graph.graph.get(key).Node:
                    data['Edges'].append({
                        'src': self.graph.graph.get(key).Node.get(index).getSrc(),
                        'w': self.graph.graph.get(key).Node.get(index).getWeight(),
                        'dest': self.graph.graph.get(key).Node.get(index).getDest()
                    })
            else:
                continue

        data["Nodes"] = []
        for i in self.graph.graph:
            data['Nodes'].append({
                'pos': str(self.graph.getNode(i).getLocation().x) + ',' + str(self.graph.getNode(i).getLocation().y) + ',' + str(self.graph.getNode(i).getLocation().z), "id": self.graph.getNode(i).getKey(), })

        with open(file_name, 'w') as outfile:
            json.dump(data, outfile)
        return True
    ##############################################################################################################################################
    def findPath(self,ret:list,src:int,dest:int)-> list:
        #ret at index 0 is the array of the dist
        #ret at index 1 is the array of previous nodes
        route=[]
        if ret[0].get(dest)==sys.float_info.max: return None
        prev=dest
        while prev!=None:
            route.append(prev)
            prev=ret[1].get(prev)
        route.reverse()
        return route
    ###############################################################################################################################################
    def assistShortest(self,src:int,dest:int,functionChoice:int)-> list or dict:#functionChoice 0 is for shortestPath list and 1 is to return a list for all the shortest distances from the src
        minDist:float=0
        newDist:float=0
        index:int=0
        ret=[]
        distQ=[]#We implement the prioity queue we used in our java program with list.
        visited={}
        dist={}
        previousNode={}
        temp:tuple(int,float)=()#Our pair in our java program in this casse will be tuple. (id,distance)
        #distQ=PriorityQueue.PriorityQueue
        for key in self.graph.graph:
            visited[key]:dict[int:bool]=False
            dist[key]=sys.float_info.max
            previousNode[key]=None
        dist[src]=0
        distQ.append((0,src))
       # distQ.sort(reverse=True)
        while len(distQ)>0:
            temp=distQ.pop()
            index=temp[1]
            minDist=temp[0]#We poll from the priority queue accordingly to the distance value in the tuple (id,distance)
            visited[index]=True
            if dist.get(index)<minDist: continue
            for edgeKey in self.graph.graph.get(index).Node:
               if visited.get(edgeKey): continue
               newDist=dist.get(index)+self.graph.graph.get(index).Node.get(edgeKey).getWeight()
               if newDist<dist.get(edgeKey):
                   previousNode[edgeKey]=index
                   dist[edgeKey]=newDist
                   distQ.append((newDist,edgeKey))
                   distQ.sort(reverse=True)
        ret.append(dist)
        ret.append(previousNode)
        if functionChoice==0:return self.findPath(ret,src,dest),dist[dest]
        elif functionChoice==1: return dist
    #################################################################################################################################################
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        if self.graph.graph.get(id1)==None or self.graph.graph.get(id2)==None:
            return None,None
        path,distance=self.assistShortest(id1,id2,0)
        if path==None: return (float('inf'),[])
        #here calculate the total distance of the route.
        return distance,path
    #################################################################################################################################################
    def TSP(self, node_lst:list[int]) -> (list[int], float):
        #Note for my self: dont forget to sum the total traveled distance
        cityRoute=[]
        cityRouteList=[]# will store a list of NodeData lists
        routeTemp=[]
        distance=0
        sum=0
        #do route with j=(i+1)%mod citis.size() to close full circle route with cities
        for i in range(len(node_lst)-1):
            dist,routeTemp=self.shortest_path(node_lst[i],node_lst[(i+1)%(len(node_lst))])#dist is not relevant in this function
            if routeTemp==None: return (float('inf'),[])
            cityRouteList.append(routeTemp)
        for i in range(len(cityRouteList)):
            if i!=0:
                for j in range(1,len(cityRouteList[i])):
                    cityRoute.append(cityRouteList[i][j])
            else:
                for j  in range(len(cityRouteList[i])):
                    cityRoute.append(cityRouteList[i][j])
        for i in range(len(cityRoute)-1):
           garbage,distance=self.assistShortest(cityRoute[i],cityRoute[i+1],0)
           sum+=distance
        return (cityRoute,sum)
    #################################################################################################################################################
    def centerPoint(self) -> (int, float):
        maxDistance=0
        dist:dict[int:float]={}#format : {node_id:max min distance}
        if self.isConnected():
            for key in self.graph.graph:#just get a random key to work with in the next loop
                tempKey=key
                break;
            for key in self.graph.graph:
                tempDict=self.assistShortest(key,tempKey,1)
                max_key=max(tempDict, key=tempDict.get)#Returns the key of the max value in the dictionary
                maxDistance=tempDict[max_key]
                dist[key]=maxDistance
            return  (min(dist,key=dist.get),dist[min(dist,key=dist.get)]) # returns the smallest value in this max dist dict.
        else:
          return (None,float('inf'))
    #################################################################################################################################################
    def plot_graph(self) -> None:
        X_nodes = []
        Y_nodes = []

        for key in self.graph.graph:
            X_nodes.append(self.graph.getNode(key).getLocation().x)
            Y_nodes.append(self.graph.getNode(key).getLocation().y)

        X_nodes.sort()
        Y_nodes.sort()
        GUI(self.graph, X_nodes, Y_nodes)