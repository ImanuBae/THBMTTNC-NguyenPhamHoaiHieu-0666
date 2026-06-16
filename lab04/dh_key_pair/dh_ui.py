from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization
import tkinter as tk
from tkinter import scrolledtext


class DHKeyPairUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Diffie-Hellman Key Pair")
        self.root.geometry("760x560")

        tk.Button(root, text="Generate DH Shared Secret", command=self.generate).pack(padx=10, pady=10)

        self.output = scrolledtext.ScrolledText(root, height=28)
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def write(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)

    def public_key_to_pem(self, public_key):
        return public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode()

    def generate(self):
        self.output.delete("1.0", tk.END)
        parameters = dh.generate_parameters(generator=2, key_size=2048)

        server_private_key = parameters.generate_private_key()
        server_public_key = server_private_key.public_key()

        client_private_key = parameters.generate_private_key()
        client_public_key = client_private_key.public_key()

        server_shared_key = server_private_key.exchange(client_public_key)
        client_shared_key = client_private_key.exchange(server_public_key)

        self.write("Server Public Key:")
        self.write(self.public_key_to_pem(server_public_key))
        self.write("Client Public Key:")
        self.write(self.public_key_to_pem(client_public_key))
        self.write("Server Shared Secret:")
        self.write(server_shared_key.hex())
        self.write("Client Shared Secret:")
        self.write(client_shared_key.hex())
        self.write("Match: " + str(server_shared_key == client_shared_key))


if __name__ == "__main__":
    app = tk.Tk()
    DHKeyPairUI(app)
    app.mainloop()
