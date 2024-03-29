from src.roteamento import *
import socket
import pickle

#recebe uma mensagem e manda pra quem ta no roteamento
def send(MESSAGE):
    #verifica pra quem ele deve mandar
    hostname = socket.gethostname()
    ip_local = socket.gethostbyname(hostname)
    #endereco para a qual ele deve mandar
    UDP_IP = rota[ip_local]
    #UDP_IP = "localhost"
    #UDP_IP = socket.gethostbyname(hostname)
    #data = MESSAGE.encode()
    data = pickle.dumps(MESSAGE)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(data, (UDP_IP, UDP_PORT))

