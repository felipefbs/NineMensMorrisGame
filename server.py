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
server.register_function(login, "login")


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
server.register_function(turn, "my_turn")


def players_ready() -> bool:
    if(len(players) < 2):
        return True
    else:
        return False
server.register_function(players_ready, "ready")


def init_board():
    board = np.zeros((7,7), dtype = int)
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
board = init_board()

def get_board():
    str_board = []
    for i in range(0,7):
        for j in range(0,7):
            str_board.append(str(board[i,j]))
    return str_board
server.register_function(get_board, "board")


def piece_placer(line: int, colu: int, player: int):
    board[line, column] = player

def valid_place(line: int, colu: int) -> bool:
    if(board[line, colu] == 0 or board[line, colu] == 1 or board[line, colu] == 2):
        return False
    else:
        return True

def line_colu(place: str):
    print(place)
    line = int(place[0]) - 1
    column = int(ord(place[1]) - ord('A'))
    return line, column

def place_piece(place: str, player: int) -> bool:
    l, c = line_colu(place)
    if(valid_place(l, c)):
        print("Player "+players[player]+" place a piece in "+place)
        piece_placer(l, c, player)
        return True
    else:
        print("Player "+players[player]+" tryed to place a piece in "+place)
        return False
server.register_function(place_piece, "place_piece")




server.serve_forever()