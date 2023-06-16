from roteamento import *
from receive import *
from teste import *
from client import *

def main():
    hand = []
    jogada = [0] * 4
    rodada = 1
    #verifica se eh o carteador, senao espera carta
    if(ordem == CARTEADOR):
        trash = input("Pressione ENTER para distrubir as cartas!")
        msg = cria_mensagem_cartas()
        #pega as proprias cartas
        hand = recebe_baralho(msg)
        msg[2] = msg[2][num_cards:]
        #envia
        send(msg)
        #espera confirmacao para continuar
        msgR = recebe_mensagem()
        #ocorreu algum erro, aborta a operacao
        if(msgR[3].count(1) != num):
            print("Algo deu errado no embaralhamento!")
            quit()

        #se o carteador for o mesmo de entregar as cartas continue
        if(PRIMEIRO_A_JOGAR != CARTEADOR):
            #lista vazia (lixo)
            mt = []
            msg = cria_mensagem(jogada, mt)
            send(msg)

    #se cair nesse else, precisa esperar carta
    else:
        msg = recebe_mensagem()
        hand = recebe_baralho(msg)
        msg[2] = msg[2][num_cards:] # exclui tudo o que ele pegou da lista
        msg[3][ordem-1] = 1 # marca que recebeu
        send(msg)
        if(CARTEADOR != PRIMEIRO_A_JOGAR):
            msg = recebe_mensagem()
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

    venceu = 0
    winner_list = []
    while (fim_de_jogo != 1):
        flush_terminal()
        imprime_tela(player_info, hand, jogada, rodada)
        #verifica se a maquina atual tem o bastao
        #se sim, pede a jogada
        if(BASTAO == 1):
            jogada_antiga = jogada.copy()
            jogada = get_jogada(jogada, hand, venceu)
            msg = cria_mensagem(jogada, winner_list)
            #verifica se a jogada mudou ou se foi passada
            #se zerou as cartas, termina a jogada
            if(len(hand) == 0 and venceu == 0):
                venceu = 1 # altera o estado do jogador para venceu
                info = []
                info.append(ordem)
                info.append(rodada)
                winner_list.append(info)
                if(len(winner_list) >= num-1):
                    fim_de_jogo = 1

            send(msg) # envia a jogada pra todo mundo
            msgR = recebe_mensagem()
            msg = cria_mensagem_bastao(msgR) # envia o bastao para frente
            send(msgR)
            BASTAO = 0 # perde o bastao
            player_info[num] = add_ordem(ordem)
        else:
            #espera algo, e quando receber manda pra frente, consumindo as paradas
            msg = recebe_mensagem()
            #player_info[num] = add_ordem(player_info[num])
            jogada = msg[2]
            winner_list = msg[5]
            #player_info = atualiza_dados(msg, player_info)
            if(len(winner_list) == num-1):
                fim_de_jogo = 1
                #o jogo acabou
            if("bastao" in msg):
                #player_info.append(ordem) # quem ta com o bastao
                player_info = atualiza_dados(jogada, player_info)
                player_info[num] = ordem
                #envia a mensagem para todo mundo 
                if(jogada[2] == ordem): # significa que todo mundo passou, ele ganha a rodada
                    jogada = [0] * 4    # marca como zero a jogada
                    rodada += 1
                msg = cria_mensagem(jogada, winner_list)
                msg = cria_mensagem_passagem(msg)
                send(msg)
                msgR = recebe_mensagem()
                BASTAO = 1
            else:
                #player_info = atualiza_dados(jogada, player_info) #atualiza os dados
                if("passando" in msg):
                    player_info = atualiza_dados(jogada, player_info)
                    player_info[num] = msg[1]
                    if(jogada[0] == 0): #incrementa a rodada
                        player_info[ordem-1] = player_info[ordem-1] - jogada[0]
                        rodada += 1
                        player_info[num] = msg[1]
                # se ele n for receber o bastao
                msg[3][ordem-1] = 1 # confirma que recebeu
                send(msg) #envia a mensagem para proximo da rede
    imprime_fim(winner_list)



if __name__ == "__main__":
    main()

