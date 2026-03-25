from tkinter import *
from tkinter import ttk 

class lacalculadoramaslindadelatierra:
    def __init__(self):
        super().__init__()
        self.root = master
        self.root.title("Calculadora")
        self.s = ttk.Style()

        self.s.configure('Lightblue.TFrame', background='lightblue')

        self.mainframe = ttk.Frame(self.root, padding=(3, 3, 12, 12), style='Lightblue.TFrame') 
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        
        self.num1 = StringVar()
        self.num1_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.num1)
        self.num1_entry.grid(column=2, row=1, sticky=(W, E))

        self.num2 = StringVar()
        self.num2_entry = ttk.Entry(self.mainframe, width=7, textvariable=self.num2)
        self.num2_entry.grid(column=2, row=2, sticky=(W, E))

        self.choices = ("+", "-", "*", "/", "**", "raiz")
        self.choicesvar = StringVar(value=self.choices)
        self.operationlist = Listbox(self.mainframe, listvariable=self.choicesvar)
        self.operationlist.grid(column=3, row=1)

        ttk.Button(self.mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        self.result = StringVar()
        ttk.Label(self.mainframe, textvariable=self.result).grid(column=2, row=3, sticky=(W, E))
 
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.mainframe.columnconfigure(2, weight=1)
        for child in self.mainframe.winfo_children(): 
                child.grid_configure(padx=5, pady=5)

        self.num1_entry.focus()
        self.num2_entry.focus()
        self.root.bind("<Return>", self.calculate)


    def calculate(self):
        try:
            self.n1 = float(self.num1.get())
            self.n2 = float(self.num2.get())
            self.operator = self.operationlist.curselection()
            self.operator = self.operator[0]
            self.operator = self.operationlist.get(self.operator)
            if (self.operator == "raiz" or "/") and self.n2 == 0:
                self.result.set("Math Error")
                return
            elif self.operator != "raiz":
                self.operation = eval(f"{self.n1} {self.operator} {self.n2}")
            else:
                self.operation = self.n1 ** (1/ self.n2)
            self.result.set(self.operation)
            print(self.operation)
            return
        except Exception:
            pass


master = Tk()
app = lacalculadoramaslindadelatierra()
master.mainloop()
