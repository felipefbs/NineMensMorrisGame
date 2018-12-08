import socket
import xmlrpc.client
import time


def client_ip():
    ip_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_sock.connect(('8.8.8.8', 80))
    return ip_sock.getsockname()[0]

client_ip = client_ip()
ip_server = '127.0.0.1'
port = 10000
server = xmlrpc.client.ServerProxy('http://'+ip_server+':'+str(port))

def print_board():
    board = server.board()

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

def verify_mill(place: str, player: int, enemy_player: int):
    if (server.verify(place, player)):
        print_board()
        print("Select a piece from enemy player to remove")
        place = str(input()).upper()
        if(not(server.remove(place, enemy_player))):
            print("Select a piece from enemy player to remove")
            place = str(input()).upper()

name = str(input('What\'s your name, player?  '))
player = server.login(name, client_ip)
print(player)
client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.bind((client_ip, (port+player)))

if (player == 1):
    enemy_player = 2
else:
    enemy_player = 1

print_board()
client_sock.listen(10)
server.im_ready(player)
receiver, address = client_sock.accept()


while (receiver.recv(8).decode('utf-8') == 'wait'):
    print("Waiting for another player...")
    time.sleep(1)
else:
    print("Player found. Let the game begin!")
 
client_sock.close()
pieces_in_board = 0
max_pieces = 3
print("Time to place your pieces into the board")
server.game_stage(1)
turn = 0
while (pieces_in_board < max_pieces):
    turn = receiver.recv(8).decode('utf-8')
    if( turn == str(player)):
        print_board()
        print("Remaing pieces: " + str(max_pieces - pieces_in_board))
        place = str(input("Where you want to place your piece?  ")).upper().replace(" ", "")
        while(not(server.place(place, player))):
            print("Invalid place\nIndicate a valid place!")
            place = str(input()).upper().replace(" ", "")
        pieces_in_board += 1
        verify_mill(place, player, enemy_player)
        server.not_my_turn()
    else:
        print_board()
        print("Enemy turn...")
        print("Remaing pieces: " + str(max_pieces - pieces_in_board))

print_board()
server.game_stage(2)

game = 0
while (game == 0):
    turn = receiver.recv(8).decode('utf-8')
    if( turn == str(player)):
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
        verify_mill(place, player, enemy_player)
        server.not_my_turn()        
    else:
        print_board()
        print("Enemy turn...")
        print("You have " + str(pieces_in_board)+" pieces in the board")
    server.game()

    

if(game == player):
    print("Congratulations, you win")
else:
    print("Sorry buddy, but you loose the game")

    
    


