from roteamento import *
from receive import *
from teste import *
from client import *
import time
"""
    TODO: colocar as mensagens indicando a rodada talvez
          fazer um menu bonitinho pra mostra tudo etc
          provavelmente refazer a get_jogada
          se a pessoa ja ganhou, so confirma a mensagem e manda pra frente
          +a sua jogada e passar sempre
"""


def main():
    hand = []
    #verifica se eh o carteador, senao espera carta
    if(ordem == CARTEADOR):
        trash = input("Pressione ENTER para distrubir as cartas!")
        msg = cria_mensagem_cartas()
        #pega as proprias cartas
        hand = recebe_baralho(msg)
        msg[2] = msg[2][20:]
        #envia
        send(msg)
        #espera confirmacao para continuar
        msgR = recebe_mensagem()
        #ocorreu algum erro, aborta a operacao
        if(msgR[3].count(1) != num):
            print("Algo deu errado no embaralhamento!")
            quit()
    #se cair nesse else, precisa esperar carta
    else:
        msg = recebe_mensagem()
        hand = recebe_baralho(msg) 
        msg[2] = msg[2][len(hand):] # exclui tudo o que ele pegou da lista
        msg[3][ordem-1] = 1 # marca que recebeu
        send(msg)

    #loop do jogo
    fim_de_jogo = 0
    player_info = [len(hand)] * num # lista que guarda quantas cartas cada jogador tem no momento
    player_info.append(PRIMEIRO_A_JOGAR) # quem ta com o bastao
    
    #se ele for o primeiro a jogar, fica com o bastao
    if(ordem == PRIMEIRO_A_JOGAR):
        BASTAO = 1
    else:
        BASTAO = 0

    jogada = [0] * 4
    venceu = 0
    winner_list = []
    while (fim_de_jogo != 1):
        #flush_terminal()
        print(hand)
        imprime_tela(player_info, hand, jogada)
        #verifica se a maquina atual tem o bastao
        #se sim, pede a jogada
        if(BASTAO == 1):
            jogada_antiga = jogada.copy()
            jogada = get_jogada(jogada, hand, venceu)
            msg = cria_mensagem(jogada, winner_list)
            #verifica se a jogada mudou ou se foi passada
            if(jogada_antiga[1] != jogada[1]): 
                player_info[ordem-1] = player_info[ordem-1] - jogada[0]
            
            #se zerou as cartas, termina a jogada
            if(len(hand) == 0):
                venceu = 1 # altera o estado do jogador para venceu
                if not(ordem in winner_list):
                    winner_list.append(ordem)
            
            send(msg) # envia a jogada pra todo mundo
            msgR = recebe_mensagem()
            msg = cria_mensagem_bastao(msgR) # envia o bastao para frente
            send(msgR)
            BASTAO = 0 # perde o bastao
            player_info[num] += 1 % (num+1)
        else:
            #espera algo, e quando receber manda pra frente, consumindo as paradas
            msg = recebe_mensagem()
            print(msg)
            player_info[num] = ((player_info[num] % (num))) + 1
            jogada = msg[2]
            winner_list = msg[5]
            if(len(winner_list) == num-1):
                fim_de_jogo = 1
                #o jogo acabou
            if("bastao" in msg):
                #player_info.append(ordem) # quem ta com o bastao
                player_info[num] = ordem
                BASTAO = 1      # ele ta com o bastao, pode fazer a jogada
                if(jogada[2] == ordem): # significa que todo mundo passou, ele ganha a rodada
                    jogada = [0] * 4    # marca como zero a jogada
            else:
                player_info = atualiza_dados(jogada, player_info) #atualiza os dados
                # se ele n for receber o bastao
                #atualiza_dados(msg, player_info) #atualiza os dados
                msg[3][ordem-1] = 1 # confirma que recebeu
                send(msg) #envia a mensagem para proximo da rede
    print(winner_list)



if __name__ == "__main__":
    main()

