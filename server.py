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
    if (0 <= line <= 6 and 0 <= column <= 6):   
        if(board[line, column] == 0 or board[line, column] == 1 or board[line, column] == 2):
            return False
        else:
            print("valid_place")
            return True
    else:
        return False

def line_column(place: str):
    line = int(place[0]) - 1
    column = int(ord(place[1]) - ord('A'))
    print(line, column)
    return line, column

def place_piece(place: str, player: int) -> bool:
    if (place[0].isdigit() and place[1].isalpha()):
        l, c = line_column(place)
        if(valid_place(l, c)):
            print(player)
            print("Player "+players[player-1]+" place a piece in "+place)
            piece_placer(l, c, player)
            return True
        else:
            print("Player "+players[player-1]+" tryed to place a piece in "+place)
            return False
    else:
        return False
server.register_function(place_piece, "place_piece")

def move_piece(curr_place: str, next_place: str, player: int) -> bool:
    # se o local atual for uma peça do jogador e o proximo local for um local vazio e ambos estiverem em locais dentro do tabuleiro a função executa o movimento
    if(board[line_column(curr_place)] == player and board[line_column(next_place)] == 5):
        l, c = line_column(curr_place)
        if (0 <= l <= 6 and 0 <= c <= 6):   
            piece_placer(l, c, 5)
        else:
            return False
        l, c = line_column(next_place)
        if (0 <= line <= 6 and 0 <= column <= 6):   
            piece_placer(l, c, player)
            return True
        else:
            return False
    else:
        return False
server.register_function(move_piece, "move")   


def remove_piece(place: str, enemy_player: int) -> bool:
    l, c = line_column(place)
    if (0 <= l <= 6 and 0 <= c <= 6):
        if (board[l,c] == enemy_player):
            piece_placer(l, c, 5)
            return True
        else:
            return False
    else:
        return False
server.register_function(remove_piece, "remove")

def verify_mill():
    colunas = []
    linhas = []

    for i in range(7):
        colunas.append(board[:,i])
        linhas.append(board[i])
    linha31 = linhas[3][:3]
    linha32 = linhas[3][4:]
    coluna31 = colunas[3][:3]
    coluna32 = colunas[3][4:]
    del linhas[3]
    del colunas[3]
    if (linha31.sum()==3 or linha32.sum()==3 or coluna31.sum()==3 or coluna32.sum()==3):
        if (0 not in linha31 and 0 not in linha32 and 0 not in coluna31 and 0 not in coluna32):    
            print("mill 1")
            return 1
    if (linha31.sum()==6 or linha32.sum()==6 or coluna31.sum()==6 or coluna32.sum()==6):
        
            print("mill 2")
            return 2

    for i in range(6):
        if (linhas[i].sum() == 3):
            if (0 not in linhas[i]):
                print("mill 1")
                return 1
    for i in range(6):
        if (colunas[i].sum() == 3):
            if (0 not in colunas[i]):
                print("mill 1")
                return 1

    for i in range(6):
        if (linhas[i].sum() == 6):
            if (0 not in linhas[i]):
                print("mill 2")
                return 2
    for i in range(6):
        if (colunas[i].sum() == 6):
            if (0 not in colunas[i]):
                print("mill 2")
                return 2
    return 0
server.register_function(verify_mill, "verify")

def end_game():
    player1_pieces = 0
    player2_pieces = 0

    for i in range(7):
        for j in range(7):
            if(board[i,j] == 1):
                player1_pieces += 1
            elif(board[i,j] == 2):
                player2_pieces += 1
    if (player1_pieces ==2 or player2_pieces ==2):
        if(player1_pieces<player2_pieces):
            return 1
        else:
            return 2
    
    return 0
server.register_function(end_game, "end_game")


server.serve_forever()
