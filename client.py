import socket
from time import sleep
from threading import Thread

HOST = '127.0.0.1'
PORT = 5523

clients_list = ['alex', 'pavel']

def send_msg(from_user, to_user, s):
    msg = input()
    s.sendall(b'send')
    s.sendall(from_user.encode())
    print('\nfrom_user data was sent')
    s.sendall(to_user.encode())
    print('to_user data was sent\n')
    sleep(1)
    s.sendall(msg.encode())
    print('msg sent')


def get_msg(from_user, s):
    s.sendall(b'recv')
    msg = s.recv(1024)
    print(f'\n{from_user}: {msg}\n')
    


print(f'\n[+] Conneting to {HOST}:{PORT}\n')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
        while True:
            username = input('Username: ')
            s.sendall(username.encode())
            server_answer = s.recv(1024)
            if server_answer.decode() == 'done':
                print('\n[+] User was found\n')
                break
            elif username == 'exit':
                exit()
            else:
                print('\n[-] Account not found.\n')
                continue
        while True:
            move = input()
            if move == 'send':
                while True:
                    to = input('\nConnect to chat with user: ')
                    s.sendall(to.encode())
                    server_answer = s.recv(1024)
                    if server_answer.decode() == 'done':
                        print('\n[+] Connect done')
                        break
                    elif to == 'exit':
                        exit()
                    else:
                        print('\n[-] Account not found')
                        continue
                break
        
        print(f'\nFrom {username} to {to}.\n')

        while True:
            Thread(target=get_msg, args=(username, s)).start()
            Thread(target=send_msg, args=(username, to, s)).start()

    except KeyboardInterrupt:
        s.close()
        print('\n\nQuitting...\n')
        exit()