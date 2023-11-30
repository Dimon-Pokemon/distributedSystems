from Message import Message
from Status import Status

class Node:
    socket = None
    connections: dict = {}

    def convert_tuple_address_to_string(self, addr: tuple) -> str:
        """
        Преобразует адрес в виде кортежа в адрес в виде строки вида "IP:PORT",

        Подробности:
            Для отправки сообщений socket.sendto требуется указать адрес в виде кортежа
            ('127.0.0.1', 2551), где порт представлен в виде числа, а хост в виде строки.
            А список подключений представлен в виде словаря dict и имеет вид
            connections = {"127.0.0.1:2551": "name", "127.0.0.1:2552": "name2"} -
            это нужно для нормального преобразования в объект JSON, потому что если ключом будет КОРТЕЖ, то
            преобразования будет некорректым.

        """
        return ":".join((addr[0], str(addr[1])))

    def send_connections_to_new_client(self, address: tuple, connections: dict):
        message = Message(
            status=Status.CONNECTIONS.value,
            connections=connections
        )
        self.socket.sendto(message.to_json().encode("utf-8"), address)

    def send_info_about_new_client(self, address_new_client: tuple, name_new_client: str):
        message = Message(
            status=Status.NEW_CLIENT_INFO.value,
            address=self.convert_tuple_address_to_string(address_new_client),
            name=name_new_client
        )
        byte_json_message = message.to_json().encode("utf-8")
        for address_client in self.connections.values():
            # В словаре соединений адреса хронятся в виде строк '127.0.0.1:2551'
            # а для отправки на сокет данных нужен адрес в виде кортежа ('127.0.0.1', 2551)
            tuple_address_client = address_client.split(":") # Получаем список вида ['127.0.0.1', '2551']
            tuple_address_client = (tuple_address_client[0], int(tuple_address_client[1])) # Получаем кортеж вида ('127.0.0.1', 2551)
            self.socket.sendto(byte_json_message, tuple_address_client)
