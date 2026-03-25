from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
root = Tk()
class cancha:
    def __init__(self, root, imagencancha, *args):
        super().__init__()
        self.croot = root
        self.croot.title("Cancha virtual")
        self.croot.geometry("600x770")
        self.croot.resizable(False, False)
        self.canchafoto = Image.open(Path(imagencancha).resolve())
        self.canchafoto = self.canchafoto.resize((600, 770), Image.Resampling.LANCZOS)
        self.canchafoto = ImageTk.PhotoImage(self.canchafoto)
        self.canvas = Canvas(self.croot, width=600, height=770)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=NW, image=self.canchafoto)
        self.jugadores_fotos = []
        self.jugadores = [] 
        self.selected = ""
        
        for i in args:
            j = Image.open(Path(i).resolve())
            j = j.resize((100, 100), Image.Resampling.LANCZOS)
            j = ImageTk.PhotoImage(j)
            self.jugadores_fotos.append(j)

        self.posiciones = [
            (300, 680), 
            (100, 550), (235, 570), (365, 570), (500, 550), 
            (210, 440), (390, 440), 
            (100, 280), (300, 280), (500, 280), 
            (300, 100)  
        ]
        for i in self.posiciones:
            index = self.posiciones.index(i)
            self.jugadores.append(ttk.Button(self.croot, command=lambda: self.select(index), image=self.jugadores_fotos[index]))
            self.jugadores[index].place(x=i[0], y=i[1])
    def select(self, index):
        if not self.selected:
            self.selected = self.jugadores[index]
        else:
            posx1 = self.posiciones[index][0]
            print(posx1)
            posy1 = self.posiciones[index][1]
            print(posy1)
            posx2 = self.posiciones[self.jugadores.index(self.selected)][0]
            print(posx2)
            posy2 = self.posiciones[self.jugadores.index(self.selected)][1]
            print(posy2)
            self.jugadores[self.jugadores.index(self.selected)].place(posx1, posy1)
            self.jugadores[index].place(posx2, posy2)
            self.jugadores[index], self.jugadores[self.jugadores.index(self.selected)] = self.jugadores[self.jugadores.index(self.selected)], self.jugadores[index]
            self.selected = ""

app = cancha(root, "imagencancha.jpg", "cambeses.jpg", "rojas.jpg", "rojo.jpg", "di-cesare.jpg", "cannavo.jpg", "sosa.jpg", "zuculini.jpg", "conechny.jpg", "fernandez.jpg", "martirena.jpg", "solari.jpg")
root.mainloop()





