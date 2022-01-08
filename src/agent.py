from src.Location import Location
class Agent:
#Which pokemons to catch, current pos maybe?
#id of agent, current value of all catched pokemons ,speed, pos, src and dest nodes.
    def __init__(self,id,value,src,dest,speed,x,y):
        self.Location=Location(x,y,0)
        self.id=id
        self.val=value
        self.src=src
        self.dest=dest
        self.speed=speed
    def getLocation(self):
        return (self.Location.x,self.Location.y)
    def getValue(self):
        return self.val
    def getSpeed(self):
        return self.speed
    def getSrcID(self):
        return self.src
    def getDestID(self):
        return self.dest
    def setPoki(self,poki:tuple):
        self.Poki=poki
    def getPoki(self):
        return self.Poki