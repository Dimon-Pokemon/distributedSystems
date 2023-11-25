import tkinter
from tkinter import *
from tkinter import ttk
from Client import Client


class UserInterface:
    connectToChatWindow: Tk = None
    createChateWindow: Tk = None
    mainWindow: Tk = None
    client = None

    main = None

    def __init__(self, main):
        self.main = main

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
        connect = Button(self.connectToChatWindow, text="Подключиться", command=lambda: (self.main.create_client_and_connect_to_chat(
            input_your_host.get(),
            int(input_your_port.get()),
            input_name.get(),
            input_server_host.get(),
            int(input_server_port.get())
        ), self.connectToChatWindow.destroy(), self.start_main_window()))
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

    def start_main_window(self):
        x = 400
        y = 600
        self.mainWindow = Tk()
        self.mainWindow.geometry(f"{x}x{y}")

        list_box_connections = Listbox(self.mainWindow)
        for i in self.main.client.connections.values():
            list_box_connections.insert(0, i)

        messages_frame = ttk.Frame(self.mainWindow, borderwidth=1, relief=SOLID, padding=[8, 10])
        scroll_bar = tkinter.Scrollbar(messages_frame)

        entry_message = Entry(self.mainWindow)

        button_send_message = Button(self.mainWindow, text="Отправить")

        list_box_connections_WIDTH = 75
        messages_frame_height = y - button_send_message.winfo_reqheight()
        entry_message_WIDTH = 225

        list_box_connections.place(x=0, y=0, width=list_box_connections_WIDTH, height=600)
        messages_frame.place(x=list_box_connections_WIDTH, y=0, width=325, height=messages_frame_height)
        scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        entry_message.place(x=list_box_connections_WIDTH, y=messages_frame_height, width=entry_message_WIDTH)
        button_send_message.place(x=entry_message_WIDTH+list_box_connections_WIDTH, y=messages_frame_height, width=100)

        self.mainWindow.mainloop()




