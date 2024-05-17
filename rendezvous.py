import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect(('1.1.1.1', 0))


def listen():
    while True:
        clients = []

        while True:
            print('Listening on {}:{}.'.format(sock.getsockname()[0], sock.getsockname()[1]))
            print('Peers command: ./client.py {} {}.'.format(sock.getsockname()[0], sock.getsockname()[1]))
            data, address = sock.recvfrom(128)

            print('connection from: {}'.format(address))
            clients.append(address)

            sock.sendto(b'ready', address)

            if len(clients) == 2:
                print('got 2 clients, sending details to each.')
                break

        c1 = clients.pop()
        c1_addr, c1_port = c1
        c2 = clients.pop()
        c2_addr, c2_port = c2

        sock.sendto('{} {}'.format(c1_addr, c1_port).encode(), c2)
        sock.sendto('{} {}'.format(c2_addr, c2_port).encode(), c1)

listener = threading.Thread(target=listen, daemon=True)
listener.start()


while True:
    msg = input('ctrl-c to exit.')