# Assignment4OOP
Name: David Ehevich , ID:  212757405

Name: Liel Zilberman , ID: 212480974

Name: Israel Yaacobovich ,  ID: 


Disclaimer:
--
All of the info about the graph algorithms used in this assignment and all of the graph implementation which is used in this assignment can be seen in our Assignment3OOP repo,

Link: https://github.com/DavidOP1/Assignment3OOP

Added classes in this assignment:
--
client.py- This class allows us to run commands on the java server to get info for the game , explanations of the commands are in the class in comments. We can receive data about the current pokemons , given agents , given graph and game info which shows the current 

About the assignment- Pokemon Game:
--
In this assignment we have to create somewhat of a pokemon game. On a given graph , we have "agents" and pokemons, the pokemons are located on the edges of the directed graph, meaning , a pokemon on the edge from node 8 to 9 is not the same pokemon on edge from node 9 to 8. The "agents" capture the pokemons only if they pass right by them and are on the same directed edge. Requierments in this game, we are limited by the number of moves we can make in a game, for each second we can make 10 moves, meaning in a 30 seconds game the maximum moves we can make is 300 moves, if we pass that number, our grade wont count. Each pokemon has value, and the grade of the game goes up as we catch more and more pokemons. 

Getting the Game Info:
--
We were given a java server which stores data about given cases, we have 16 cases in total. We get the info about the game, pokemons, "agents" and graph in JSON format.

Running the game:
--
In the github repo you have a folder named: ServerAndData, create a folder in your computer name what you want, for example: ServerAndData, then install the java server and the data folder. After completing these steps , run cmd go to the folder which you created, in our example ServerAndData, and run the server by typing:

java -jar Ex4_Server_v0.0.jar 0  , the '0'  at the end of the line is the number of the case, we have 16 cases(0-15). After typing 
