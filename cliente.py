import xmlrpc.client
import time
s = xmlrpc.client.ServerProxy('http://localhost:9999')


player_name = str(input())
player = s.login(player_name)

while(True):
    if(s.my_turn(player)):
        print("My turn")
        time.sleep(1)
        #it's my turn
    else:
        print("NOT My turn")
        time.sleep(5)
        #it's not my turn
