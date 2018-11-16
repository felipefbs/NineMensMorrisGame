from xmlrpc.server import SimpleXMLRPCServer
import numpy as np 
import time

server = SimpleXMLRPCServer(('localhost', 9999))

players = []
def login(player_name: str) -> int:
    if(len(players) < 2):
        players.append(player_name)
        print(player_name+" connected to the server")
        #if(len(players) == 1):
        #    player_turn = 1
        return len(players)
    else:
        print(player_name+" tryed to connect...")
        return 0
player_turn = 1
def turn(player: int) -> bool:
    global player_turn
    if(player_turn == player):
        if(player_turn == 1):
            player_turn = 2
        else:
            player_turn = 1
        return True
    else:
        return False





server.register_function(turn, "my_turn")
server.register_function(login, "login")
server.serve_forever()