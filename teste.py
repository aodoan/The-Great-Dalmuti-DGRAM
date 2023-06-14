from roteamento import *
import socket
import random
import shutil
import client
import os

def return_carta(num):
    contador = 0
    if(num == 79 or num == 80):
        return 13
    for i in range(1, 13):
        for j in range(0, i):
            contador += 1
            if(contador == num):
                return i



#cria uma lista de 1 a 80
def embaralha():
    cartas = []
    for i in range(1, 81):
        cartas.append(i)
    random.shuffle(cartas)
    return cartas

# marcador de inicio | origem | quem fez a ultima jogada | dados (jogada) e numero de passadas | FIM
def cria_mensagem(jogada, winner_list):
    mensagem = []
    mensagem.append(MARCADOR_INICIO)
    mensagem.append(ordem)
    #tem um campo pra jogada

    mensagem.append(jogada)

    confirmacao = [0] * num
    confirmacao[ordem-1] = 1
    mensagem.append(confirmacao)

    #lugar para deixar caso para trocar de bastao
    mensagem.append(0)
    mensagem.append(winner_list)
    mensagem.append(MARCADOR_FIM)
    return mensagem


# marcador inicio | origem | dados | FIM
def cria_mensagem_cartas():
    mensagem = []
    mensagem.append(MARCADOR_INICIO) #inicio
    mensagem.append(ordem) # marca quem mandou
    lista = embaralha() # inicia um vetor com valores de 1 a 80 embaralhados
    for i in range(0, 80):
        lista[i] = return_carta(lista[i]) # atribui o valor de cada carta corretamente
    mensagem.append(lista)
    confirmacao = [0] * num
    confirmacao[ordem-1] = 1
    mensagem.append(confirmacao) # campos de confirmacao de recebimento
    mensagem.append(MARCADOR_FIM)
    return mensagem

#recebe uma mensagem inteira e retorna somente as suas cartas
def recebe_baralho(mensagem):
    baralho = mensagem[2][:20]
    baralho.sort()
    return baralho


def atualiza_dados(jogada, player_info):
    if(jogada == None):
        return player_info
    #ve quem mandou
    if(jogada[3] == 0):
        origem = jogada[2] - 1
        print(f'estou atualizando dados do {origem} com {jogada[0]}')
        player_info[origem] = player_info[origem] - jogada[0]

    #por enquanto o modo de enviar jogada e uma lista com duas posicoes
    #poer_info[origem] = player_info[origem] - msg[2][0]
    return player_info

# passa a ultima jogada que foi feita
# se passou retorna a mesma jogada
# se for a primeira jogada da rodada, tem que passar uma lista zerada
# funcao precaria, arrumar o quanto antes que vergonha
def get_jogada(jogada, hand_set, venceu):
    jester = 0
    #se a pessoa ja venceu, so passa a vez
    if(venceu == 1):
        jogada[3] = 1 # indica que a jogada ja foi passada
        return jogada

    while True:
        if(jogada[0] == 0): # se eh a primeira jogada da rodada, nem pergunta
            op = 'J'
        elif(hand_set.count(13) > 0): #tem algum valete
            op = input("J - Jogar, P - Passar, JE - Jogar com um coringa: ")
        else:
            op = input("J - Jogar, P - Passar: ")
        op = op.replace(" ", "")
        op = op.upper()
        if(op == "JE" or op == "je"):
            op = 'j'
            jester = 1

        if(op == "j" or op == "J"):
            while True:
                try:
                    q, n = input("Digite sua jogada [qtd/nivel] ").split(" ", 2)
                except:
                    print("Digite os dados corretamente")
                    continue
                if(int(q) and int(n)):
                    break;
            qtd = int(q)
            nivel = int(n)
            print(f"{qtd} cartas do nivel {nivel}")
            if(jester == 1):
                hand_set.remove(13) # tira um coringa
                hand_set.append(nivel) # adiciona mais uma carta na mao
            #so verifica se teve alguma jogada antes


            if(jogada[0] != qtd and jogada[0] != 0):
                print("Voce precisa jogar o mesmo numero de cartas!")
                if(jester == 1):
                    hand_set.remove(nivel) # tira um coringa
                    hand_set.append(13) # adiciona mais uma carta na mao
                    jester = 0
            elif(nivel >= jogada[1] and jogada[0] != 0):
                print("Voce precisa jogar cartas com nivel menor!")
                if(jester == 1):
                    hand_set.remove(nivel) # tira um coringa
                    hand_set.append(13) # adiciona mais uma carta na mao
                    jester = 0
            else:
                #chega aqui somente se a jogada for valida, agora verifica se ele tem as cartas
                #verifica se tem as cartas do nivel requerido
                if(hand_set.count(nivel) >= qtd):
                    for i in range(0, qtd):
                        hand_set.remove(nivel)  # remove as cartas do baralho se
                    #print("jogada feita!")
                    jogada[0] = qtd             # atribui os valores para jogada e retorna
                    jogada[1] = nivel           #
                    jogada[2] = ordem           # define quem fez a jogada
                    jogada[3] = 0
                    #se tiver, printa e vaza
                    return jogada
                else:
                    print("voce nao tem a carta para jogar!")

        elif(op == "P" or op == "p"):
            print("Voce passou a vez!")
            jogada[3] = 1
            return jogada

# mensagem que passa o bastao para frente
def cria_mensagem_bastao(msg):
    msg[4] = "bastao"
    return msg

#imprime o handle de cada um,
def imprime_tela(player_info, card_set, jogada):
    #os.system('clear')
    print_header()
    imprime_jogada(player_info, jogada)
    print_separator()
    #imprime os logins
    for player in range(1, num+1):
        if(player != player_info[num]):
            print(f"{handle(player)}", end=' '*SPACE)
        else:
            print(BOLDS + handle(player) + BOLDE, end=' '*SPACE)

    print()

    if(len(card_set) == 0):
        imprime_final()
    else:
        #imprime a qtd de cartas
        for score in range(0, num):
            size = len(handle(score+1))
            n = (size // 2) - 1
            print(" " * n, end='')
            print(player_info[score], end='')
            print(" " * (n+SPACE), end='')
        print()
    print_separator()
    imprime_cartas(card_set)
    print_separator()

def flush_terminal():
    print("\n" * 100)
    '''
lista = cria_mensagem_cartas()
print(lista)
hand = recebe_baralho(lista)
print(hand)
print(lista)

lista = cartas[:20]
lista.sort()
a = 0
for card in lista:
    lista[a] = return_carta(card)
    a += 1
imprime_cartas(lista)
'''
