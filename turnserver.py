import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 12345))


print('Listening on {}:{}.'.format(sock.getsockname()[0], sock.getsockname()[1]))
def listen():
    while True:
        clients = []

        while True:
            data, address = sock.recvfrom(1024)

            print('Connection from: {} with {}'.format(address, data))
            clients.append(address)

            if len(clients) == 2:
                print('Got 2 clients, will send things to each other.')
                break

        while True:
            data, address = sock.recvfrom(8192)
            print('Got something from: {} with {}'.format(address, data))
            if address == clients[0]:
                print('Sending to the other side {}'.format(clients[1]))
                sock.sendto(data, clients[1])
            else:
                print('Sending to the other side {}'.format(clients[0]))
                sock.sendto(data, clients[0])


listener = threading.Thread(target=listen, daemon=True)
listener.start()


while True:
    msg = input('ctrl-c to exit.')