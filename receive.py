from roteamento import *
import socket
import pickle #binary etc

#define a porta
hostname = socket.gethostname()
UDP_IP = socket.gethostbyname(hostname)
#UDP_IP = "localhost"


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
#sock.bind((UDP_IP, 2000))

#fica na mensagem ate receber algo, retorna a mensagem completa
def recebe_mensagem():
    lista = []
    while True:      
        data, addr = sock.recvfrom(1024) 
        lista = pickle.loads(data)
        break
    return lista

def main():
    
        print("vou esperar mensagem!")
        lista = recebe_mensagem()
        print(lista)
        

if __name__ == "__main__":
    main()