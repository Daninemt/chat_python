from socket import socket, AF_INET, SOCK_STREAM, error
import logging
from threading import Thread
import datetime


class ChatClient:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.sock = self._setup_socket(host, port)
        self.name = ""
        self.register()
        thread = Thread(target=self.send_message)
        thread.daemon = True
        thread.start()

        while True:
            try:
                data = self.sock.recv(4096)
                if not data:
                    break
                self.logger.info(data.decode())
            except error as msg:
                self.logger.warning(f"Error occurred while trying to receive data through socket: {msg}")

    def register(self):
        try:
            self.name = input("Enter your name:\t")
            client_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            client_time += " | "
            register_message = client_time + self.name + " has just entered the chat"
            self.sock.send(register_message.encode('utf-8', 'backslashreplace'))
        except error as msg:
            self.logger.warning(f"Error occurred while trying to send data through socket: {msg}")

    def send_message(self):
        while True:
            try:
                user_message = input()
                if len(user_message) > 0:
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    now += " | "
                    name = self.name + " | "
                    message = now + name + user_message
                self.sock.send(message.encode('utf-8', 'backslashreplace'))
            except error as msg:
                self.logger.warning(f"Error occurred while trying to send data through socket: {msg}")

    def _setup_socket(self, host, port):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((host, port))
            return sock
        except error as msg:
            self.logger.warning(f"Couldn't create socket: {msg}")

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('chat_client')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger


if __name__ == "__main__":
    SERVER_HOST = input("Enter host's ip: ")
    SERVER_PORT = 4333
    client = ChatClient(SERVER_HOST, SERVER_PORT)
