from tkinter import *
from tkinter import ttk, messagebox
import ijson, json, os 
from pathlib import Path

#á  é  í  ó  ú

class Inventory:
    def __init__(self, root):
        super().__init__
        self.root = root
        self.root.title("Sistema de gestión de inventarios")
        self.root.geometry("1000x1000")
        self.root.grid_rowconfigure(0, weight=1)
        for i in range(2): self.root.grid_columnconfigure(i, weight=1)
        
        self.treesection = LabelFrame(self.root, text="Archivo", bg="lightblue")
        self.treesection.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
        self.treesection.grid_rowconfigure(0, weight=1)
        self.treesection.grid_columnconfigure(0, weight=5)
        self.treesection.grid_columnconfigure(1, weight=1)

        self.entrysection = LabelFrame(self.root, text="Ingreso", bg="lightblue")
        self.entrysection.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
        for i in range(11): self.entrysection.grid_rowconfigure(i, weight=1)
        for i in range(3): self.entrysection.grid_columnconfigure(i, weight=1)

        count = 1
        for i in ["nombre", "llave", "precio", "stock"]:
            exec(f'self.{i}label = Label(self.entrysection, text="{i.title()}")')
            exec(f'self.{i}label.grid(row={count-1}, column=0, columnspan=3, sticky=NSEW)')
            exec(f'self.{i} = StringVar()')
            exec(f'self.{i}entry = Entry(self.entrysection, textvariable=self.{i})')
            exec(f'self.{i}entry.grid(row={count}, column=0, columnspan=3, sticky=NSEW)')
            count += 2
        
        self.categorialabel = Label(self.entrysection, text="Categoría")
        self.categorialabel.grid(row=count-1, column=0, columnspan=3, sticky=NSEW)
        categorylist = ("Ropa", "Marroquinería", "Muebles", "Sacrificios")
        self.categoria = Spinbox(self.entrysection, bg="white", values=categorylist, state="readonly")
        self.categoria.grid(row=count, column=0, columnspan=3, sticky=NSEW)

        self.savebutton = Button(self.entrysection, text="Guardar", command=self.save)
        self.savebutton.grid(row=10, column=0, padx=3, pady=3, sticky=NSEW)
        self.changebutton = Button(self.entrysection, text="Modificar", command=self.change)
        self.changebutton.grid(row=10, column=1, padx=3, pady=3, sticky=NSEW)
        self.erasebutton = Button(self.entrysection, text="Borrar", command=self.erase)
        self.erasebutton.grid(row=10, column=2, padx=3, pady=3, sticky=NSEW)
        
        self.tree = ttk.Treeview(self.treesection)
        self.load_json_file(self.tree)
        self.tree.grid(row=0, column=0, sticky=NSEW)
        self.scrollbar = ttk.Scrollbar(self.treesection, orient=VERTICAL, command=self.tree.yview)
        self.scrollbar.grid(row=0, column=1, sticky=NSEW)
        self.tree.configure(yscrollcommand=self.scrollbar.set)


    def load_json_file(self, tree):
        try:
            for i in tree.get_children():
                tree.delete(i)

            with open(Path("inventory.jsonl").resolve(), "r") as file:
                for i in file:
                    data = json.loads(i.strip())
                    self.json_to_tree(tree, data, "")

        except Exception as e:
            messagebox.showerror("Error", f"Falló en cargar el archivo JSON\n{e}")

    def json_to_tree(self, tree, data, parent_node, datatype=None):
        if isinstance(data, dict):  
            parent_node = tree.insert(parent_node, END, text=data["categoría"].title(), open=True)
            new_node = tree.insert(parent_node, END, iid=data["llave"], text=data["nombre"], open=True)

            data.pop("categoría")
            data.pop("nombre")

            for key, value in data.items():
                self.json_to_tree(tree, value, new_node, datatype=key)
        else:
            tree.insert(parent_node, END, text=f"{datatype.title()}: {data}")

    def check_values(self):
        try:
            if str(self.nombre.get()).isprintable() == False:
                raise ValueError("Nombre debe ser imprimible")
            elif str(self.llave.get()).isidentifier() == False:
                raise ValueError("Llave debe ser formateada como identificador")
            elif str(self.precio.get()).isdigit() == False:
                raise ValueError("Precio debe ser numérico")
            elif str(self.stock.get()).isdigit() == False:
                raise ValueError("Stock debe ser un entero numérico")
            elif str(self.categoria.get()).isprintable() == False:
                raise ValueError("Categoría debe ser imprimible")
        except Exception as e:
            messagebox.showerror("Error", e)
            return False
        else:
            return True

    def save(self):
        if self.check_values() == False:
            return
        elif self.tree.exists(self.llave.get()):
            messagebox.showerror("Error", "Producto ya existe")
            return
        else:
            new_entry = {"nombre": self.nombre.get(), "llave": self.llave.get(), "precio": float(self.precio.get()), "stock": int(self.stock.get()), "categoría": self.categoria.get()}
            try:
                with open('inventory.jsonl', 'a') as f:
                    f.write(json.dumps(new_entry) + '\n')
            except Exception as e:
                messagebox.showerror("Error", e)
            self.load_json_file(self.tree)

    def change(self):
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
                        if obj.get('llave') == self.llave.get():
                            obj['nombre'] = self.nombre.get()
                            obj['precio'] = float(self.precio.get())
                            obj['stock'] = int(self.stock.get())
                            obj['categoría'] = self.categoria.get()
                        writer.write(json.dumps(obj) + '\n')
                os.replace(Path('remadeinventory.jsonl').resolve(), Path('inventory.jsonl').resolve())
                self.load_json_file(self.tree)
            except Exception as e:
                messagebox.showerror("Error", e)

    def erase(self):
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
                self.load_json_file(self.tree)
            except Exception as e:
                messagebox.showerror("Error", e)


root = Tk()
app = Inventory(root)
root.mainloop()
