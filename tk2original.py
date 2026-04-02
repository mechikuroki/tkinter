from tkinter import *
from tkinter import ttk, messagebox
import json, os, re 
from pathlib import Path

#á  é  í  ó  ú
#aclaracion: tengo el teclado en ingles y no tengo ganas de ponerlo en us international porque el layout se mezcla y encima muchos caracteres se vuelven medio
#cripticos para escribir; las letras en el archivo con tilde las copie del comentario de arriba pero me parece que para los comentarios no tiene mucha vuelta

#esto es lo que hice antes de darme cuenta que todo se tenia que cargar en memoria
class Inventory:
    def __init__(self, root):
        super().__init__()
        #configuro el root
        self.root = root
        self.root.title("Sistema de gestión de inventarios")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(1, weight=1)
        
        #configuro el cacho donde va a estar el treeview
        self.treesection = LabelFrame(self.root, text="Archivo", bg="lightblue")
        self.treesection.grid(row=0, column=2, sticky=NSEW, padx=5, pady=5)
        self.treesection.grid_rowconfigure(0, weight=1)
        self.treesection.grid_columnconfigure(0, weight=5)
        self.treesection.grid_columnconfigure(1, weight=1)

        #configuro la mitad donde van a estar los inputs
        self.entrysection = LabelFrame(self.root, text="Ingreso", bg="lightblue")
        self.entrysection.grid(row=0, column=0, columnspan=2, sticky=NSEW, padx=5, pady=5)
        for i in range(11): self.entrysection.grid_rowconfigure(i, weight=1)
        for i in range(3): self.entrysection.grid_columnconfigure(i, weight=1)

        #inputs normales
        count = 1
        for i in ["nombre", "llave", "precio"]:
            exec(f'self.{i}label = Label(self.entrysection, text="{i.title()}")')
            exec(f'self.{i}label.grid(row={count-1}, column=0, columnspan=3, sticky=NSEW)')
            exec(f'self.{i} = StringVar()')
            exec(f'self.{i}entry = Entry(self.entrysection, textvariable=self.{i})')
            exec(f'self.{i}entry.grid(row={count}, column=0, columnspan=3, sticky=NSEW)')
            count += 2
        
        #categoria por la tilde
        self.categorialabel = Label(self.entrysection, text="Categoría")
        self.categorialabel.grid(row=count-1, column=0, columnspan=3, sticky=NSEW)
        self.categoria = StringVar()
        self.categoriaentry = Entry(self.entrysection, textvariable=self.categoria)
        self.categoriaentry.grid(row=count, column=0, columnspan=3, sticky=NSEW)

        #el spinbox de stock
        self.stocklabel = Label(self.entrysection, text="Stock")
        self.stocklabel.grid(row=count+1, column=0, columnspan=3, sticky=NSEW)
        self.stockvar = IntVar(value=10)
        self.stock = Spinbox(self.entrysection, from_=0, to=1000, textvariable=self.stockvar, state="readonly")
        self.stock.grid(row=count+2, column=0, columnspan=3, sticky=NSEW)


        #los botones para guardar, modificar y borrar
        self.savebutton = Button(self.entrysection, text="Guardar", command=self.save)
        self.savebutton.grid(row=10, column=0, padx=3, pady=3, sticky=NSEW)
        self.changebutton = Button(self.entrysection, text="Modificar", command=self.change)
        self.changebutton.grid(row=10, column=1, padx=3, pady=3, sticky=NSEW)
        self.erasebutton = Button(self.entrysection, text="Borrar", command=self.erase)
        self.erasebutton.grid(row=10, column=2, padx=3, pady=3, sticky=NSEW)
        
        #el treeview en si
        self.tree = ttk.Treeview(self.treesection, columns=("Nombre", "Llave", "Precio", "Categoria", "Stock"), show="headings")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Llave", text="Llave")
        self.tree.heading("Precio", text="Precio")
        self.tree.heading("Categoria", text="Categoría")
        self.tree.heading("Stock", text="Stock")
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.scrollbar = ttk.Scrollbar(self.treesection, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.load_json_file(self.tree)

    #la funcion para que los campos sean automaticamente seleccionados
    def on_tree_select(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
        values = self.tree.item(selected_item)['values']
        self.nombre.set(values[0])
        self.llave.set(selected_item) 
        self.precio.set(values[2])
        self.categoria.set(values[3])
        self.stockvar.set(values[4])

    #esto carga el .jsonl de a pedazos 
    def load_json_file(self, tree):
        try:
            for i in tree.get_children():
                tree.delete(i)

            with open(Path("inventory.jsonl").resolve(), "r") as file:
                for i in file:
                    data = json.loads(i.strip())
                    self.tree.insert("", "end", iid=str(data["llave"]), values=(data["nombre"], data["precio"], data["categoria"], data["stock"]))
        except Exception as e:
            messagebox.showerror("Error", f"Falló en cargar el archivo JSON\n{e}")

	
    def clear_fields(self):
        self.llave.set("")
        self.nombre.set("")
        self.precio.set("")
        self.categoria.set("")

    #devuelve True si los valores son correctos, False si no lo son; si everyentry=False solo chequea la key (esto es para cuando borra)
    def check_values(self, everyentry=False):
        try: 
            if str(self.llave.get()).isalnum() == False:
                raise ValueError("Llave debe ser alfanumérica")
            if everyentry:
                if str(self.nombre.get()).isprintable() == False or str(self.nombre.get()) == "":
                    raise ValueError("Nombre debe ser imprimible")
                elif bool(re.match(r"^\d+(\.\d{1,2})?$", str(self.precio.get()))) == False:
                    raise ValueError("Precio debe ser numérico y tener como tope 2 decimales")
                elif str(self.categoria.get()).isprintable() == False:
                    raise ValueError("Categoria debe ser imprimible")
        except Exception as e:
            messagebox.showerror("Error", e)
            return False
        else:
            return True
    
    #la funcion del boton para guardar 
    def save(self):
        if self.check_values(everyentry=True) == False:
            return
        elif self.tree.exists(self.llave.get()):
            messagebox.showerror("Error", "Producto ya existe")
            return
        else:
            new_entry = {"nombre": self.nombre.get(), "llave": self.llave.get(), "precio": float(self.precio.get()),  "categoría": self.categoria.get(), "stock": int(self.stockvar.get())}
            try:
                with open('inventory.jsonl', 'a') as f:
                    f.write(json.dumps(new_entry) + '\n')
            except Exception as e:
                messagebox.showerror("Error", e)
            else:
                self.clear_fields()
            
            self.load_json_file(self.tree)

    #funcion del boton de modificar
    def change(self):
        if self.check_values(everyentry=True) == False:
            return
        elif self.tree.exists(self.llave.get()) == False:
            messagebox.showerror("Error", "Llave inexistente")
            return
        else:
            try:
                with open(Path('inventory.jsonl').resolve(), 'r') as reader, open('remadeinventory.jsonl', 'w') as writer:
                    for line in reader:
                        obj = json.loads(line)
                        if obj.get('llave') == self.llave.get():
                            obj['nombre'] = self.nombre.get()
                            obj['precio'] = float(self.precio.get())
                            obj['categoría'] = self.categoria.get()
                            obj['stock'] = int(self.stockvar.get())
                        writer.write(json.dumps(obj) + '\n')
                os.replace(Path('remadeinventory.jsonl').resolve(), Path('inventory.jsonl').resolve())
            except Exception as e:
                messagebox.showerror("Error", e)
            else:
                self.clear_fields()
            
            self.load_json_file(self.tree)


    #funcion del boton para borrar
    def erase(self):
        #cabe aclarar que esto borra solo con la llave: me parece que no tiene sentido que el usuario agregue otra info. Igualmente, se puede cambiar esto agregando 
        #everyentry=True a checkvalues() y chequeando luego que todos los items coincidan
        if self.check_values() == False:
            return
        elif self.tree.exists(self.llave.get()) == False:
            messagebox.showerror("Error", "Llave inexistente")
            return
        else:
            try:
                with open(Path('inventory.jsonl').resolve(), 'r') as reader, open('remadeinventory.jsonl', 'w') as writer:
                    for line in reader:
                        obj = json.loads(line)
                        if obj.get('llave') != self.llave.get():
                            writer.write(json.dumps(obj) + '\n')
                os.replace(Path('remadeinventory.jsonl').resolve(), Path('inventory.jsonl').resolve())
                self.clear_fields()
            except Exception as e:
                messagebox.showerror("Error", e)
            else:
                self.clear_fields()

            self.load_json_file(self.tree)
if __name__ == "__main__":
    root = Tk()
    app = Inventory(root)
    root.mainloop()
