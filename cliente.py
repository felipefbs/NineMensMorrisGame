import xmlrpc.client
import time
s = xmlrpc.client.ServerProxy('http://localhost:9999')

print("Welcome to the Nine Men's Morris game\nWhat's your name player?")
player_name = str(input())
player = s.login(player_name)

if(player == 0):
    print("Sorry "+player_name+" but this game already have two players...")
    exit()

while(s.ready()):
    print("Waiting for another player...")
    time.sleep(2)

while(True):
    if(s.my_turn(player)):
        print("My turn")
        time.sleep(1)
        #it's my turn
    else:
        print("NOT My turn")
        time.sleep(5)
        #it's not my turn
