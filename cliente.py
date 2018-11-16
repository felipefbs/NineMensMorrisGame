import xmlrpc.client

s = xmlrpc.client.ServerProxy('http://localhost:9999')


player_name = str(input())
player = s.login(player_name)