from src.roteamento import *
import socket
import pickle #binary etc

#fica na mensagem ate receber algo, retorna a mensagem completa

hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def recebe_mensagem():   
    lista = []
    while True:
        data, addr = sock.recvfrom(1024)
        #print("recebi dado")
        lista = pickle.loads(data)
        break
    return lista

def main():
        lista = recebe_mensagem()
        print(lista)


if __name__ == "__main__":
    main()
