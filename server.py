from xmlrpc.server import SimpleXMLRPCServer
import numpy as np 
import time

server = SimpleXMLRPCServer(('localhost', 9999))

def initialize_board() -> list:
    board = np.zeros((7,7), dtype=int)
    for i in range(0,7):
            for j in range(0,7):
                if(i==0 or i ==6):
                    if (j == 0 or j == 3 or j==6):
                        board[i,j] = 5
                if(i==1 or i ==5):
                    if (j == 1 or j == 3 or j==5):
                        board[i,j] = 5
                if(i==2 or i ==4):
                    if (j == 2 or j == 3 or j==4):
                        board[i,j] = 5
                if(i == 3):
                    if (j == 0 or j == 1 or j==2 or j == 4 or j == 5 or j==6):
                        board[i,j] = 5
    return board


players = []
def login(player_name: str) -> int:
    if(len(players) < 2):
        players.append(player_name)
        print(player_name+" connected to the server")
        return len(players)
    else:
        print(player_name+" tryed to connect...")
        return 0
server.register_function(login, "login")

server.serve_forever()