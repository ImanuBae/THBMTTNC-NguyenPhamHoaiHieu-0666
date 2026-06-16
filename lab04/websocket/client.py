import threading
import tornado.ioloop
import tornado.websocket


class WebSocketClient:
    def __init__(self, io_loop):
        self.connection = None
        self.io_loop = io_loop

    def start(self):
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            callback=self.on_connected,
            on_message_callback=self.on_message,
            ping_interval=10,
            ping_timeout=30,
        )

    def on_connected(self, future):
        try:
            self.connection = future.result()
            print("Connected to server.")
            print("Type a message and press Enter. Type 'exit' to quit.")
            threading.Thread(target=self.read_input, daemon=True).start()
        except Exception as exc:
            print("Could not connect:", exc)
            self.io_loop.stop()

    def read_input(self):
        while True:
            message = input("Message: ")
            if message.lower() == "exit":
                self.io_loop.add_callback(self.stop)
                break
            self.io_loop.add_callback(self.connection.write_message, message)

    def on_message(self, message):
        if message is None:
            print("Disconnected from server.")
            self.stop()
            return
        print("Encrypted response from server:")
        print(message)

    def stop(self):
        if self.connection:
            self.connection.close()
        self.io_loop.stop()


def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()


if __name__ == "__main__":
    main()
