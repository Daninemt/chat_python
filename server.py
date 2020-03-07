from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, timeout, error
import logging
from concurrent.futures import ThreadPoolExecutor


class ChatServer:
    def __init__(self, host, port):
        self.logger = self._setup_logger()
        self.sock = self._setup_socket(host, port)
        self.connections = []

    def run(self):
        self.logger.info("Chat server is running")
        with ThreadPoolExecutor() as executor:
            while True:
                try:
                    conn, addr = self.sock.accept()
                    conn.settimeout(60)
                    self.logger.debug(f"New connection: {addr}")
                    self.connections.append(conn)
                    self.logger.debug(f"Connections: {self.connections}")
                    executor.submit(self.relay_messages, conn)
                except error as msg:
                    self.logger.warning(f"Error occurred while trying to connect to the client: {msg}")

    def relay_messages(self, conn):
        while True:
            try:
                data = conn.recv(4096)
                for connection in self.connections:
                    connection.send(data)
                if not data:
                    self.logger.warning("No data. Exiting.")
                    break
            except timeout:
                self.logger.warning(f"The following connection got timeout {conn}")
                conn.send("bye".encode('utf-8'))
                self.connections.remove(conn)
                conn.close()

    def _setup_socket(self, host, port):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen()
            return sock
        except error as msg:
            self.logger.warning(f"Error occurred while trying to create socket: {msg}")

    @staticmethod
    def _setup_logger():
        logger = logging.getLogger('chat_server')
        logger.addHandler(logging.StreamHandler())
        logger.setLevel(logging.DEBUG)
        return logger


if __name__ == "__main__":
    SERVER_HOST = "localhost"
    SERVER_PORT = 4333
    server = ChatServer(SERVER_HOST, SERVER_PORT)
    server.run()
