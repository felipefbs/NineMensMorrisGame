import xmlrpc.client
import time
s = xmlrpc.client.ServerProxy('http://localhost:9999')

def print_board():
    board = s.board()
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

print("Welcome to the Nine Men's Morris game\nWhat's your name player?")
player_name = str(input())
player = s.login(player_name)

if(player == 0):
    print("Sorry "+player_name+" but this game already have two players...")
    exit()

print_board()

while(s.ready()):
    print("Waiting for another player...")
    time.sleep(2)

print("Time to place your pieces")
while(True):
    if(s.my_turn(player)):
        #it's my turn
        print("My turn")
        time.sleep(1)
        
    else:
        print("NOT My turn")
        time.sleep(5)
        #it's not my turn
