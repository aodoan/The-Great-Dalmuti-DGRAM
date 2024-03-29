import configparser
import socket
import math

hostname = socket.gethostname()

MARCADOR_INICIO = "INICIO"
MARCADOR_FIM = "FIM"

BOLDS = '\033[1m'
BOLDE = '\033[0m'
SPACE = 5

#abre o arquivo de configuracao
CONFIG_FILE = "./config.txt" #arquivo de configuracao
f = open(CONFIG_FILE, "r")
conteudo = f.read()
config = configparser.RawConfigParser()
config.read(r'config.txt')


def num_players():
    num = int(config.get('GAME_INFO', 'player'))
    return num

num = num_players()
num_cards = math.ceil(80/num)
total = num_cards * num

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


PRIMEIRO_A_JOGAR = int(config.get('GAME_INFO', "first_to_play"))
CARTEADOR = int(config.get('GAME_INFO', "player_deal"))
UDP_PORT = int(config.get('GAME_INFO', "UDP_PORT"))

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

def imprime_meio(rodada):
    string = "Rodada " + str(rodada)
    num = (how_many - len(string)) // 2
    print(" " * num + string)

def print_middle(text):
    string = str(text)
    num = (how_many - len(string)) // 2
    print(" " * num + string)


def imprime_jogada(player_info, jogada):
    if(jogada[0] != 0): #tem alguma jogada pra imprimir
        string = "A ultima jogada feita foi " + str(jogada[0]) +" cartas do nivel " + str(jogada[1])
        print_middle(string)
    else:
        player = handle(player_info[num])
        #print(f"{player} vai comecar a rodada.")
        string = str(player) + " vai comecar a rodada"
        print_middle(string)

def print_separator():
    print('-'*how_many)

