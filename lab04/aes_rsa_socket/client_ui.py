from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext


class AESRSAClientUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AES + RSA Socket Client")
        self.root.geometry("640x460")

        self.client_socket = None
        self.aes_key = None
        self.running = False

        tk.Label(root, text="Host").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.host_entry = tk.Entry(root)
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")

        tk.Label(root, text="Port").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.port_entry = tk.Entry(root, width=8)
        self.port_entry.insert(0, "12345")
        self.port_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_server)
        self.connect_button.grid(row=0, column=4, padx=8, pady=8)

        self.log_box = scrolledtext.ScrolledText(root, height=20)
        self.log_box.grid(row=1, column=0, columnspan=5, padx=8, pady=8, sticky="nsew")

        self.message_entry = tk.Entry(root)
        self.message_entry.grid(row=2, column=0, columnspan=4, padx=8, pady=8, sticky="ew")
        self.message_entry.bind("<Return>", lambda event: self.send_message())

        self.send_button = tk.Button(root, text="Send", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=2, column=4, padx=8, pady=8)

        root.columnconfigure(1, weight=1)
        root.columnconfigure(3, weight=1)
        root.rowconfigure(1, weight=1)
        root.protocol("WM_DELETE_WINDOW", self.close)

    def log(self, message):
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def encrypt_message(self, key, message):
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
        return cipher.iv + ciphertext

    def decrypt_message(self, key, encrypted_message):
        iv = encrypted_message[:AES.block_size]
        ciphertext = encrypted_message[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(ciphertext), AES.block_size).decode()

    def connect_server(self):
        try:
            host = self.host_entry.get().strip()
            port = int(self.port_entry.get().strip())
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((host, port))

            client_key = RSA.generate(2048)
            RSA.import_key(self.client_socket.recv(2048))
            self.client_socket.send(client_key.publickey().export_key(format="PEM"))

            encrypted_aes_key = self.client_socket.recv(2048)
            cipher_rsa = PKCS1_OAEP.new(client_key)
            self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)

            self.running = True
            self.connect_button.config(state=tk.DISABLED)
            self.send_button.config(state=tk.NORMAL)
            self.log("Connected and AES key received.")
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as exc:
            messagebox.showerror("Connection error", str(exc))

    def receive_messages(self):
        while self.running:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                message = self.decrypt_message(self.aes_key, encrypted_message)
                self.root.after(0, self.log, "Server: " + message)
            except Exception:
                break
        self.root.after(0, self.log, "Disconnected.")

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        try:
            encrypted_message = self.encrypt_message(self.aes_key, message)
            self.client_socket.send(encrypted_message)
            self.log("You: " + message)
            self.message_entry.delete(0, tk.END)
            if message == "exit":
                self.close()
        except Exception as exc:
            messagebox.showerror("Send error", str(exc))

    def close(self):
        self.running = False
        try:
            if self.client_socket:
                self.client_socket.close()
        except OSError:
            pass
        self.root.destroy()


if __name__ == "__main__":
    app = tk.Tk()
    AESRSAClientUI(app)
    app.mainloop()
