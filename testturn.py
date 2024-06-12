import socket
import sys
import threading

rendezvous = ('45.63.87.161', 12345)

# connect to rendezvous
print('Connecting to rendezvous server at', rendezvous)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))
sock.sendto(b'hey, im here.', rendezvous)

# listen for messages from the other side.
def listen():
    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n>'.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), rendezvous)
