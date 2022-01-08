# Just testing here, Ratio the distance between the weight of the edge and the distance the agent has to make to get
# there, and then put in priority queue. weight/distance, the higher the better. Calculate priority queue for agents
# to capture a pokemon, do that for each pokemon and with available agents. Build each agent a route. Ratio the
# distance between the weight of the edge and the distance the agent has to make to get there, and then put in
# priority queue. weight/distance, the higher the better. Ratio the distance between the weight of the edge and the
# distance the agent has to make to get there, and then put in priority queue. weight/distance, the higher the
# better. Ratio the distance between the weight of the edge and the distance the agent has to make to get there,
# and then put in priority queue. weight/distance, the higher the better. from GraphAlgo import GraphAlgo
import json
from types import SimpleNamespace

import pygame
from pygame import display, RESIZABLE, gfxdraw
from src.pokemon import Pokemon
from model.client import Client
from src.agent import Agent
from src.DiGraph import DiGraph
import math
import sys
import time
from src.GraphAlgo import GraphAlgo

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
client = Client()
client.start_connection(HOST, PORT)
pok = []
agents: Agent = {}
pokEdg = []
public = ""

# init pygame
WIDTH, HEIGHT = 1080, 800

pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Pokemon Game")
background_img = pygame.image.load('../view/map.png')
agent_img = pygame.image.load('../view/agent.png')
pikachu_img = pygame.image.load('../view/pikachu.png')
meowth_img = pygame.image.load('../view/meowth.png')

pygame.font.init()

FONT = pygame.font.SysFont('Arial', 20, bold=True)
font_button = pygame.font.SysFont('Arial', 30, bold=True)


class Button:
    def __init__(self, image, x_pos, y_pos, text_input):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_input = text_input
        self.text = font_button.render(self.text_input, True, "white")
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            client.stop()
            client.stop_connection()

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top,
                                                                                          self.rect.bottom):
            self.text = font_button.render(self.text_input, True, "green")
        else:
            self.text = font_button.render(self.text_input, True, "white")


button_surface = pygame.image.load("../view/button.png")
button_surface = pygame.transform.scale(button_surface, (200, 100))

button = Button(button_surface, 80, 150, "Stop")

pokemons_json = client.get_pokemons()
pokemons_obj = json.loads(pokemons_json, object_hook=lambda d: SimpleNamespace(**d))

graph_json = client.get_graph()
graph_obj = json.loads(graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph_obj.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

min_x = min(list(graph_obj.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph_obj.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph_obj.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph_obj.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

font = pygame.font.SysFont('Arial', 32, bold=True)


def creatAgents(info: dict):
    numAgents = info["GameServer"]["agents"]
    # Here I have to receive the list of pokemons as well.
    pokEdg.sort(reverse=True)
    for i in range(numAgents):
        string = '"id":{0}'.format(pokEdg[0][1])  # Getting highest value pokemon src's edge.
        # '{"agent_id":0, "next_node_id":1}'.
        string = '{' + string + '}'
        client.add_agent(string)


def createGraph(g: dict):
    for nd in g["Nodes"]:
        (x, y, z) = nd["pos"].split(",")
        graph.add_node(nd["id"], (float(x), float(y), float(z)))
    for edg in g["Edges"]:
        graph.add_edge(edg["src"], edg["dest"], edg["w"])


pokList: Pokemon = []


def createPoki(poki):
    mone = 0
    for pokemon in poki["Pokemons"]:
        for info in pokemon:
            mone = 0
            val = pokemon[info]["value"]
            type = pokemon[info]["type"]
            x, y, z = pokemon[info]["pos"].split(",")
            pokList.append(Pokemon(val, float(x), float(y), type))


pokEdg = []  # Will store tuples of where to pokis are located, tuple , maybe of (src,dest,id) id of pokemon.


# maybe add return here to return the pok list.
def FindPoki():
    temp, small, gap = (), sys.float_info.max, 0
    src, dest = 0, 0
    for p in pokList:
        small, gap = sys.float_info.max, 0
        temp = ()
        for i in graph.graph:
            for j in graph.getNode(i).Node:
                src = graph.getNode(i).getLocation()
                dest = graph.getNode(j).getLocation()

                edgeSize = math.sqrt(math.pow(src.y - dest.y, 2) + math.pow(src.x - dest.x, 2))

                # Dont forget to check type here.
                # Keeping the most minimal gap.

                size1 = math.sqrt(math.pow(p.getLocation().y - dest.y, 2) + math.pow(p.getLocation().x - dest.x, 2))
                size2 = math.sqrt(math.pow(p.getLocation().y - src.y, 2) + math.pow(p.getLocation().x - src.x, 2))

                gap = abs((size1 + size2) - edgeSize)

                # If the edge goes to a dest with higher y value means the type is 1
                if (j > i and p.getType() == 1):
                    if gap < small:
                        small = gap
                        temp = (p.getValue(), j, i, p.getLocation().x, p.getLocation().y,
                                p.getType())  # the value will be used for the algorithm. tuple struct (value,src,dest)
                        src = j
                        dest = i

                elif (i > j and p.getType() == -1):
                    if gap < small:
                        small = gap
                        temp = (p.getValue(), i, j, p.getLocation().x, p.getLocation().y,
                                p.getType())  # the value will be used for the algorithm. tuple struct (value,src,dest)
                        src = i
                        dest = j

        if not temp:
            continue
        else:
            mone = 0
            for ed in pokEdg:
                if temp[0] == ed[0] and temp[1] == ed[1] and temp[2] == ed[2] and temp[3] == ed[3] and temp[4] == ed[
                    4] and temp[5] == ed[5]:
                    break
                elif mone == len(pokEdg) - 1:
                    pokEdg.append(temp)
        if len(pokEdg) == 0:
            pokEdg.append(temp)

        # 35.197656770719604,32.10191878639921
        # Create a list of pokemons for each agent.
        # Maybe to ID for the pokemon will be a tuple - > (src,dest) since It's a directional graph and this is how we will get the correct edge every time.\
        # Here find the correct edge for the pokemon;
        # Create a list of tuples on which the pokemons are located at.


def firstSrcAgent():
    timp = 0
    agenti = json.loads(client.get_agents())
    for ag in agenti["Agents"]:

        if len(pokEdg) != 0:
            dest = '"agent_id":{0}, "next_node_id":{1}'.format(ag["Agent"]["id"], pokEdg[0][2])  # Think about the id.

            dest = '{' + dest + '}'

            client.choose_next_edge(dest)
            timp = pokEdg[0]
            agents[ag["Agent"]["id"]] = [(pokEdg[0][1], pokEdg[0][2], pokEdg[0][3], pokEdg[0][4]), ([],
                                                                                                    0)]  # All assigned pokemons to the agent. in the second param we will keep future routes to pokemons. (x,y,src,dest)
            pokEdg.pop(0)  # Removing it from the poki list since the agent is going to catch it.
        else:
            algi = GraphAlgo(graph)
            dest = '"agent_id":{0}, "next_node_id":{1}'.format(ag["Agent"]["id"], 0)  # Think about the id.
            # print(dest)
            dest = '{' + dest + '}'
            # print(dest)
            client.choose_next_edge(dest)
            #print("first id= ", ag["Agent"]["id"])
            agents[ag["Agent"]["id"]] = [(), ([], 0)]


graph = DiGraph()
# To get the best route , we will go to the src of the edge the pokemon is on , in the tuple (src,dest) and after we
# did all the route, we will move the agent to the dest of the edge the pokemon is located on.
if __name__ == '__main__':
    g = json.loads(client.get_graph())
    createGraph(g)
    info = json.loads(client.get_info())

    pokemons = json.loads(client.get_pokemons())
    createPoki(pokemons)

    FindPoki()

    # client.move()
    # createGraph(client.get_graph())
    # java -jar Ex4_server_v0.0.jar 0
    # After creating agents and assigning dest's activate move?
    creatAgents(info)
    mone = 0
    algo = GraphAlgo(graph)
    client.start()
    while client.is_running() == "true":
        info_json = client.get_info()
        info_obj = json.loads(info_json, object_hook=lambda d: SimpleNamespace(**d))

        # time to end in seconds
        end_time = int(int(client.time_to_end()) * 0.001)

        pokemons_json = json.loads(client.get_pokemons(),
                                   object_hook=lambda d: SimpleNamespace(**d)).Pokemons
        pokemons_json = [p.Pokemon for p in pokemons_json]
        for p in pokemons_json:
            x, y, _ = p.pos.split(',')
            p.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))
        agents1 = json.loads(client.get_agents(),
                             object_hook=lambda d: SimpleNamespace(**d)).Agents
        agents1 = [agent.Agent for agent in agents1]
        for a in agents1:
            x, y, _ = a.pos.split(',')
            a.pos = SimpleNamespace(x=my_scale(
                float(x), x=True), y=my_scale(float(y), y=True))
        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            if event.type == pygame.VIDEORESIZE:
                background_img = pygame.transform.scale(background_img, (event.w, event.h))
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.checkForInput(pygame.mouse.get_pos())
        # refresh surface
        screen.fill(pygame.Color(0, 0, 0))
        # background image
        screen.blit(background_img, (0, 0))

        # draw nodes
        for n in graph_obj.Nodes:
            x = my_scale(n.pos.x, x=True)
            y = my_scale(n.pos.y, y=True)

            # its just to get a nice antialiased circle
            gfxdraw.filled_circle(screen, int(x), int(y),
                                  radius, pygame.Color(168, 0, 0))
            gfxdraw.aacircle(screen, int(x), int(y),
                             radius, pygame.Color(76, 25, 25))

            # draw the node id
            id_srf = FONT.render(str(n.id), True, pygame.Color(255, 255, 255))
            rect = id_srf.get_rect(center=(x, y))
            screen.blit(id_srf, rect)

        # draw edges
        for e in graph_obj.Edges:
            # find the edge nodes
            src = next(n for n in graph_obj.Nodes if n.id == e.src)
            dest = next(n for n in graph_obj.Nodes if n.id == e.dest)

            # scaled positions
            src_x = my_scale(src.pos.x, x=True)
            src_y = my_scale(src.pos.y, y=True)
            dest_x = my_scale(dest.pos.x, x=True)
            dest_y = my_scale(dest.pos.y, y=True)

            # draw the line
            pygame.draw.line(screen, pygame.Color(0, 0, 0),
                             (src_x, src_y), (dest_x, dest_y))

        # draw agents
        for agent in agents1:
         screen.blit(agent_img, (int(agent.pos.x) - 50, int(agent.pos.y) - 50))

        # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked
        # in the same way).
        for p in pokemons_json:
            if p.type == 1:
                screen.blit(pikachu_img, (int(p.pos.x) - 50, int(p.pos.y) - 50))
            elif p.type == -1:
                screen.blit(meowth_img, (int(p.pos.x) - 50, int(p.pos.y) - 50))
        # draw the score

        grade = font.render("Grade: " + str(info_obj.GameServer.grade), True, (250, 250, 250))
        moves = font.render("Moves: " + str(info_obj.GameServer.moves), True, (250, 250, 250))
        seconds = font.render("Time Left: " + str(end_time), True, (250, 250, 250))
        screen.blit(grade, (10, 10))
        screen.blit(moves, (10, 40))
        screen.blit(seconds, (10, 70))
        button.update()
        button.changeColor(pygame.mouse.get_pos())

        # update screen changes
        display.update()

        # refresh rate
        clock.tick(60)

        # Time to live is in miliseconds meaning, if I can do 10 move calls each 1 second, meaning 1 call each 1/10
        # second , meaning 1 call every 100 miliseconds. In the agent list keep the current pokemon.
        agn = json.loads(client.get_agents())
        if mone == 0:
            firstSrcAgent()
            mone += 1
            client.move()
        agn = json.loads(client.get_agents())
        for ag in agn["Agents"]:
            if ag["Agent"][
                "dest"] != -1:  # Since it goes from one edge to another , so the src and dest always have to update.

                if ag["Agent"]["src"] == agents[ag["Agent"]["id"]][0][0] and ag["Agent"]["dest"] == \
                        agents[ag["Agent"]["id"]][0][1]:
                    # Here start checking the distance between the assigned agent and poki.
                    x, y, z = ag["Agent"]["pos"].split(",")
                    # (x, y, src, dest)
                    dist = math.sqrt(math.pow(agents[ag["Agent"]["id"]][0][3] - float(y), 2) + math.pow(
                        agents[ag["Agent"]["id"]][0][2] - float(x), 2))

            elif ag["Agent"]["dest"] == -1:
                # Notice that it will enter this condition mid route as well Check if the list of the route of the
                # agent is not empty , it didnt grab the pokemon, if the len list is 1 then its on the src of the
                # pokemon edge. I dont think tsp is needed, only the current node of the agent and the src of edge
                # the pokemon is located on.
                if len(agents[ag["Agent"]["id"]][1][0]) == 0:
                    # Remove pokemon from list:
                    # Here remove from pokEdge:

                    pokList = []
                    createPoki(json.loads(client.get_pokemons()))
                    FindPoki()
                    pokEdg.sort(reverse=True)
                    agents[ag["Agent"]["id"]] = [(pokEdg[0][1], pokEdg[0][2], pokEdg[0][3], pokEdg[0][4]), ([], 0)]
                    size = len(pokList)
                    i = 0
                    while i < size:

                        # agents[ag["Agent"]["id"]][0][2]
                        # pokList[i].getLocation().y==agents[ag["Agent"]["id"]][0][3]
                        if pokList[i].getLocation().x == agents[ag["Agent"]["id"]][0][2] and pokList[
                            i].getLocation().y == agents[ag["Agent"]["id"]][0][3]:
                            pokList.pop(i)  # if we have 2 removes it's problematic/
                            i = i - 1
                            size = size - 1

                        i += 1
                    size = len(pokEdg)
                    i = 0
                    while i < size:
                        if pokEdg[i][0] == agents[ag["Agent"]["id"]][0][0] and pokEdg[i][1] == \
                                agents[ag["Agent"]["id"]][0][1] and pokEdg[i][2] == agents[ag["Agent"]["id"]][0][2] and \
                                pokEdg[i][3] == agents[ag["Agent"]["id"]][0][3]:
                            pokEdg.pop(i)
                            i = i - 1
                            size = size - 1
                        i += 1

                    agents[ag["Agent"]["id"]][1] = (algo.shortest_path(ag["Agent"]["src"], pokEdg[0][1])[1], pokEdg[0][
                        2])  # Dont forget about the dest of the pok edge, how to do it? tuple which keeps the src and dest of the poki.

                    dest = '"agent_id":{0}, "next_node_id":{1}'.format(ag["Agent"]["id"],
                                                                       agents[ag["Agent"]["id"]][1][0][
                                                                           0])  # Think ab out the id.
                    dest = '{' + dest + '}'
                    client.choose_next_edge(dest)
                    pokEdg.pop(0)

                elif len(agents[ag["Agent"]["id"]][1][0]) > 1:
                    if ag["Agent"]["src"] == agents[ag["Agent"]["id"]][1][0][0]:
                        agents[ag["Agent"]["id"]][1][0].pop(0)
                        dest = '"agent_id":{0}, "next_node_id":{1}'.format(ag["Agent"]["id"],
                                                                           agents[ag["Agent"]["id"]][1][0][
                                                                               0])  # Think about the id.
                        dest = '{' + dest + '}'
                        client.choose_next_edge(dest)

                elif len(agents[ag["Agent"]["id"]][1][0]) == 1:
                    dest = '"agent_id":{0}, "next_node_id":{1}'.format(ag["Agent"]["id"], agents[ag["Agent"]["id"]][1][
                        1])  # Think about the id.
                    dest = '{' + dest + '}'
                    client.choose_next_edge(dest)

                    agents[ag["Agent"]["id"]][1][0].pop(0)
        client.move()
        time.sleep(1 / 10)