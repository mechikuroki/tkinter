from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
import os

class cancha:
    def __init__(self, root, imagencancha, plantel):
        super().__init__()
        #seteo root
        self.croot = root
        self.croot.title("Cancha virtual")
        self.croot.geometry("600x770")
        self.croot.resizable(False, False)
        #seteo la foto del fondo como foto de tkinter
        self.canchafoto = Image.open(Path(imagencancha).resolve())
        self.canchafoto = self.canchafoto.resize((600, 770), Image.Resampling.LANCZOS)
        self.canchafoto = ImageTk.PhotoImage(self.canchafoto)
        self.frame = Frame(self.croot, width=600, height=770)
        self.frame.place(x=0, y=0, anchor=NW)
        self.label = Label(self.frame, image=self.canchafoto, width=600, height=770)
        self.label.place(x=0, y=0, anchor=NW)
        
        self.jugadores_fotos = []
        self.jugadores = [] 
        self.selected = ""
        #configurar las fotos como, bueno, fotos de tkinter 
        for i in plantel:
            j = Image.open(Path(os.path.join("jugadores", i)).resolve())
            j = j.resize((100, 106), Image.Resampling.LANCZOS)
            j = ImageTk.PhotoImage(j)
            self.jugadores_fotos.append(j)

        self.posiciones = [
            (300, 680), 
            (100, 550), (235, 570), (365, 570), (500, 550), 
            (210, 440), (390, 440), 
            (100, 280), (300, 280), (500, 280), 
            (300, 100)  
        ]
        #setear a los jugadores en sus posiciones
        for i, pos in enumerate(self.posiciones):
            btn = ttk.Button(self.frame, image=self.jugadores_fotos[i])
            btn.pos_index = i 
            btn.config(command=lambda b=btn: self.select(b))
            btn.place(x=pos[0], y=pos[1], anchor=CENTER)
            self.jugadores.append(btn)

   #funcion para hacer el switch 
    def select(self, clicked_btn):
        if not self.selected:
            self.selected = clicked_btn
        elif self.selected == clicked_btn:
            return
        else:
            idx1 = clicked_btn.pos_index
            idx2 = self.selected.pos_index

            pos1 = self.posiciones[idx1]
            pos2 = self.posiciones[idx2]

            self.selected.place(x=pos1[0], y=pos1[1], anchor=CENTER)
            clicked_btn.place(x=pos2[0], y=pos2[1], anchor=CENTER)

            self.selected.pos_index, clicked_btn.pos_index = idx1, idx2

            self.selected = ""

if __name__ == "__main__":
    root = Tk()
    plantel = ("cambeses.jpg", "rojas.jpg", "rojo.jpg", "di-cesare.jpg", "cannavo.jpg", "sosa.jpg", "zuculini.jpg", "conechny.jpg", "fernandez.jpg", "martirena.jpg", "solari.jpg")
    app = cancha(root, "imagencancha.jpg", plantel)    
    root.mainloop()





