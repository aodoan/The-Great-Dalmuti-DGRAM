import configparser
import socket
#definicoes

hostname = socket.gethostname()
CARTEADOR = 1

CONFIG_FILE = "config.txt" #arquivo de configuracao
UDP_PORT = 8080            #porta padrao de comunicacao
MARCADOR_INICIO = "INICIO"
MARCADOR_FIM = "FIM"
PRIMEIRO_A_JOGAR = 1 # define quem eh o grande dalmuti na primeira rodada
BOLDS = '\033[1m'
BOLDE = '\033[0m'
SPACE = 5

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

#retorna o nick do jogador de acordo com a ordem
def handle(ordem):
    return config.get('HANDLE', str(ordem))


def order(IP):
    for key, value in config.items('IP'):
        if(value == IP):
            ordem = key
    return int(ordem)

#imprime um texto em bold sem new line
def bold(text):
    print(BOLDS + text + BOLDE, end=' ')

ordem = order(socket.gethostbyname(hostname))

def header_info():
    contador = 0
    for player in range(1, num+1):
        contador = contador + len(handle(player))
        contador = contador + SPACE
    return contador

how_many = header_info()
GAMENAME = "The Great Dalmuti"
spaces = (how_many - len(GAMENAME)) // 2

def print_header():
    print('-'*how_many)
    print(" " * spaces + GAMENAME)
    print('-'*how_many)

spacesC = (how_many - 9) // 2
def imprime_cartas(card_set):
    for i in range(1, 14):
        r = card_set.count(i)
        #so imprime se houver carta
        if(r > 0):
            print(" "*spaces + f"[{i:2}] -> {r}")

def imprime_final():
    print(" "*spaces + "voce terminou seu baralho!")

def imprime_jogada(player_info, jogada):
    if(jogada[0] != 0): #tem alguma jogada pra imprimir
        print(f"A ultima jogada feita foi {jogada[0]} cartas do nivel {jogada[1]}")
    else:
        player = handle(player_info[num])
        print(f"{player} vai comecar a rodada.")

def print_separator():
    print('-'*how_many)
