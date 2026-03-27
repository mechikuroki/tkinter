from tkinter import *
from tkinter import ttk, messagebox
import ijson
from pathlib import Path

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
        self.treesection.grid_columnconfigure(0, weight=1)

        self.entrysection = LabelFrame(self.root, text="Ingreso", bg="lightblue")
        self.entrysection.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
        for i in range(11): self.entrysection.grid_rowconfigure(i, weight=1)
        for i in range(3): self.entrysection.grid_columnconfigure(i, weight=1)

        count = 1
        for i in ["name", "key", "price", "stock", "category"]:
            exec(f'self.{i}label = Label(self.entrysection, text="{i.title()}")')
            exec(f'self.{i}label.grid(row={count-1}, column=0, columnspan=3, sticky=NSEW)')
            exec(f'self.{i} = StringVar()')
            exec(f'self.{i}entry = Entry(self.entrysection, textvariable=self.{i})')
            exec(f'self.{i}entry.grid(row={count}, column=0, columnspan=3, sticky=NSEW)')
            count += 2

        self.savebutton = Button(self.entrysection, text="Guardar", command=self.save)
        self.savebutton.grid(row=10, column=0, padx=3, pady=3, sticky=NSEW)
        self.changebutton = Button(self.entrysection, text="Modificar", command=self.change)
        self.changebutton.grid(row=10, column=1, padx=3, pady=3, sticky=NSEW)
        self.erasebutton = Button(self.entrysection, text="Borrar", command=self.erase)
        self.erasebutton.grid(row=10, column=2, padx=3, pady=3, sticky=NSEW)
        
        self.tree = ttk.Treeview(self.treesection)
        self.load_json_file(self.tree)
        self.tree.grid(row=0, column=0, sticky=NSEW)
    def load_json_file(self, tree):
        try:
            for i in tree.get_children():
                tree.delete(i)

            with open(Path("inventory.json").resolve(), "rb") as file:
                parser = ijson.items(file, 'item')
                for data in parser:
                    self.json_to_tree(tree, data, "")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file.\n{e}")

    def json_to_tree(self, tree, data, parent_node):
        if isinstance(data, dict):  
            if tree.exists(data["category"].title()) == False:
                parent_node = tree.insert(parent_node, END, text=data["category"].title(), open=True)
            new_node = tree.insert(parent_node, END, text=data["key"], open=True)

            data.pop("category")
            data.pop("key")

            for key, value in data.items():
                self.json_to_tree(tree, value, new_node)
        else:
            tree.insert(parent_node, END, text=str(data))


    def save(self):
        pass
    def change(self):
        pass
    def erase(self):
        pass


root = Tk()
app = Inventory(root)
root.mainloop()
