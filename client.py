import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

# Функция для получения сообщений от сервера
def receive_messages(s: socket.socket):
    while True:
        try:
            data = s.recv(1024)
            if data:
                print(f"\nReceived: {data.decode()}")
        except ConnectionResetError:
            print("Connection lost.")
            break

# Функция для отправки сообщений на сервер
def send_messages(s: socket.socket, name: str):
    while True:
        message = input(f"{name}: ")
        if message == "/exit":
            print("Exiting chat.")
            s.close()
            break
        s.sendall(f"{name}: {message}".encode())

def start_client():
    name = input("Enter your name: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Запуск потока для приема сообщений
        threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

        # Запуск потока для отправки сообщений
        send_messages(s, name)

if __name__ == "__main__":
    start_client()
