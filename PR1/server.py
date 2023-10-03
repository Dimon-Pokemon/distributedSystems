import socket
import sys
import time
import json


class Message:
    """
    Класс - сообщение. Представляет сообщения,

    которые будут приходить от клиентов.
    """

    def __init__(self, status_code: str = '200', **data):
        # Распаковываем кортеж именованных аргументов в параметры класса.
        # Паттерн Builder.
        for param, value in data.items():
            setattr(self, param, value)
        self.status_code = status_code # Код ответа сообщения.
        # Время получения ответа
        self.current_time = time.strftime(
            "%Y-%m-%d-%H.%M.%S",
            time.localtime()
        )

    def to_json(self):
        """
        Возвращает атрибуты класса и их значения в виде json.
        Использует стандартный модуль python - json.
        :return: json
        """
        return json.dumps(self, default=lambda o : o.__dict__, sort_keys=True, indent=4)


class ServerDataHandler:
    """
    Класс-обработчик с бизнес-логикой сервера.
    Реализует методы обраотки сообщение и их рассылки
    """

    clients = {} # Временное хрнанилище клиентов в виде словаря

    current_connection = None # Текущее подключение

    def _add_connection(self, name: str, addr: str):
        """Добавляет новое соденинение в словарь clients"""
        self.current_connection = addr
        self.clients[name] = addr

    def get_and_register_message(self, data: bytes, addr: str):
        """
                  Сохраняет адрес запроса пользователя,
                  записывается в атрибут data данные из json в виде словаря,
                  добавляет имя пользователя и адрес в словарь чтобы у нас был
                  доступ к адресу по имени пользователя который обратился к серверу

                  :param data - полученные "сырые" данные в виде bytes
                  :param addr - адрес отправителя данных
                  :return Message(status_code='200', **data) - объект сообщения
        """
        data = dict(json.loads(data.decode('utf-8'))) # Декодируем данные
        self._add_connection(name=data.get('sender_name', 'Unknown'), addr=addr) # Добавляем/обновляем список клиентов
        return Message(status_code=200, **data)

    def send_message(self, sock, message_obj: Message):
        """
                   Отправляет сообщение по всем адресам в словаре
                   кроме адреса отправившего запрос (эхо)
                   :param sock - серверный сокет
                   :param message_obj - объект сообщения
        """
        data = message_obj.to_json() # Закодированное в json сообщение
        # Отправляем сообщение всем клиентам, кроме текущего
        for client in self.clients.values():
            if self.current_connection != client:
                sock.sendto(data.encode('utf-8'), client)


if __name__ == "__main__":
    # Создаем объект серверного сокета
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # host и port на котором будет запущен сервер
    host = 'localhost'
    port = 8888
    # Устанавливаем опцию для текущего адреса сокета,
    # чтобы его можно было переиспользовать в последующих перезапусках:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Регистрируем сокет
    s.bind((host, port))
    # Создаем обработчик бизнес-логики
    data_handler = ServerDataHandler()
    # Флаг для остановки работы сервера
    quit_server = False
    print("Server started")

    # Основной цикл работы сервера
    while not quit_server:
        try:
            # Получаем данные из буфера сокета
            recv_data, recv_addr = s.recvfrom(1024)
            # Логируем информацию в консоль
            sys.stdout.write(recv_data.decode('utf-8'))

            # Регистрируем сообщение
            message = data_handler.get_and_register_message(recv_data, recv_addr)
            # Посылаем сообщение в чат (эхо)
            data_handler.send_message(s, message)

        except Exception as ex:
            # Если произошла ошибка, останавливаем работу сервер
            print(f"Server stopped, because {ex}")
            quit_server = True
    # Закрываем серверное соединение.
    s.close()

