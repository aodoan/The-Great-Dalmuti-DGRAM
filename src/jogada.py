from src.roteamento import *

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
        elif(jester_qtd > 0): #tem algum valete
            op = input("J - Jogar, P - Passar, JE - Jogar com um coringa: ")
        else:
            op = input("J - Jogar, P - Passar: ")
        op = op.replace(" ", "")
        op = op.upper()
        if(op == "JE" and jester_qtd > 0):
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
                    if((1 <= int(n) <= 12)):
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
