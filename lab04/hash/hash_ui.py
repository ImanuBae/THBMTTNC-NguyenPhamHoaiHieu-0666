import hashlib
import tkinter as tk
from tkinter import ttk, messagebox


class HashUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hash Algorithms")
        self.root.geometry("680x360")

        tk.Label(root, text="Input").pack(anchor="w", padx=10, pady=(10, 4))
        self.input_text = tk.Text(root, height=6)
        self.input_text.pack(fill=tk.X, padx=10)

        options = ["MD5", "SHA-256", "SHA-3-256", "BLAKE2b"]
        self.algorithm = tk.StringVar(value=options[0])
        ttk.Combobox(root, textvariable=self.algorithm, values=options, state="readonly").pack(
            fill=tk.X, padx=10, pady=10
        )

        tk.Button(root, text="Calculate Hash", command=self.calculate_hash).pack(padx=10, pady=4)

        tk.Label(root, text="Hash Result").pack(anchor="w", padx=10, pady=(10, 4))
        self.result_entry = tk.Entry(root)
        self.result_entry.pack(fill=tk.X, padx=10)

    def calculate_hash(self):
        data = self.input_text.get("1.0", tk.END).rstrip("\n").encode("utf-8")
        if not data:
            messagebox.showwarning("Warning", "Please enter data to hash.")
            return

        algorithm = self.algorithm.get()
        if algorithm == "MD5":
            result = hashlib.md5(data).hexdigest()
        elif algorithm == "SHA-256":
            result = hashlib.sha256(data).hexdigest()
        elif algorithm == "SHA-3-256":
            result = hashlib.sha3_256(data).hexdigest()
        else:
            result = hashlib.blake2b(data, digest_size=64).hexdigest()

        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, result)


if __name__ == "__main__":
    app = tk.Tk()
    HashUI(app)
    app.mainloop()
