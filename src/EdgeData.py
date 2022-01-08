class EdgeData:
    def __init__(self,src:int,dest:int,weight:float):
        self.src=src
        self.dest=dest
        self.weight=weight
    def getSrc(self):
        return self.src
    def getDest(self):
        return self.dest
    def getWeight(self):
        return self.weight