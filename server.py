import socket
from threading import Thread

HOST = '127.0.0.1'
PORT = 5523

clients_list = ['alex', 'pavel']

userConnections = {} # 'username' : connection

def recv_msg(conn):
    from_user = conn.recv(1024)
    to_user = conn.recv(1024)
    print(to_user.decode())
    msg = conn.recv(1024)
    to_conn = userConnections[to_user.decode()]
    print(f'{from_user.decode()}:{to_user.decode()}:{msg.decode()}')
    return from_user, to_user, msg, to_conn

def send_msg(to_user, msg, to_conn):
    to_conn.sendall(msg)
    print(f'message sent to {to_user.decode()}')


def message_handler(conn):
    global clients_list
    with conn:
        while True:
            username = conn.recv(1024)
            userConnections[username.decode()] = conn
            if username.decode() in clients_list:
                print(f'[+] {username.decode()} connected')
                conn.sendall(b'done')
                break
            else:
                conn.sendall(b'user not found')
                continue

        while True:
            to = conn.recv(1024)
            if to.decode() in clients_list:
                conn.sendall(b'done')
                break
            else:
                conn.sendall(b'user not found')
                continue

        while True:
            is_send = s.recv(1024)
            if is_send.decode() == 'send':
                from_user, to_user, msg, to_conn = recv_msg(conn)
            elif is_send == 'recv':
                send_msg(to_user, msg, to_conn)
        

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        print('Listening...')
        conn, addr = s.accept()
        Thread(target=message_handler, args=(conn,)).start()

print('[+] server closed')