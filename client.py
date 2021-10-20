import socket
from pathlib import Path

from utils import ask_port


DEFAULT_HOST = 'localhost'
EXIT = 'exit'


def send(sock, data):
    length = '{:0>3}'.format(len(data))
    sock.send((length + data).encode())
    print(f'Отправлено {int(length)} симв.')


def recv(sock):
    data = sock.recv(1024).decode()
    length = data[:3]
    print(f'Получено {int(length)} симв.')
    return data[3:]


def _main():
    host = input('Введите имя хоста (или Enter для использования значения по '
                 'умолчанию): ')
    if host == '':
        host = DEFAULT_HOST
    port = ask_port()

    sock = socket.socket()
    sock.connect((host, port))

    while True:
        command = recv(sock)
        if command == '!get_token':
            token = Path('token.txt').read_text()
            if token:
                send(sock, Path('token.txt').read_text())
            else:
                send(sock, str(None).encode())
        elif command == '!save_token':
            Path('token.txt').write_text(recv(sock))
        elif command == '!password':
            send(sock, input('Введите пароль: '))
        elif command == '!username':
            send(sock, input('Введите имя: '))
        elif command == '!success':
            print(recv(sock))
            while True:
                message = input()
                if message == EXIT:
                    break
                send(sock, message)
                data = recv(sock)
                print(data)
            break
        elif command == '!forbidden':
            print('Ошибка: отказано в доступе')
            break

    sock.close()


if __name__ == '__main__':
    _main()