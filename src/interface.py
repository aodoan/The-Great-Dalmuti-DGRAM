from src.roteamento import *
from src.interface import *

#imprime as informacoes de player info, e a mao de cada jogador
def imprime_tela(player_info, card_set, jogada, rodada):
    #os.system('clear')
    print_header()
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

    
    #imprime a qtd de cartas
    for score in range(0, num):
        size = len(handle(score+1))
        n = (size // 2) - 1
        print(" " * n, end='')
        print(player_info[score], end='')
        print(" " * (n+SPACE), end='')
    print()
    
    print_separator()
    #se o jogador nao tem cartas imprime mensagem final
    if(len(card_set) == 0):
        #imprime_final()
        print_middle("Voce terminou seu baralho!")
    else:
        imprime_cartas(card_set)
    print_separator()

#imprime \n para "limpar" o terminal
def flush_terminal():
    print("\n" * 100)

def imprime_fim(winner_list):
    for i in range(0, len(winner_list)):
        nickname = handle(winner_list[i][0])
        print(f"{i+1}° posicao -> {nickname} terminou suas cartas na rodada {winner_list[i][1]}")

def print_m(text):
    string = str(text)
    num = (how_many - len(string)) // 2
    print(" " * num + string)

