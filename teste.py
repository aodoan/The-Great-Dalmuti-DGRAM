from roteamento import *
import socket
import random
import shutil
import client


def return_carta(num):
    contador = 0
    if(num == 79 or num == 80):
        return 13
    for i in range(1, 13):
        for j in range(0, i):
            contador += 1
            if(contador == num):
                return i

def imprime_cartas(card_set):
    for i in range(1, 14):
        r = card_set.count(i)
        #so imprime se houver carta
        if(r > 0):
            print(f"[{i:2}] -> {r}")
    
#cria uma lista de 1 a 80 
def embaralha():
    cartas = []
    for i in range(1, 81):
        cartas.append(i)
    random.shuffle(cartas)
    return cartas

# marcador de inicio | origem | dados (jogada) e numero de passadas | FIM
def cria_mensagem(jogada):
    mensagem = []
    mensagem.append(MARCADOR_INICIO)
    mensagem.append(ordem)
    #tem um campo pra jogada
    mensagem.append(jogada)
    
    confirmacao = [0] * num
    confirmacao[ordem-1] = 1
    mensagem.append(confirmacao)

    #inicia o contador de quantas rodadas foram passadas desde a ultima jogada
    mensagem.append(0)
    mensagem.append(MARCADOR_FIM)
    print(mensagem)
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

player_info = [20] * num

def atualiza_dados(msg, player_info):
    #ve quem mandou
    origem = msg[1] - 1
    #por enquanto o modo de enviar jogada e uma lista com duas posicoes
    #posicao 0 quantas cartas, posicao 1 qual valor da carta
    player_info[origem] = player_info[origem] - msg[2][0]
    return player_info

def get_jogada():
    

jogada = []
jogada.append(2)
jogada.append(4)
lista = cria_mensagem(jogada)
print(player_info)
atualiza_dados(lista, player_info)
print(player_info)

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
