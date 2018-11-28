import xmlrpc.client
import time
import os

try:
    ip = os.sys.argv[1]
    s = xmlrpc.client.ServerProxy('http://'+ip+':10001')
except IndexError:
    print("Invalid IP")
    exit()



def print_board():
    board = s.board()
    #os.system("clear")
    print("A B C D E F G")
    print("-------------")
    count = 0
    while(count!=49):
        for i in range(0,7):
            if(board[count] == '5'):
                print("O", end=' ')
            elif(board[count] == '0'):
                print(" ", end=' ')
            elif(board[count] == '1'):
                print("1", end=' ')
            elif(board[count] == '2'):
                print("2", end=' ')
            count+=1
        print("|"+ str(int(count/7)))

def verify_mill(player: int, enemy_player: int):
    if (s.verify() == player):
        print("Select a piece from enemy player to remove")
        place = str(input()).upper()
        if(not(s.remove(place, enemy_player))):
            print("Select a piece from enemy player to remove")
            place = str(input()).upper()

print("Welcome to the Nine Men's Morris game\nWhat's your name player?")
player_name = str(input())
player = s.login(player_name)

if(player == 0):
    print("Sorry "+player_name+" but this game already have two players...")
    exit()


if (player == 1):
    enemy_player = 2
else:
    enemy_player = 1

print_board()

while(s.ready()):
    print("Waiting for another player...")
    time.sleep(3)


pieces_in_board = 0
max_pieces = 9
print("Time to place your pieces")
while(pieces_in_board < max_pieces):
    while(s.my_turn(player)):
        print_board()
        print("Remaing pieces: " + str(max_pieces - pieces_in_board))
        print("Where you want to place your piece?")
        place = str(input()).upper()
        while(not(s.place_piece(place, player))):
            print("Invalid place\nIndicate a valid place!")
            place = str(input()).upper()
        pieces_in_board += 1
        verify_mill(player, enemy_player)
        s.not_my_turn()      
    else:
        print_board()
        print("Enemy turn...")
        print("Remaing pieces: " + str(max_pieces - pieces_in_board))
        time.sleep(2)


print_board()
print("Time to move your pieces arround the board to decide whom wins!")
game = 0   
while(game == 0):
    if(s.my_turn(player)):
        print_board()
        print("You have " + str(pieces_in_board)+" pieces in the board")
        
        print("Wich piece you want to move?")
        curr_place = str(input()).upper()
        print("To where you wanna to move your piece?")
        next_place = str(input()).upper()

        while (not s.move(curr_place, next_place, player)):
            print("You tried to select an invalid piece or an invalid place\nDo it right this time")
            curr_place = str(input()).upper()
            print("To where you wanna to move your piece?")
            next_place = str(input()).upper()
        print_board()
        
        verify_mill(player, enemy_player)

        print_board()
        s.not_my_turn()
    else:
        print_board()
        print("Enemy turn...")
        print("You have " + str(pieces_in_board)+" pieces in the board")
        time.sleep(3)

    game = s.end_game()

if(game == 1):
    print("Congratulations, you win")
elif(game == 2):
    print("Sorry buddy, but you loose the game")

