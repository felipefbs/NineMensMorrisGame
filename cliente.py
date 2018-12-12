import socket
import xmlrpc.client
import time
import os

def client_ip():
    ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_sock.connect(('8.8.8.8', 80))
    ip = ip_sock.getsockname()[0]
    ip_sock.close()
    return ip

ip_client = client_ip()
ip_server = '127.0.0.1'
port = 10000
server = xmlrpc.client.ServerProxy('http://'+ip_server+':'+str(port))

def print_board():
    board = server.board()
    os.system('clear')
    print('  A   B   C   D   E   F   G')
    print('1 '+board[0]+'-----------'+board[1]+'-----------'+board[2])
    print('  |           |           |')
    print('2 |   '+board[3]+'-------'+board[4]+'-------'+board[5]+'   |')
    print('  |   |       |       |   |')
    print('3 |   |   '+board[6]+'---'+board[7]+'---'+board[8]+'   |   |')
    print('  |   |   |       |   |   |')
    print('4 '+board[9]+'---'+board[10]+'---'+board[11]+'       '+board[12]+'---'+board[13]+'---'+board[14])
    print('  |   |   |       |   |   |')
    print('5 |   |   '+board[15]+'---'+board[16]+'---'+board[17]+'   |   |')
    print('  |   |       |       |   |')
    print('6 |   '+board[18]+'-------'+board[19]+'-------'+board[20]+'   |')
    print('  |           |           |')
    print('7 '+board[21]+'-----------'+board[22]+'-----------'+board[23])

def game_winner():
    board = server.board()
    p1, p2 = 0, 0
    for i in board:
        if (i == str(player)):
            p1 += 1
        if (i == str(enemy_player)):
            p2 += 1
    if (p1 == 2):
        return 'lose'
    elif (p2 == 2):
        return 'win'
    else:
        return 0

def verify_mill(place: str, player: int, enemy_player: int):
    global pieces_in_board
    if (server.verify(place, player)):
        print_board()
        print("Select a piece from enemy player to remove")
        place = str(input()).upper()
        if(not(server.remove(place, enemy_player))):
            print("Select a piece from enemy player to remove")
            place = str(input()).upper()
        pieces_in_board -= 1

name = str(input('What\'s your name, player?  '))
player = server.login(name, ip_client)
port += player
print(port)
if(player == 0):
    print("This game already have two players")
    exit()

enemy_player = 2 if player == 1 else 1

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.bind((ip_client, (port)))
client.listen()
server.im_ready(player)
def receiv_sock() -> str:
    r, a = client.accept()
    msg = r.recv(8).decode('utf-8')
    return msg

print_board()
print("Waiting for another player...")
receiv_sock()
print("Player found. Let the game begin!")
 
pieces_in_board = 0
max_pieces = 3
print("Time to place your pieces into the board")

while (pieces_in_board < max_pieces):
    print_board()
    print("Enemy turn...")
    print("Remaing pieces: " + str(max_pieces - pieces_in_board))
    receiv_sock()
    print_board()
    print("Remaing pieces: " + str(max_pieces - pieces_in_board))
    place = str(input("Where you want to place your piece?  ")).upper().replace(" ", "")
    while(not(server.place(place, player))):
        print("Invalid place\nIndicate a valid place!")
        place = str(input()).upper().replace(" ", "")
    pieces_in_board += 1
    verify_mill(place, player, enemy_player)
    server.not_my_turn()

print_board()
server.waiter()
receiv_sock()

while (True):
    if (server.end_game()):
        break
    print_board()
    print("Enemy turn...")
    print("You have " + str(pieces_in_board)+" pieces in the board")
    if (receiv_sock() == 'end'):
        break
    print_board()
    print("You have " + str(pieces_in_board)+" pieces in the board")
    print("Wich piece you want to move?")
    curr_place = str(input()).upper().replace(" ", "")
    print("To where you wanna to move your piece?")
    next_place = str(input()).upper().replace(" ", "")
    while (not server.move(curr_place, next_place, player)):
        print("You tried to select an invalid piece or an invalid place\nDo it right this time")
        curr_place = str(input()).upper().replace(" ", "")
        print("To where you wanna to move your piece?")
        next_place = str(input()).upper().replace(" ", "")
    print_board()
    verify_mill(next_place, player, enemy_player)
    server.not_my_turn()

print_board()
if (game_winner() == 'win'):
    print("You Win!")
else:
    print("You Lose")

client.close()

