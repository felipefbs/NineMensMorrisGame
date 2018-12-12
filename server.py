from xmlrpc.server import SimpleXMLRPCServer
import socket
import threading
import time
import numpy as np

ip_server = '127.0.0.1'
port = 10000
server = SimpleXMLRPCServer((ip_server, port), allow_none=True)
players = []
player_turn = 0
game_stage = 1

def send_sock(player: int, msg: str):
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.connect((players[player][1], (port+player+1)))
        server_sock.send(msg.encode('utf-8'))
        server_sock.close()

def login(player_name: str, client_ip: str):
        if(len(players) < 2):
                players.append([player_name, client_ip])
                print(players)
                return len(players)
        else:
                return 0
server.register_function(login, 'login')


def im_ready(player: int):
        global player1_ready 
        global player2_ready
        if (player == 1):
                return 0
        else:   
                send_sock(0, '1')
                send_sock(1, '1')
                send_sock(player_turn, '1')
server.register_function(im_ready, 'im_ready')


def not_my_turn():
        global player_turn
        if(player_turn == 0):
                player_turn = 1
                print(player_turn)
                send_sock(player_turn, '1')
        else:
                player_turn = 0
                print(player_turn)
                if(end_game()):
                        send_sock(player_turn, 'end')
                send_sock(player_turn, '1')

server.register_function(not_my_turn, "not_my_turn")

def waiter():
        global game_stage
        if (game_stage == 1):
                game_stage += 1
        else:
                time.sleep(2)
                send_sock(0, '1')
                send_sock(1, '1')
server.register_function(waiter, "waiter")


def init_board():
        board = np.zeros((7,7), dtype = int)
        board[0] = [5, 0, 0, 5, 0, 0, 5]
        board[1] = [0, 5, 0, 5, 0, 5, 0]
        board[2] = [0, 0, 5, 5, 5, 0, 0]
        board[3] = [5, 5, 5, 0, 5, 5, 5]
        board[4] = board[2]
        board[5] = board[1]
        board[6] = board[0]

        print (board) 
        return board
board = init_board()

def get_board():
        str_board = ''
        for i in range(0,7):
                for j in range(0,7):
                        str_board += str(board[i,j])
        return str_board.replace('0', '').replace('5', 'O')
server.register_function(get_board, 'board')

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
            print("Player "+players[player-1][0]+" place a piece in "+place)
            piece_placer(l, c, player)
            return True
        else:
            print("Player "+players[player-1][0]+" tryed to place a piece in "+place)
            return False
    else:
        return False
server.register_function(place_piece, "place")

def is_mill(player: int, place1: str, place2: str) -> bool:
    if (board[line_column(place1)] == player and board[line_column(place2)] == player):
        return True
    return False

def verify_mill(place: str, player: int) -> bool:
    mill = {    '1A': (is_mill(player, '1D', '1G')) or (is_mill(player, '4A', '7A')),
                '1D': (is_mill(player, '1G', '1A')) or (is_mill(player, '2D', '3D')),
                '1G': (is_mill(player, '1D', '1A')) or (is_mill(player, '4G', '7G')),
                '2B': (is_mill(player, '2D', '2F')) or (is_mill(player, '4B', '6A')),
                '2D': (is_mill(player, '2B', '2F')) or (is_mill(player, '1D', '3D')),
                '2F': (is_mill(player, '4F', '6F')) or (is_mill(player, '2D', '2B')),
                '3C': (is_mill(player, '3D', '3E')) or (is_mill(player, '4C', '5C')),
                '3D': (is_mill(player, '3C', '3E')) or (is_mill(player, '1D', '2D')),
                '3E': (is_mill(player, '4E', '5E')) or (is_mill(player, '3C', '3D')),
                '4A': (is_mill(player, '1A', '7A')) or (is_mill(player, '4B', '4C')),
                '4B': (is_mill(player, '4A', '4C')) or (is_mill(player, '2B', '6B')),
                '4C': (is_mill(player, '3C', '5C')) or (is_mill(player, '4A', '4B')),
                '4E': (is_mill(player, '4F', '4G')) or (is_mill(player, '3E', '5E')),
                '4F': (is_mill(player, '2F', '6F')) or (is_mill(player, '4E', '4G')),
                '4G': (is_mill(player, '1G', '7G')) or (is_mill(player, '4E', '4F')),
                '5C': (is_mill(player, '3C', '4C')) or (is_mill(player, '5D', '5E')),
                '5D': (is_mill(player, '5C', '5E')) or (is_mill(player, '6D', '7D')),
                '5E': (is_mill(player, '5C', '5D')) or (is_mill(player, '3E', '4E')),
                '6B': (is_mill(player, '6D', '6F')) or (is_mill(player, '2B', '4B')),
                '6D': (is_mill(player, '6B', '6F')) or (is_mill(player, '5D', '7D')),
                '6F': (is_mill(player, '6D', '6B')) or (is_mill(player, '2F', '4F')),
                '7A': (is_mill(player, '1A', '4A')) or (is_mill(player, '7D', '7G')),
                '7D': (is_mill(player, '7A', '7G')) or (is_mill(player, '5D', '6D')),
                '7G': (is_mill(player, '7A', '7D')) or (is_mill(player, '1G', '4G'))}
    return mill[place]
server.register_function(verify_mill, "verify")

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

def move_piece(curr_place: str, next_place: str, player: int) -> bool:
    # se o local atual for uma peça do jogador e o proximo local for um local vazio e ambos estiverem em locais dentro do tabuleiro a função executa o movimento
    if(board[line_column(curr_place)] == player and board[line_column(next_place)] == 5):
        line, column = line_column(curr_place)
        if (0 <= line <= 6 and 0 <= column <= 6):   
            piece_placer(line, column, 5)
        else:
            return False
        line, column = line_column(next_place)
        if (0 <= line <= 6 and 0 <= column <= 6):   
            piece_placer(line, column, player)
            return True
        else:
            return False
    else:
        return False
server.register_function(move_piece, "move")

def end_game():
        str_board = get_board()
        player1_pieces, player2_pieces = 0, 0
        for i in str_board:
                if (i == '1'):
                        player1_pieces += 1
                if (i == '2'):
                        player2_pieces += 1
        if (player1_pieces == 2 or player2_pieces == 2 ):
                return True
        else:
                return False
server.register_function(end_game, 'end_game')
server.serve_forever()