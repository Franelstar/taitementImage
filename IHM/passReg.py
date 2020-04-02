import tkinter as tk


class nom_fichier(tk.Toplevel):
    def __init__(self, parent, titre='titre', message='message'):
        tk.Toplevel.__init__(self, parent)
        self.title = titre
        self.entry = tk.Entry(self, width=50)
        self.entry.grid(row=1, columnspan=2, padx=2, pady=5)
        tk.Button(self, text='Valider', command=self.valider).grid(row=2, column=0,
                                                                   sticky=tk.W + tk.E, padx=2, pady=5)

        tk.Button(self, text='Annuler', command=self.destroy).grid(row=2, column=1,
                                                               sticky=tk.W + tk.E, padx=2, pady=5)
        self.wait_window(self)


    def valider(self):
        if not self.valid():
            return
        self.sortie()
        self.destroy()


    def valid(self):
        self.filename = self.entry.get()
        self.entry.delete(0, tk.END)
        if self.filename == '':
            return 0
        else:
            return 1


    def sortie(self):
        return self.filename


if __name__ == '__main__':
    root = tk.Tk()
    new_canal = nom_fichier(root, titre='Nom du Canal',
                            message='Veulliez saisir le nom du nouveau canal')
    filename = new_canal.sortie() + '.cfg'
    print
    filename
    root.mainloop()