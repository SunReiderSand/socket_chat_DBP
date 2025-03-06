import socket
import threading

HOST = "127.0.0.1"
PORT = 12345
clients = []  # Список подключенных клиентов

# Функция для обработки каждого клиента
def handle_client(connection: socket.socket, address: tuple) -> None:
    with connection:
        clients.append(connection)  # Добавляем нового клиента в список
        print(f"New connection: {address}")

        while True:
            try:
                data = connection.recv(1024)
                if not data:
                    break
                # Логируем сообщение и адрес клиента
                print(f"Received from {address}: {data.decode()}")
                # Отправляем всем остальным клиентам, кроме отправителя
                for client in clients:
                    if client != connection:
                        client.sendall(data)
            except ConnectionResetError:
                break

        clients.remove(connection)  # Удаляем клиента из списка
        print(f"Connection closed: {address}")

# Основной сервер
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server started, waiting for connections...")

        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
