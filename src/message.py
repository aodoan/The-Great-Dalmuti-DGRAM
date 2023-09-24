from src.roteamento import *
from src.interface import *
import random

#le um numero de 1 a 80 e atribui seu valor
def return_carta(num):
    contador = 0
    if(num == 79 or num == 80):
        return 13
    for i in range(1, 13):
        for j in range(0, i):
            contador += 1
            if(contador == num):
                return i

#cria uma lista de 1 a 80 e embaralha
def embaralha():
    cartas = []
    for i in range(1, 81):
        cartas.append(i)
    random.shuffle(cartas)
    return cartas


#cria uma mensagem em forma de lista

#FORMATACAO DAS MENSAGENS
#marcador de inicio
#origem da mensagem
#jogada
#campo de confirmacao
#campo para trocar o bastao
#lista de vencedores
#marcador de fim
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

#cria uma mensagem de entregar cartas
#FORMATACAO
#marcador de inicio
#origem da mensagem
#lista de cartas
#campo de confirmacao
#marcador de fim
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

#recebe uma mensagem e retorna somente as cartas do seu baralho
def recebe_baralho(mensagem):
    baralho = mensagem[2][:num_cards]
    baralho.sort()
    return baralho

#recebe uma jogada e atualiza na estrutura player_info de cada maquina
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

# mensagem que passa o bastao para frente
def cria_mensagem_bastao(msg):
    msg[4] = "bastao"
    return msg

def cria_mensagem_passagem(msg):
    msg[4] = "passando"
    return msg

#incrementa a ordem (mantem em controle quem ta com o bastao)
def add_ordem(ordem):
    ordem = ordem + 1
    if(ordem > num):
        ordem = 1
    return ordem

