from tkinter import *
from tkinter import ttk

from Message import Message

from typing import List


class UserInterface:
    connectToChatWindow: Tk = None
    mainWindow: Tk = None

    main = None # Ссылка на главный класс приложения

    listbox_connections: Listbox = None
    entry_message: Entry = None

    # Холст (выделенная область на которой можно свободно размещать разные графические элементы)
    # на который будут выводится сообщения чата
    canvas_for_show_messages: Canvas = None

    def __init__(self, main):
        self.main = main

    def delete_name_from_listbox(self, name):
        """Метод удаления с GUI имени участника чата"""
        index = self.listbox_connections.get(0, END).index(name)  # Получаем идекс элемента из listbox
        self.listbox_connections.delete(index) # Удаляем элемент по индексу

    def start_window_create_or_connect_to_chat(self, x: int = 0, y: int = 0, height: int = 280, width: int = 320):
        """Метод для построения и конфигурации стартового окна чата"""
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
        connect = Button(self.connectToChatWindow, text="Подключиться", command=lambda: self.main.create_client_and_start_chat(
            input_your_host.get(),
            int(input_your_port.get()),
            input_name.get(),
            input_server_host.get(),
            int(input_server_port.get())
        ))
        separator = ttk.Separator(self.connectToChatWindow) # Вертикальная черта для красоты
        create = Button(self.connectToChatWindow, text="Создать чат", command=lambda: self.main.create_server(
            input_your_host.get(),
            int(input_your_port.get()),
            input_name.get(),
            input_server_host.get(),
            int(input_server_port.get())
        ))

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
            Label(self.canvas_for_show_messages, text=message_attributes['text']).pack(anchor='w', padx=5, pady=5)
        else:
            Label(self.canvas_for_show_messages, text=message_attributes['text']).pack(anchor='e', padx=5, pady=5)

    def print_all_messages(self, messages: List[Message]):
        """
        Метод вывода всех сообщений чата при переключении между чатами.

        Удаляет все старые сообщения прошлого чата с messages_canvas: Canvas и затем
        добавляет сообщения выбранного на данный момент чата через метод print_message.

        :param messages: список сообщений в виде списка объектов класса Message
        """
        for widget in self.canvas_for_show_messages.winfo_children():
            widget.destroy()
        for message in messages:
            self.print_message(message)

    def on_select_listbox(self, event):
        """Метод для обработки события переключения между клиентами чата (ListBox)"""
        select_chat_name = self.listbox_connections.get(self.listbox_connections.curselection()[0]) # Получаем выбранное из списка имя пользователя
        self.main.set_selected_chat(select_chat_name) # Устанавливаем выбранный чат
        messages = self.main.get_chat_history(select_chat_name) # Получаем все сообщения чата с этим пользователем
        self.print_all_messages(messages) # Вывод на поле всех сообщений этого пользователя

    def send_message(self, event=None):
        """Метод для отправки сообщения. Срабатывает при нажатии на кнопку 'Отправить' или на клавишу 'Enter' """
        self.main.send(self.listbox_connections.get(self.listbox_connections.curselection()), self.entry_message.get())
        self.entry_message.delete(0, END)

    def start_main_window(self, name, host, port):
        """Метод для построения и конфигурации основного окна чата"""
        x = 400
        y = 600
        self.mainWindow = Tk()
        # Добавлям реакцию на закрытие приложения
        self.mainWindow.protocol("WM_DELETE_WINDOW", self.main.exit)
        self.mainWindow.geometry(f"{x}x{y}")
        self.mainWindow.title(f"ваш ник: {name}. Ваш адрес: {host}:{port}")

        self.listbox_connections = Listbox(self.mainWindow)
        for i in self.main.client.connections.keys():
            self.listbox_connections.insert(0, i)
        # Связавание события выбора элемента Listbox'а с методом on_select_listbox
        # Переключение между чатами
        self.listbox_connections.bind('<<ListboxSelect>>', self.on_select_listbox)

        self.canvas_for_show_messages = Canvas(self.mainWindow, borderwidth=1, relief=SOLID, scrollregion=(-10000, -10000, 10000, 10000))

        scrollbar = Scrollbar(self.mainWindow, orient='vertical', command=self.canvas_for_show_messages.yview)
        self.canvas_for_show_messages['yscrollcommand'] = scrollbar.set

        self.entry_message = Entry(self.mainWindow)
        self.entry_message.bind('<Return>', self.send_message)

        button_send_message = Button(self.mainWindow, text="отправить", command=lambda: self.send_message())

        # Размеры виджетов
        list_box_connections_WIDTH = 75 # Ширина списка подключений
        messages_canvas_height = y - button_send_message.winfo_reqheight() # Высота Canvas для вывода сообщений
        messages_canvas_width = 315  # Ширина 
        entry_message_WIDTH = 225 # Ширина поля ввода сообщения

        '''Размещение виджетов в окне'''
        self.listbox_connections.place(x=0, y=0, width=list_box_connections_WIDTH, height=600)
        self.canvas_for_show_messages.place(x=list_box_connections_WIDTH, y=0, width=messages_canvas_width, height=messages_canvas_height)
        # scroll_bar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar.place(x=list_box_connections_WIDTH+messages_canvas_width, y=0, width=20, height=messages_canvas_height)
        self.entry_message.place(x=list_box_connections_WIDTH, y=messages_canvas_height, width=entry_message_WIDTH)
        button_send_message.place(x=entry_message_WIDTH+list_box_connections_WIDTH, y=messages_canvas_height, width=100)

        self.mainWindow.mainloop()

