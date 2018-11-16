from xmlrpc.server import SimpleXMLRPCServer
import numpy as np 
import time
import random

server = SimpleXMLRPCServer(('localhost', 9999))
player_turn = 0
players = []
def login(player_name: str) -> int:
    global player_turn
    if(len(players) < 2):
        players.append(player_name)
        print(player_name+" connected to the server")
        player_turn = random.randint(1,2)
        print(player_turn)
        return len(players)
    else:
        print(player_name+" tryed to connect...")
        return 0

def turn(player: int) -> bool:
    global player_turn
    if(player_turn == player):
        if(player_turn == 1):
            player_turn = 2
        else:
            player_turn = 1
        print(players[player-1]+'\'s turn')
        return True
    else:
        return False

def players_ready() -> bool:
    if(len(players) < 2):
        return True
    else:
        return False


server.register_function(players_ready, "ready")
server.register_function(turn, "my_turn")
server.register_function(login, "login")
server.serve_forever()