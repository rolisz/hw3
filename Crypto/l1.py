#!/usr/bin/env python
import Tkinter as tk
import string

def modular_inverse(x, n=27):
    for i in range(n):
        if x*i % n == 1:
            return i

def invert_2_2_matrix(m, n=27):
    a = m[0]
    b = m[1]
    c = m[2]
    d = m[3]

    inv = modular_inverse(a*d-b*c,n)
    print(inv)
    return [inv*d%n, (-inv*b)%n, (-inv*c)%n, inv*a%n]


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
        self.createWidgets()

    def createWidgets(self):
        top=self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        w = tk.Entry(self)
        tk.Label(self, text="Alphabet").grid()
        self.alphabet_var = tk.StringVar()
        self.alphabet_var.set(" "+string.ascii_lowercase)
        self.alphabet = tk.Entry(self, textvariable=self.alphabet_var)
        self.alphabet.grid(sticky=tk.E+tk.W)
        tk.Label(self, text="Encryption key").grid()
        self.key_var = tk.StringVar()
        self.key_var.set("11 8 3 7")
        self.key = tk.Entry(self, textvariable=self.key_var)
        self.key.grid(sticky=tk.E+tk.W)
        tk.Label(self, text="Plain Text").grid()
        self.plaintext_var = tk.StringVar()
        self.plaintext = tk.Entry(self, textvariable=self.plaintext_var)
        self.plaintext.grid(sticky=tk.E+tk.W)
        tk.Label(self, text="Cypher text").grid()
        self.cyphertext_var = tk.StringVar()
        self.cyphertext = tk.Entry(self, textvariable=self.cyphertext_var)
        self.cyphertext.grid(sticky=tk.E+tk.W)
        self.encrypt = tk.Button(self, text='Encrypt',
            command=self.encrypt_func)
        self.encrypt.grid()

        self.decrypt = tk.Button(self, text='Decrypt',
            command=self.decrypt_func)
        self.decrypt.grid()

    def encrypt_func(self):
        alphabet = self.alphabet_var.get()
        n = len(alphabet)
        numeric = [alphabet.index(x) for x in self.plaintext_var.get()]
        print(numeric)
        if len(numeric) % 2 != 0:
            numeric.append(alphabet.index(" "))
        it = iter(numeric)

        key = map(int,self.key_var.get().split())
        encryption = []
        for l1, l2 in zip(it, it):
            encryption.append((l1*key[0] + l2*key[2]) % n)
            encryption.append((l1*key[1] + l2*key[3]) % n)

        self.cyphertext_var.set("".join(alphabet[i] for i in encryption))

    def decrypt_func(self):
        alphabet = self.alphabet_var.get()
        n = len(alphabet)
        numeric = [alphabet.index(x) for x in self.cyphertext_var.get()]
        it = iter(numeric)

        key = invert_2_2_matrix(map(int,self.key_var.get().split()))
        print(key)
        decryption = []
        for l1, l2 in zip(it, it):
            decryption.append((l1*key[0] + l2*key[2]) % n)
            decryption.append((l1*key[1] + l2*key[3]) % n)

        self.plaintext_var.set("".join(alphabet[i] for i in decryption))


app = Application()
app.master.title('Sample application')
app.mainloop()