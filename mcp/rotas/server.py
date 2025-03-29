import socket
import json
from rotas.const import HOST, PORT


class Server:
    def __init__(self, func: callable):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"MCP server {HOST}:{PORT}")
        self.active = True
        while self.active:
            conn, _ = server.accept()
            data = conn.recv(1024).decode()
            if not data:
                conn.close()
                continue
            try:
                filter = json.loads(data)
                res = func(filter)
            except Exception as e:
                res = [f"Erro: {e}"]
            print(res)
            print('-' * 50)            
            conn.send(
                json.dumps(res).encode()
            )
            conn.close()

    def stop(self):
        self.active = False
