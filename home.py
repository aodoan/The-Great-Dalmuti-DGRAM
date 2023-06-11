
from roteamento import *
import socket
import random
import shutil
import client
from teste import *
import os
import time
player_info = [20] * 4
player_info.append(2)

msg = cria_mensagem_cartas()
hand = recebe_baralho(msg)

imprime_tela(player_info, hand)

jogada = []
jogada.append(2)
jogada.append(5)
jogada.append(3)


imprime_tela(player_info, hand)