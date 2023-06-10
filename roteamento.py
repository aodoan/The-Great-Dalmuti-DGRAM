import configparser
import socket
#definicoes

hostname = socket.gethostname()
CARTEADOR = 1

CONFIG_FILE = "config.txt" #arquivo de configuracao
UDP_PORT = 8080            #porta padrao de comunicacao
MARCADOR_INICIO = "INICIO"
MARCADOR_FIM = "FIM"
PRIMEIRO_A_JOGAR = 1
f = open(CONFIG_FILE, "r")
conteudo = f.read()
config = configparser.RawConfigParser()
config.read(r'config.txt')



def num_players():
    num = int(config.get('NUM', 'player'))
    return num

num = num_players()

def players():
    num = num_players()
    #inicia lista de jogadores
    players = []
    #loop que le o nome de todos os jogadores
    for i in range(1, num+1):
        players.append(config.get('HANDLE', str(i)))
    return players

player_list = players()

def ip():
    num = num_players()
    ip_a = []
    #le os ips de cada maquina
    for i in range(1, num+1):
        ip_a.append(config.get('IP', str(i)))
    return ip_a

ip_list = ip()

def rota():
    IP = ip()
    num = num_players()
    #cria um dicionario com o endereco que cada maquina deve conectar
    rota = dict()
    i = 0
    for ip_a in IP:
        rota[ip_a] = IP[(i+1)%num]
        i += 1
    return rota

rota = rota()

#recebe o ip local e retorna o seu nick
def player_handle(IP):
    for key, value in config.items('IP'):
        if(value == IP):
            ordem = key
    return config.get('HANDLE', str(ordem))


def order(IP):
    for key, value in config.items('IP'):
        if(value == IP):
            ordem = key
    return int(ordem)

ordem = order(socket.gethostbyname(hostname))
