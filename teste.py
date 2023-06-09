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

a = cria_mensagem_cartas()
hand_set = recebe_baralho(a)
print(hand_set)

def atualiza_dados(msg, player_info):
    #ve quem mandou
    origem = msg[1] - 1
    #por enquanto o modo de enviar jogada e uma lista com duas posicoes
    #posicao 0 quantas cartas, posicao 1 qual valor da carta
    player_info[origem] = player_info[origem] - msg[2][0]
    return player_info

#passa a ultima jogada que foi feita
#funcao precaria, arrumar o quanto antes que vergonha
def get_jogada(jogada):
    imprime_cartas(hand_set)
    if(jogada[0] != 0):
        print(f"A ultima jogada foi: {jogada[0]} cartas de nivel {jogada[1]}")
    else:
        print("Faca a sua jogada: ")
    while True:
        if(jogada[0] == 0):
            op = 'J'
        else:
            op = input("J - Jogar, P - Passar: ")
        if(op == "j" or op == "J"):
            while True:
                try:
                    q, n = input("Digite sua jogada [qtd/nivel] ").split(" ", 2)
                    break
                except:
                    print("Digite os inputs corretamente.") 
            
            qtd = int(q)
            nivel = int(n)
            print(f"{qtd} cartas do nivel {nivel}")
            
            #verifica se a jogada eh valida
            if(jogada[0] != qtd):
                print("Voce precisa jogar o mesmo numero de cartas!")
            elif(nivel >= jogada[1]):
                print("Voce precisa jogar cartas com nivel menor!")

            #chega aqui somente se a jogada for valida, agora verifica se ele tem as cartas
            else:
                #verifica se tem as cartas do nivel requerido
                if(hand_set.count(nivel) >= qtd):
                    for i in range(0, qtd):
                        hand_set.remove(nivel)  # remove as cartas do baralho se tiver
                    print("jogada feita!")
                    jogada[0] = qtd             # atribui os valores para jogada e retorna
                    jogada[1] = nivel           #
                    player_info[ordem-1] -= qtd #diminui a quantidade de cartas
                    #se tiver, printa e vaza
                    return jogada
                    break
                else:
                    print("voce nao tem a carta para jogar!")

        elif(op == "P" or op == "p"):
            print("Voce passou a vez!")
            return jogada
            break
    

#jogada = [0] * 2
jogada = []
jogada.append(1)
jogada.append(10)
msg = cria_mensagem(jogada)

print(player_info)
print(jogada)
jogada = get_jogada(jogada)
print(jogada)
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
