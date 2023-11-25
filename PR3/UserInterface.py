from tkinter import *
from tkinter import ttk
from Main import Main
from Client import Client


class UserInterface:
    connectToChatWindow: Tk = None
    createChateWindow: Tk = None
    mainWindow: Tk = None
    client = None

    main: Main = None

    def __init__(self, main: Main):
        self.main = main

    def get_client(self):
        return self.client

    def start_window_create_or_connect_to_chat(self, x: int = 0, y: int = 0, height: int = 280, width: int = 320):

        self.connectToChatWindow = Tk()
        self.connectToChatWindow.title("Подсоединиться к чату")
        self.connectToChatWindow.geometry(f"{height}x{width}+{x}+{y}")

        label_your_host = Label(self.connectToChatWindow, text="Введите ваш адрес:")
        label_your_port = Label(self.connectToChatWindow, text="Введите ваш порт:")
        label_your_name = Label(self.connectToChatWindow, text="Введите ваше имя:")
        label_server_host = Label(self.connectToChatWindow, text="Введите адрес сервера:")
        label_server_port = Label(self.connectToChatWindow, text="Введите порт сервера:")
        input_your_host = Entry(self.connectToChatWindow)
        input_your_port = Entry(self.connectToChatWindow)
        input_name = Entry(self.connectToChatWindow)
        input_server_host = Entry(self.connectToChatWindow)
        input_server_port = Entry(self.connectToChatWindow)
        connect = Button(self.connectToChatWindow, text="Подключиться", command=lambda: self.main.create_client_and_connect_to_chat(
            input_your_host,
            input_your_port,
            input_name,
            input_server_host,
            input_server_port
        ))
        separator = ttk.Separator(self.connectToChatWindow)
        create = Button(self.connectToChatWindow, text="Создать чат")

        # label1.pack()
        label_your_host.pack()
        input_your_host.pack()
        label_your_port.pack()
        input_your_port.pack()
        label_your_name.pack()
        input_name.pack()
        label_server_host.pack()
        input_server_host.pack()
        label_server_port.pack()
        input_server_port.pack()
        connect.pack()
        separator.pack(fill=X, padx=10, expand=True)
        create.pack()

        self.connectToChatWindow.mainloop()


