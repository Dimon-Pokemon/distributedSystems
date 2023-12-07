import argparse
import json
import socket
import sys
import threading

from Status import Status
from Message import Message

from Node import Node

from time import time, sleep


# Класс сервера Server наследуется от Node
class Server(Node):
    # socket = None
    # connections: dict = {}
    run: bool = False
    start_waiting: "time" = None # Переменная, определяющая точку начала отсчета до отключения сервера
    timeout: int = None

    def __init__(self, host, port, timeout=30):
        self.timeout = timeout # Установка времени ожидания новых подключений

        # Создание сокета сервера
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((host, port))

        self.run = True

    def receive(self):
        """Метод обработки сообщений от клиентов"""
        while self.run:
            data, addr = self.socket.recvfrom(1024)
            data = dict(json.loads(data.decode("utf-8")))
            # print(data)
            if data['status'] == Status.JOIN.value:
                if data["name"] in self.connections:
                    pass
                else:
                    self.send_connections_to_new_client(addr, self.connections)
                    print("Hello,", addr)
                    self.send_info_about_new_client(addr, data['name'])
                    self.connections[data['name']] = self.convert_tuple_address_to_string(addr)
            elif data['status'] == Status.EXIT.value:
                # Убираем отключенного клиента из списка подключений
                self.connections.pop(data['name'])

    def run_server(self):
        # Поток демон автоматически завершается, когда основной поток завершается
        thread = threading.Thread(target=self.receive, daemon=True)
        thread.start()
        '''
        Реализация автоматического отключения сервера, если нет новых подключений в течении некоторого промежутка 
        времени, в секундах записанного в поле self.timeout
        '''
        while self.run:
            # Проверка наличия подключений
            if len(self.connections) == 0: # В чате никого нет
                if self.start_waiting is None: # Проверка, был ли начат отсчет времени до отключения
                    self.start_waiting = time() # Время начала ожидания подключения
                    print("Time:", self.start_waiting)
                else:
                    if time() - self.start_waiting > self.timeout:
                        self.run = False # Меняем флаг. В целом, ненужно, так как вызывем sys.exit(0)
                        sys.exit(0) # Завершение работы сервера
                    print("Diff:", time() - self.start_waiting)  # Вывод информация о прошедшем времени ожидания
            else:
                self.start_waiting = None
            sleep(3)

# Запуск сервера
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", dest="host", default="127.0.0.1")
    parser.add_argument("--port", dest="port", default=2550, type=int)
    args = parser.parse_args()

    server = Server(args.host, args.port)
    server.run_server()

