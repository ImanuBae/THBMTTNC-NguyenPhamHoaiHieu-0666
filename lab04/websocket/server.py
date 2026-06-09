from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import tornado.ioloop
import tornado.web
import tornado.websocket


AES_KEY = get_random_bytes(16)


def encrypt_message(message):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return {
        "iv": cipher.iv.hex(),
        "ciphertext": ciphertext.hex(),
    }


class AESWebSocketServer(tornado.websocket.WebSocketHandler):
    def open(self):
        print("Client connected.")

    def on_message(self, message):
        encrypted = encrypt_message(message)
        response = f"IV: {encrypted['iv']}\nCiphertext: {encrypted['ciphertext']}"
        print(f"Received: {message}")
        print(f"Encrypted: {encrypted['ciphertext']}")
        self.write_message(response)

    def on_close(self):
        print("Client disconnected.")


def main():
    app = tornado.web.Application(
        [(r"/websocket/", AESWebSocketServer)],
        websocket_ping_interval=10,
        websocket_ping_timeout=30,
    )
    app.listen(8888)
    print("WebSocket AES server is running at ws://localhost:8888/websocket/")
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
