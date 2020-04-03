from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
from Histogramme import hist
import cv2 as cv
import matplotlib.pyplot as plt


class MyApp:

    def __init__(self):
        self.window = Tk()
        self.window.title("Traitement d'image")
        self.window.geometry("720x480")
        self.width = 500
        self.height = 400
        self.couleur="#FFFFFF"
        self.window.minsize(self.width, self.height)
        self.window.config(background=self.couleur)
        self.menu_barre = Menu(self.window)
        self.file_histogramme = Menu()
        self.file_contraste = Menu()
        self.file_filtre = Menu()
        self.file_contour = Menu()

        # initialization des composants
        self.canvas = Canvas(self.window, width=self.width, height=self.height, bg=self.couleur, highlightthickness=0)

        # On charge le menu
        self.creer_menu()

        # empaquetage
        self.canvas.pack(expand=YES)

    def creer_menu(self):
        # Menu fichier
        file_menu = Menu(self.menu_barre, tearoff=0)
        file_menu.add_command(label="Nouveau", command=self.ouvrir_image)
        file_menu.add_command(label="Quitter", command=self.window.quit)

        # Menu histogramme
        self.file_histogramme = Menu(self.menu_barre, tearoff=0)
        self.file_histogramme.add_command(label="Histogramme", command=self.histograme, state="disabled")

        # Menu Contraste
        self.file_contraste = Menu(self.menu_barre, tearoff=0)
        self.file_contraste.add_command(label="Transformation Linéaire", command=self.transformation_lineaire, state="disabled")
        self.file_contraste.add_command(label="Transformation Linéaire avec saturation", command=self.transformation_lineaire_avec_saturation,
                                        state="disabled")
        self.file_contraste.add_command(label="Correction gamma", command=self.correctionGamma, state="disabled")
        self.file_contraste.add_command(label="Egalisation Histogramme", command=self.egalisationHistogramme, state="disabled")

        # Menu filtre
        self.file_filtre = Menu(self.menu_barre, tearoff=0)
        self.file_filtre.add_command(label="Moyenneur 3x3", command=self.moyenneur3, state="disabled")
        self.file_filtre.add_command(label="Moyenneur 5x5", command=self.moyenneur5, state="disabled")
        self.file_filtre.add_command(label="Moyenneur 7x7", command=self.moyenneur7, state="disabled")
        self.file_filtre.add_command(label="Gaussien 3x3", command=self.gaussien3, state="disabled")
        self.file_filtre.add_command(label="Gaussien 5x5", command=self.gaussien5, state="disabled")
        self.file_filtre.add_command(label="Gaussien 7x7", command=self.gaussien7, state="disabled")
        self.file_filtre.add_command(label="Median 3x3", command=self.median3, state="disabled")
        self.file_filtre.add_command(label="Median 5x5", command=self.median5, state="disabled")
        self.file_filtre.add_command(label="Median 7x7", command=self.median7, state="disabled")

        # Menu contours
        self.file_contour = Menu(self.menu_barre, tearoff=0)
        self.file_contour.add_command(label="Robert", command=self.robert, state="disabled")
        self.file_contour.add_command(label="Prewitt", command=self.prewitt, state="disabled")
        self.file_contour.add_command(label="Sobel", command=self.sobel, state="disabled")
        self.file_contour.add_command(label="Laplacien", command=self.laplacien, state="disabled")
        self.file_contour.add_command(label="Canny", command=self.canny, state="disabled")

        self.menu_barre.add_cascade(label="Fichier", menu=file_menu)
        self.menu_barre.add_cascade(label="Caractéristiques", menu=self.file_histogramme)
        self.menu_barre.add_cascade(label="Contraste", menu=self.file_contraste)
        self.menu_barre.add_cascade(label="Filtres", menu=self.file_filtre)
        self.menu_barre.add_cascade(label="Contours", menu=self.file_contour)

        self.window.config(menu=self.menu_barre)

    def ouvrir_image(self):
        filename = filedialog.askopenfilename(title="Ouvrir une image", filetypes=[('all files', '.*')])
        image = cv.imread(filename)
        self.image = cv.cvtColor(image, cv.COLOR_BGR2GRAY);
        height, width = self.image.shape
        imgScale = self.width/width
        newX,newY = self.image.shape[1]*imgScale, self.image.shape[0]*imgScale
        resized = cv.resize(self.image,(int(newX),int(newY)))
        self.img = ImageTk.PhotoImage(image=Image.fromarray(resized))
        self.canvas.create_image(0, 0, anchor=NW, image=self.img)

        self.file_histogramme.entryconfig("Histogramme", state="normal")
        self.file_contraste.entryconfig("Transformation Linéaire", state="normal")
        self.file_contraste.entryconfig("Transformation Linéaire avec saturation", state="normal")
        self.file_contraste.entryconfig("Correction gamma", state="normal")
        self.file_contraste.entryconfig("Egalisation Histogramme", state="normal")
        self.file_filtre.entryconfig("Moyenneur 3x3", state="normal")
        self.file_filtre.entryconfig("Moyenneur 5x5", state="normal")
        self.file_filtre.entryconfig("Moyenneur 7x7", state="normal")
        self.file_filtre.entryconfig("Gaussien 3x3", state="normal")
        self.file_filtre.entryconfig("Gaussien 5x5", state="normal")
        self.file_filtre.entryconfig("Gaussien 7x7", state="normal")
        self.file_filtre.entryconfig("Median 3x3", state="normal")
        self.file_filtre.entryconfig("Median 5x5", state="normal")
        self.file_filtre.entryconfig("Median 7x7", state="normal")
        self.file_contour.entryconfig("Robert", state="normal")
        self.file_contour.entryconfig("Prewitt", state="normal")
        self.file_contour.entryconfig("Sobel", state="normal")
        self.file_contour.entryconfig("Laplacien", state="normal")
        self.file_contour.entryconfig("Canny", state="normal")

    def histograme(self):
        plt.plot(hist.histogramme(self.image))
        plt.title("Histogramme")    
        plt.show()

    def transformation_lineaire(self):
        self.plot(hist.transformationLinaire(self.image), "Transformation Linéaire")

    def transformation_lineaire_avec_saturation(self):
        self.toplevel = Toplevel()
        self.toplevel.title("Selectionnez SMax et SMin")
        self.entry1 = Entry(self.toplevel)
        label1 = Label(self.toplevel, text="Valeur max", font=("Courrier", 16))
        label1.grid(row=1, column=1, padx=1, pady=1)
        self.entry1.grid(row=1, column=2, padx=1, pady=1)
        self.entry2 = Entry(self.toplevel)
        label2 = Label(self.toplevel, text="Valeur min", font=("Courrier", 16))
        label2.grid(row=2, column=1, padx=1, pady=1)
        self.entry2.grid(row=2, column=2, padx=1, pady=1)
        Button(self.toplevel, text='Valider', command=self.validertransformationLinaireAvecSaturation).grid(row=3, column=0, sticky=W + E, padx=2, pady=5)
        Button(self.toplevel, text='Annuler', command=self.toplevel.destroy).grid(row=3, column=1, sticky=W + E, padx=2, pady=5)
        self.toplevel.wait_window(self.toplevel)

    def validertransformationLinaireAvecSaturation(self):
        max = self.entry1.get()
        min = self.entry2.get()
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.toplevel.destroy()
        if max != '' and min != '' and int(max) > int(min):
            self.plot(hist.transformationLinaireAvecSaturation(self.image, int(max), int(min)), "Transformation Linéaire avec saturation")

    def correctionGamma(self):
        self.toplevel = Toplevel()
        self.toplevel.title("Choisissez gamma")
        self.entry1 = Entry(self.toplevel)
        label1 = Label(self.toplevel, text="Valeur gamma", font=("Courrier", 16))
        label1.grid(row=1, column=1, padx=1, pady=1)
        self.entry1.grid(row=1, column=2, padx=1, pady=1)
        Button(self.toplevel, text='Valider', command=self.validercorrectionGamma).grid(row=3, column=0, sticky=W + E, padx=2, pady=5)
        Button(self.toplevel, text='Annuler', command=self.toplevel.destroy).grid(row=3, column=1, sticky=W + E, padx=2, pady=5)
        self.toplevel.wait_window(self.toplevel)

    def validercorrectionGamma(self):
        gamma = self.entry1.get()
        self.entry1.delete(0, END)
        self.toplevel.destroy()
        if gamma != '':
            self.plot(hist.adjust_gamma(self.image, int(gamma)), "Correction gamma")

    def egalisationHistogramme(self):
        self.plot(hist.egalisationHistogramme(self.image), "Egalisation de l'histogramme")

    def moyenneur3(self):
        self.plot(hist.filtreMoyenneur3(self.image), "Filtre moyenneur 3x3")

    def moyenneur5(self):
        self.plot(hist.filtreMoyenneur5(self.image), "Filtre moyenneur 5x5")

    def moyenneur7(self):
        self.plot(hist.filtreMoyenneur7(self.image), "Filtre moyenneur 7x7")

    def gaussien3(self):
        self.plot(hist.filtreGaussien3(self.image), "Filtre gaussien 3x3")

    def gaussien5(self):
        self.plot(hist.filtreGaussien5(self.image), "Filtre gaussien 5x5")

    def gaussien7(self):
        self.plot(hist.filtreGaussien7(self.image), "Filtre gaussien 7x7")

    def median3(self):
        self.plot(hist.filtreMedian3(self.image), "Filtre Median 3x3")

    def median5(self):
        self.plot(hist.filtreMedian5(self.image), "Filtre Median 5x5")

    def median7(self):
        self.plot(hist.filtreMedian7(self.image), "Filtre Median 7x7")

    def prewitt(self):
        plt.imshow(hist.prewitt(self.image), cmap="gray")
        plt.title("Filtre de Prewitt")
        plt.show()

    def robert(self):
        plt.imshow(hist.robert(self.image), cmap="gray")
        plt.title("Filtre de Robert")
        plt.show()

    def sobel(self):
        plt.imshow(hist.sobel(self.image), cmap="gray")
        plt.title("Filtre de Sobel")
        plt.show()

    def laplacien(self):
        plt.imshow(hist.laplacien(self.image), cmap="gray")
        plt.title("Filtre de Laplacien")
        plt.show()

    def canny(self):
        self.toplevel = Toplevel()
        self.toplevel.title("Selectionnez SMax et SMin")
        self.entry1 = Entry(self.toplevel)
        label1 = Label(self.toplevel, text="seuils max", font=("Courrier", 16))
        label1.grid(row=1, column=1, padx=1, pady=1)
        self.entry1.grid(row=1, column=2, padx=1, pady=1)
        self.entry2 = Entry(self.toplevel)
        label2 = Label(self.toplevel, text="seuils min", font=("Courrier", 16))
        label2.grid(row=2, column=1, padx=1, pady=1)
        self.entry2.grid(row=2, column=2, padx=1, pady=1)
        Button(self.toplevel, text='Valider', command=self.validerCanny).grid(row=3, column=0, sticky=W + E, padx=2, pady=5)
        Button(self.toplevel, text='Annuler', command=self.toplevel.destroy).grid(row=3, column=1, sticky=W + E, padx=2, pady=5)
        self.toplevel.wait_window(self.toplevel)

    def validerCanny(self):
        max = self.entry1.get()
        min = self.entry2.get()
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.toplevel.destroy()
        if max != '' and min != '' and int(max) > int(min):
            plt.imshow(hist.canny(self.image, int(max), int(min)), cmap="gray")
            plt.title("Filtre de Canny")
            plt.show()

    def plot(self, image, titre):
        fig = plt.figure(1)
        plt.gcf().subplots_adjust(wspace=0.5, hspace=0.3)

        fig.add_subplot(2, 2, 1)
        plt.imshow(self.image, cmap="gray")
        plt.title("Avant")

        fig.add_subplot(2, 2, 2)
        plt.imshow(image, cmap="gray")
        plt.title(titre)

        fig.add_subplot(2, 2, 3)
        plt.plot(hist.histogramme(self.image))
        plt.title("Avant")

        fig.add_subplot(2, 2, 4)
        plt.plot(hist.histogramme(image))
        plt.title("Après")
        plt.show()
        plt.close()

def main():
    app = MyApp()
    app.window.mainloop()

if __name__ == '__main__':
    main()
