from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from Message import Message

from typing import List


class UserInterface:
    connectToChatWindow: Tk = None
    createChateWindow: Tk = None
    mainWindow: Tk = None
    client = None

    main = None

    list_box_connections: Listbox = None

    # Холст (выделенная область на которой можно свободно размещать разные графические элементы)
    # на который будут выводится сообщения чата
    messages_canvas: Canvas = None

    def __init__(self, main):
        self.main = main

    # def show_error(self, title, message):
    #     messagebox.showerror(title, message)

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
        connect = Button(self.connectToChatWindow, text="Подключиться", command=lambda: self.main.сделать_так_чтобы_все_было_хорошо(
            input_your_host.get(),
            int(input_your_port.get()),
            input_name.get(),
            input_server_host.get(),
            int(input_server_port.get())
        ))
        #, self.connectToChatWindow.destroy(), self.start_main_window())
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

    def print_message(self, message: Message):
        """
        Метод выводит одно сообщение в область чата (messages_canvas: Canvas)
        """
        message_attributes = message.__dict__
        if message_attributes['position'] == 'left':
            Label(self.messages_canvas, text=message_attributes['text']).pack(anchor='w', padx=5, pady=5)
        else:
            Label(self.messages_canvas, text=message_attributes['text']).pack(anchor='e', padx=5, pady=5)

    def print_all_messages(self, messages: List[Message]):
        """
        Метод вывода всех сообщений чата при переключении между чатами.

        Удаляет все старые сообщения прошлого чата с messages_canvas: Canvas и затем
        добавляет сообщения выбранного на данный момент чата через метод print_message.

        :param messages: список сообщений в виде списка объектов класса Message
        """
        self.messages_canvas.delete('all')
        for message in messages:
            self.print_message(message)

    def on_select_listbox(self, event):
        select_chat_name = self.list_box_connections.get(self.list_box_connections.curselection()[0]) # Получаем выбранное из списка имя пользователя
        self.main.set_selected_chat(select_chat_name)
        messages = self.main.get_chat_history(select_chat_name) # Получаем все сообщения чата с этим пользователем
        self.print_all_messages(messages) # Вывод на поле всех сообщений этого пользователя

    def start_main_window(self, name, host, port):
        x = 400
        y = 600
        self.mainWindow = Tk()
        self.mainWindow.geometry(f"{x}x{y}")
        self.mainWindow.title(f"ваш ник: {name}. Ваш адрес: {host}:{port}")

        self.list_box_connections = Listbox(self.mainWindow)
        for i in self.main.client.connections.keys():
            self.list_box_connections.insert(0, i)

        self.messages_canvas = Canvas(self.mainWindow, borderwidth=1, relief=SOLID, scrollregion=(-10000, -10000, 10000, 10000))
        # for message_obj in [msg1, msg2, msg3, msg4, msg5]:
        #     message_attributes = message_obj.__dict__
        #     if message_attributes['place'] == 'left':
        #         Label(self.messages_canvas, text=message_attributes['text']).pack(anchor='w', padx=5, pady=5)
        #     else:
        #         Label(self.messages_canvas, text=message_attributes['text']).pack(anchor='e', padx=5, pady=5)

        scroll_bar = Scrollbar(self.mainWindow, orient='vertical', command=self.messages_canvas.yview)
        self.messages_canvas['yscrollcommand'] = scroll_bar.set

        entry_message = Entry(self.mainWindow)

        button_send_message = Button(self.mainWindow, text="отправить", command=lambda: self.main.send(self.list_box_connections.get(self.list_box_connections.curselection()), entry_message.get()))

        # Размеры виджетов
        list_box_connections_WIDTH = 75 # Ширина списка подключений
        messages_canvas_height = y - button_send_message.winfo_reqheight() # Высота Canvas для вывода сообщений
        messages_canvas_width = 315  # Ширина 
        entry_message_WIDTH = 225 # Ширина поля ввода сообщения

        self.list_box_connections.place(x=0, y=0, width=list_box_connections_WIDTH, height=600)
        self.messages_canvas.place(x=list_box_connections_WIDTH, y=0, width=messages_canvas_width, height=messages_canvas_height)
        # scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scroll_bar.place(x=list_box_connections_WIDTH+messages_canvas_width, y=0, width=20, height=messages_canvas_height)
        entry_message.place(x=list_box_connections_WIDTH, y=messages_canvas_height, width=entry_message_WIDTH)
        button_send_message.place(x=entry_message_WIDTH+list_box_connections_WIDTH, y=messages_canvas_height, width=100)

        self.list_box_connections.bind('<<ListboxSelect>>', self.on_select_listbox)

        self.mainWindow.mainloop()

        def create_test_messages():
            msg1 = Message.Message(
                status='message',
                text='Hello',
                position='left'
            )
            msg2 = Message.Message(
                status='message',
                text='Hello',
                position='right'
            )
            msg3 = Message.Message(
                status='message',
                text='How are you?',
                position='right'
            )
            msg4 = Message.Message(
                status='message',
                text='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nI am fine, thanks. Are you?',
                position='left'
            )
            msg5 = Message.Message(
                status='message',
                text='\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nfsfsfsdfsfsdfsdfsdfsfsdfdsfsdfsd?',
                position='left'
            )
            return [msg1, msg2, msg3, msg4, msg5]


