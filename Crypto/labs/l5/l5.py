#!/usr/bin/env python
import tkinter as tk
import string
from tkinter import messagebox as tkMessageBox
from elgamal import *


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
        self.alphabet_var = " "+string.ascii_lowercase

        w = tk.Entry(self)

        tk.Label(self, text="Public key:").grid()

        self.public_key_var = tk.StringVar()
        self.public_key_var.set("(61, 51, 31)")

        self.pub_key = tk.Entry(self, textvariable=self.public_key_var)
        self.pub_key.grid(sticky=tk.E+tk.W)


        tk.Label(self, text="Private key: ").grid()
        self.key_var = tk.StringVar()
        self.key_var.set("43")

        self.key = tk.Entry(self, textvariable=self.key_var)
        self.key.grid(sticky=tk.E+tk.W)

        self.encrypt = tk.Button(self, text='Generate keys',
            command=self.generate_keys)
        self.encrypt.grid()


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


    def generate_keys(self):
        self.pub, self.priv = generare_cheie()

        self.public_key_var.set(str(self.pub))
        self.key_var.set(str(self.priv))


    def encrypt_func(self):
        alphabet = self.alphabet_var
        n = len(alphabet)

        try:
            numeric = [alphabet.index(x) for x in self.plaintext_var.get()]
        except:
            tkMessageBox.showerror('Error',"Invalid character in plain text")
            return

        try:
            public_key = eval(self.public_key_var.get())
            private_key = eval(self.key_var.get())
            print(public_key, private_key)
        except:
            tkMessageBox.showerror('Error',"Invalid character in key")
            return

        nr_encryption = []
        for letter in numeric:
            nr_encryption.append(encrypt(public_key, letter))

        print(nr_encryption)

        encryption = []

        for el1, el2 in nr_encryption:
            encryption.append(el1//n)
            encryption.append(el1%n)
            encryption.append(el2//n)
            encryption.append(el2%n)

        print(encryption)
        self.cyphertext_var.set("".join(alphabet[i] for i in encryption))

    def decrypt_func(self):
        alphabet = self.alphabet_var
        n = len(alphabet)

        numeric = [alphabet.index(x) for x in self.cyphertext_var.get()]
        it = iter(numeric)
        try:
            public_key = eval(self.public_key_var.get())
            private_key = eval(self.key_var.get())
            print(public_key, private_key)
        except:
            tkMessageBox.showerror('Error',"Invalid character in key")
            return


        decryption = []
        for g1, g2, d1, d2 in zip(it, it, it, it):
            gamma = g1*n+g2
            delta = d1*n+d2
            print(gamma, delta)
            decryption.append(decrypt(public_key, private_key, gamma, delta ))

        print(decryption)
        self.plaintext_var.set("".join(alphabet[i] for i in decryption))


app = Application()
app.master.title('Sample application')
app.mainloop()
