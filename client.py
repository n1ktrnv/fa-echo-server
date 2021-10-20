import socket
from pathlib import Path

from utils import ask_port


DEFAULT_HOST = 'localhost'
EXIT = 'exit'


def _main():
    host = input('Введите имя хоста (или Enter для использования значения по '
                 'умолчанию): ')
    if host == '':
        host = DEFAULT_HOST
    port = ask_port()

    sock = socket.socket()
    sock.connect((host, port))

    while True:
        command = sock.recv(1024).decode()
        if command == '!get_token':
            token = Path('token.txt').read_text()
            if token:
                sock.send(Path('token.txt').read_text().encode())
            else:
                sock.send(str(None).encode())
        elif command == '!save_token':
            Path('token.txt').write_text(sock.recv(1024).decode())
        elif command == '!password':
            sock.send(input('Введите пароль: ').encode())
        elif command == '!username':
            sock.send(input('Введите имя: ').encode())
        elif command == '!success':
            print(sock.recv(1024).decode())
            while True:
                message = input()
                if message == EXIT:
                    break
                sock.send(message.encode())
                data = sock.recv(1024).decode()
                print(data)
            break
        elif command == '!forbidden':
            print('Ошибка: отказано в доступе')
            break

    sock.close()


if __name__ == '__main__':
    _main()