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
client.py- This class allows us to run commands on the java server to get info for the game , explanations of the commands are in the class in comments. We can receive data about the current pokemons , given agents , given graph and game info which shows the current grade , number of agents and pokemons, and time remaining for the game.

Ex4.py- In this class we implement the GUI and algorithm of the game, in here we run the game when the server is activated.

Pokemon.py- a class which allows to store data about pokemons , such as position and value.

Agent.py- This class allows us to store data about the agent, such as pos caught pokemons, and speed.

About the assignment- Pokemon Game:
--
In this assignment we have to create somewhat of a pokemon game. On a given graph , we have "agents" and pokemons, the pokemons are located on the edges of the directed graph, meaning , a pokemon on the edge from node 8 to 9 is not the same pokemon on edge from node 9 to 8. The "agents" capture the pokemons only if they pass right by them and are on the same directed edge. Requierments in this game, we are limited by the number of moves we can make in a game, for each second we can make 10 moves, meaning in a 30 seconds game the maximum moves we can make is 300 moves, if we pass that number, our grade wont count. Each pokemon has value, and the grade of the game goes up as we catch more and more pokemons. 

Getting the Game Info:
--
We were given a java server which stores data about given cases, we have 16 cases in total. We get the info about the game, pokemons, "agents" and graph in JSON format.

Running the game:
--
In the github repo you have a folder named: ServerAndData, create a folder in your computer name what you want, for example: ServerAndData, then install the java server and the data folder. After completing these steps , run cmd go to the folder which you created, in our example ServerAndData, and run the server by typing:

java -jar Ex4_Server_v0.0.jar 0  , the '0'  at the end of the line is the number of the case, we have 16 cases(0-15).
After turning on the java game server with the choosen case, We open another cmd window and going to the python code directory , then typing , python Ex4.py , after pressing enter a GUI window should pop up with the graph and the first pokemons and agent's located in their positions, and then the game runs and catches the pokemons.

Running the game on case 11 example, youtube video:
--
https://youtu.be/2PxvP6G69uw

UML:
--
![WhatsApp Image 2022-01-08 at 21 50 51](https://user-images.githubusercontent.com/54214707/148657977-b19caf6c-2caf-41b1-8415-7e74db39e34a.jpeg)

