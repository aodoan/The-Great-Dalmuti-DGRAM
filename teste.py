from roteamento import *
import socket
import random
import shutil
import client
import os

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


#quando a maquina tem o bastao, eh solicitado sua jogada
#retorna a jogada do usuario (passou ou fez uma jogada em cima)
#se o usuario ja ganhou, so passa
def get_jogada(jogada, hand_set, venceu):
    jester_qtd = hand_set.count(13)
    jester = 0
    #se a pessoa ja venceu, so passa a vez
    if(venceu == 1):
        jogada[3] = 1 # indica que a jogada ja foi passada
        return jogada

    while True:
        if(jogada[0] == 0): # se eh a primeira jogada da rodada, nem pergunta
            if(jester_qtd == 0):
                op = 'J'
            else:
                op = input("J - Jogar, JE - Jogar com um coringa: ")
                op = op.upper()
                if(op != 'J' and op != 'JE'):
                    op = 'lixo'
        elif(jester > 0): #tem algum valete
            op = input("J - Jogar, P - Passar, JE - Jogar com um coringa: ")
        else:
            op = input("J - Jogar, P - Passar: ")
        op = op.replace(" ", "")
        op = op.upper()
        if(op == "JE"):
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
        else:
            print("Jogada invalida!")

# mensagem que passa o bastao para frente
def cria_mensagem_bastao(msg):
    msg[4] = "bastao"
    return msg

def cria_mensagem_passagem(msg):
    msg[4] = "passando"
    return msg


#imprime as informacoes de player info, e a mao de cada jogador
def imprime_tela(player_info, card_set, jogada, rodada):
    #os.system('clear')
    print_header()
    #print(" " * spaces + f"Rodada {rodada}")
    imprime_meio(rodada)
    imprime_jogada(player_info, jogada)
    print_separator()
    #imprime os logins
    for player in range(1, num+1):
        if(player != player_info[num]):
            print(f"{handle(player)}", end=' '*SPACE)
        else:
            print(BOLDS + handle(player) + BOLDE, end=' '*SPACE)

    print()

    if(True):
        #imprime a qtd de cartas
        for score in range(0, num):
            size = len(handle(score+1))
            n = (size // 2) - 1
            print(" " * n, end='')
            print(player_info[score], end='')
            print(" " * (n+SPACE), end='')
        print()
    print_separator()
    if(len(card_set) == 0):
        #imprime_final()
        print_middle("Voce terminou seu baralho!")
    else:
        imprime_cartas(card_set)
    print_separator()

#imprime \n para "limpar" o terminal
def flush_terminal():
    print("\n" * 100)

#incrementa a ordem (mantem em controle quem ta com o bastao)
def add_ordem(ordem):
    ordem = ordem + 1
    if(ordem > num):
        ordem = 1
    return ordem

def imprime_fim(winner_list):
    for i in range(0, len(winner_list)):
        nickname = handle(winner_list[i][0])
        print(f"{i+1}° posicao -> {nickname} terminou suas cartas na rodada {winner_list[i][1]}")

def print_m(text):
    string = str(text)
    num = (how_many - len(string)) // 2
    print(" " * num + string)

