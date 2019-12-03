import socket


class TCPServer:
    BUFFER_SIZE = 1024

    def __init__(self, host='', port=7070):
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.running = True
        self.data = None

    def run_server(self):
        print(f"Starting TCP server on port {self.port}")
        self.sock.bind((self.host, self.port))
        sock.listen(10)
        conn, addr = self.sock.accept()
        print('connected:', addr)

        self.listen_socket(conn, addr)

    def listen_socket(self, conn, addr):
        while self.running:
            self.data = conn.recv(BUFFER_SIZE)
            print(data)
        self.conn.close()
        print("Server stopped")


if __name__ == '__main__':
    TCPServer().run_server()
