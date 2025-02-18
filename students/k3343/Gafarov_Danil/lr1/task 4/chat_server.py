import socket
import threading

clients = []
usernames = []


def broadcast(message, sender):
    # Отправка сообщения всем клиентам, кроме отправителя
    for client in clients:
        if client is not sender:
            client.send(message)


def handle_client(client_socket, client_address):
    #  Обработка клиентов
    print(f"[{client_address}] подключился.")

    client_socket.send("Укажите имя: ".encode('utf-8'))
    username = client_socket.recv(1024).decode('utf-8')
    clients.append(client_socket)
    usernames.append(username)

    welcome_message = f"{username} теперь в чате!".encode('utf-8')
    broadcast(welcome_message, client_socket)

    try:
        while True:
            message = client_socket.recv(1024)
            if message:
                full_message = f"{username}: {message.decode('utf-8')}".encode('utf-8')
                broadcast(full_message, client_socket)
            else:
                break
    finally:
        index = clients.index(client_socket)
        clients.remove(client_socket)
        usernames.pop(index)
        client_socket.close()
        print(f"[{client_address}] отключился.")
        broadcast(f"{username} покинул чат.".encode('utf-8'), client_socket)


def start_server():
    #  Запуск сервера
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8080))
    server.listen()

    print("Сервер поднят! Ожидание подключения...")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()


if __name__ == "__main__":
    start_server()
