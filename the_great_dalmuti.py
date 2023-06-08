from roteamento import *
from receive import *
from teste import *
from client import *

player_info = [20] * num

def atualiza_dados(msg, player_info):
    #ve quem mandou
    origem = msg[1] - 1
    #por enquanto o modo de enviar jogada e uma lista com duas posicoes
    #posicao 0 quantas cartas, posicao 1 qual valor da carta
    player_info[origem] = player_info[origem] - msg[2][0]
    return player_info


def main():
    hand = []
    #verifica se eh o carteador, senao espera carta
    if(ordem == CARTEADOR):
        msg = cria_mensagem_cartas()
        print(msg)
        #pega as proprias cartas
        hand = recebe_baralho(msg)
        msg[2] = msg[2][20:]
        #envia
        send(msg)
        #espera confirmacao para continuar
        msgR = recebe_mensagem()
        if(msgR[3].count(1) != num):
            print("Algo deu errado no embaralhamento!")
            quit()
    #se cair nesse else, precisa esperar carta
    else:
        msg = recebe_mensagem()
        hand = recebe_baralho(msg) #
        msg[2] = msg[2][20:] # exclui tudo o que ele pegou da lista
        msg[3][ordem-1] = 1 #marca que recebeu
        send(msg)

    #loop do jogo
    fim_de_jogo = 0
    BASTAO = 1 #define o bastao inicialmente com o jogador 1
    while (fim_de_jogo != 1):
        #imprime_dados()
        #verifica se a maquina atual tem o bastao
        if(ordem == BASTAO):
            print("faz a jogada...")
            
        else:
            #espera algo, e quando receber manda pra frente, consumindo as paradas
            msg = recebe_mensagem()
            atualiza_dados(msg, player_info) #atualiza os dados
            msg[3][ordem-1] = 1 # confirma que recebeu
            send(msg) #envia a mensagem para proximo da rede





if __name__ == "__main__":
    main()