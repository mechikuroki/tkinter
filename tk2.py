from tkinter import *
from tkinter import ttk, messagebox
import json
from pathlib import Path

class Inventory:
    def __init__(self, root):
        super().__init__
        self.root = root
        self.root.title = "Sistema de gestión de inventarios"
        self.root.geometry = ("800x600")
        for i in range(10): self.root.grid_rowconfigure(i, weight=1)
        for i in range(5): self.root.grid_columnconfigure(i, weight=1)
        
        self.treesection = LabelFrame(self.root, bg="lightblue")
        self.treesection.grid(row=0, column=1, rowspan=10, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.entrysection = LabelFrame(self.root, bg="lightblue")
        self.entrysection.grid(row=0, column=0, rowspan=10, columnspan=2, sticky="nsew", padx=5, pady=5)

        count = 1
        for i in ["name", "key", "price", "stock", "category"]:
            exec(f'self.{i}label = Label(self.entrysection, text="{i.title()}")')
            exec(f'self.{i}label.grid(row={count-1}, column=0, columnspan=3, sticky="we")')
            exec(f'self.{i} = StringVar()')
            exec(f'self.{i}entry = Entry(self.entrysection, textvariable=self.{i})')
            exec(f'self.{i}entry.grid(row={count}, column=0, columnspan=3, sticky="we")')
            count += 2

        self.savebutton = Button(self.entrysection, text="Guardar", command=self.save)
        self.savebutton.grid(row=10, column=1, padx=3, pady=3)
        self.changebutton = Button(self.entrysection, text="Modificar", command=self.change)
        self.changebutton.grid(row=10, column=2, padx=3, pady=3)
        self.erasebutton = Button(self.entrysection, text="Borrar", command=self.erase)
        self.erasebutton.grid(row=10, column=3, padx=3, pady=3)
        
        self.tree = ttk.Treeview(self.treesection)

    def load_json_file(self, tree):
        try:
            with open(Path("inventory.json").resolve(), "r") as file:
                data = json.load(file) 

            for item in tree.get_children():
                tree.delete(item)

            json_to_tree(tree, data, "")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load JSON file.\n{e}")

    def json_to_tree(self, tree, data, parent_node):
        if isinstance(data, dict):
            if tree.exists(data["category"].title()):
                

            for key, value in data.items():
                new_node = tree.insert(parent_node, tk.END, text=str(key), open=True)
                json_to_tree(tree, value, new_node)
        elif isinstance(data, list):
            for index, item in enumerate(data):
                new_node = tree.insert(parent_node, tk.END, text=f"[{index}]", open=True)
                json_to_tree(tree, item, new_node)
        else:
            tree.insert(parent_node, tk.END, text=str(data))


    def save(self):
        pass
    def change(self):
        pass
    def erase(self):
        pass


root = Tk()
app = Inventory(root)
root.mainloop()
