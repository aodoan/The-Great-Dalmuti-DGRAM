from roteamento import *
import socket
import pickle #binary etc

#define a porta
"""
hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
#UDP_IP = "localhost"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
"""
#fica na mensagem ate receber algo, retorna a mensagem completa
def recebe_mensagem():
    hostname = socket.gethostname()
    UDP_IP = socket.gethostbyname(hostname)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    lista = []
    while True:
        data, addr = sock.recvfrom(1024)
        #print("recebi dado")
        lista = pickle.loads(data)
        break
    return lista

def main():
        print("vou esperar mensagem!")
        lista = recebe_mensagem()
        print(lista)


if __name__ == "__main__":
    main()

