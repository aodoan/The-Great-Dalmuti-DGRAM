from roteamento import *
from receive import *
from teste import *
from client import *
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
        print(hand)
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
    player_info = [len(hand)] * num
    player_info.append(PRIMEIRO_A_JOGAR) # quem ta com o bastao
    if(ordem == PRIMEIRO_A_JOGAR):
        jogada = [0] * 4
        BASTAO = 1
    else:
        jogada = [0] * 4
        BASTAO = 0
    venceu = 0
    while (fim_de_jogo != 1):
        #por algum motivo obscuro, usar clear fode todo o jogo
        imprime_tela(player_info, hand)
        #imprime_dados()
        #verifica se a maquina atual tem o bastao
        if(BASTAO == 1):
            jogada_antiga = jogada.copy()
            jogada = get_jogada(jogada, hand, venceu)
            msg = cria_mensagem(jogada)
            print(jogada_antiga)
            print(jogada)
            if(jogada_antiga[1] != jogada[1]): # se a jogada mudo
                print("a jogada mudou")
                player_info[ordem-1] = player_info[ordem-1] - jogada[0]
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
            jogada = msg[2]
            if("bastao" in msg):
                print("recebi o bastao")
                #player_info.append(ordem) # quem ta com o bastao
                player_info[num] = ordem
                BASTAO = 1      # ele ta com o bastao, pode fazer a jogada
                if(jogada[2] == ordem): # significa que todo mundo passou, ele ganha a rodada
                    jogada = [0] * 3    # marca como zero a jogada
            else:
                player_info = atualiza_dados(jogada, player_info) #atualiza os dados
                player_info[num] += 1 % (num+1)
                # se ele n for receber o bastao
                print("passei por aqui")
                #atualiza_dados(msg, player_info) #atualiza os dados
                msg[3][ordem-1] = 1 # confirma que recebeu
                send(msg) #envia a mensagem para proximo da rede



if __name__ == "__main__":
    main()
