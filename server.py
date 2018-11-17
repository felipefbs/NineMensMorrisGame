from xmlrpc.server import SimpleXMLRPCServer
import numpy as np 
import time
import random

server = SimpleXMLRPCServer(('localhost', 10001))
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


def my_turn(player: int) -> bool:
    global player_turn
    if(player_turn == player):
        print(players[player-1]+'\'s turn')
        return True
    else:
        return False
server.register_function(my_turn, "my_turn")


def not_my_turn():
    global player_turn
    if(player_turn == 1):
        player_turn = 2
        return 0
    else:
        player_turn = 1
        return 0
server.register_function(not_my_turn, "not_my_turn")


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


def piece_placer(line: int, column: int, player: int):
    board[line, column] = player
    print(board)

def valid_place(line: int, column: int) -> bool:
    print(line, column)
    if(board[line, column] == 0 or board[line, column] == 1 or board[line, column] == 2):
        print("valid_place")
        return False
    else:
        return True

def line_column(place: str):
    line = int(place[0]) - 1
    column = int(ord(place[1]) - ord('A'))
    print(line, column)
    return line, column

def place_piece(place: str, player: int) -> bool:
    
    l, c = line_column(place)
    if(valid_place(l, c)):
        print(player)
        print("Player "+players[player-1]+" place a piece in "+place)
        piece_placer(l, c, player)
        return True
    else:
        print("Player "+players[player]+" tryed to place a piece in "+place)
        return False
server.register_function(place_piece, "place_piece")


server.serve_forever()