from src.Location import Location
class Pokemon:
    #This class will contain about if it was eaten , id , on which edge it's located on.
    #Value of the pokemon.
    #type
    def __init__(self,val,x,y,type):
        self.val=val
        self.x=x
        self.y=y
        self.type=type
    def getValue(self):
        return self.val
    def getLocation(self):
        return Location(self.x,self.y,0)
    def getType(self):
        return self.type
    def setAgent(self,id):
        self.id
    def getAgent(self):
        return self.id
    def setSrc(self,src):
        self.src=src
    def getSrc(self):
        return float(self.src)
    def setDest(self, src):
        self.dest = src

    def getDest(self):
        return float(self.dest)
