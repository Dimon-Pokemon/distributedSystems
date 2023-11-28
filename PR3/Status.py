from enum import Enum


class Status(Enum):
    CONNECTIONS = 'connections'
    MESSAGE = 'message'
    JOIN = 'join'
    NEW_CLIENT_INFO = 'new_client_info'
    ERROR_DUPLICATE_NAME = 'ERROR_DUPLICATE_NAME'
    EXIT = 'exit'

