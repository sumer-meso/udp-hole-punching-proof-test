import socket
import sys
import threading

rendezvous = (sys.argv[1], int(sys.argv[2]))

# connect to rendezvous
print('Connecting to rendezvous server at', rendezvous)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))
sock.sendto(b'hey, im here.', rendezvous)

while True:
    data = sock.recv(1024).decode()

    if data.strip() == 'ready':
        print('Checked in with server, waiting for infor for another peer ...')
        break

data = sock.recv(1024).decode()
ip, sport= data.split(' ')
sport = int(sport)

print('\ngot peer')
print('  ip:          {}'.format(ip))
print('  source port: {}'.format(sport))

print('Punching hole ...')
# This step is important to update the 5-tuple entries in the state table on NAT/firewall with the peer's ip:port.
# https://blog.ipfs.tech/2022-01-20-libp2p-hole-punching/
sock.sendto(b'bang', (ip, sport))
print('Ready to exchange messages\n')

# listen for messages from the other side.
def listen():
    while True:
        data = sock.recv(1024)
        print('\rpeer: {}\n>'.format(data.decode()), end='')

listener = threading.Thread(target=listen, daemon=True)
listener.start()

while True:
    msg = input('> ')
    sock.sendto(msg.encode(), (ip, sport))
