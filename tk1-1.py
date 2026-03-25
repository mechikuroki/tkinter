from tkinter import *
from tkinter import ttk 

root = Tk()
root.title("Calculadora")


def calculate():
    global num1, num2, operationlist
    try:
        n1 = float(num1.get())
        n2 = float(num2.get())
        operator = operationlist.curselection()
        operator = operator[0]
        operator = operationlist.get(operator)
        if (operator == "raiz" or "/") and n2 == 0:
            result.set("Math Error")
            return
        elif operator != "raiz":
            operation = eval(f"{n1} {operator} {n2}")
        else:
            operation = n1 ** (1/ n2)
        result.set(operation)
        print(operation)
        return
    except Exception:
        pass


s = ttk.Style()

s.configure('Lightblue.TFrame', background='lightblue')

mainframe = ttk.Frame(root, padding=(3, 3, 12, 12), style='Lightblue.TFrame') 
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

num1 = StringVar()
num1_entry = ttk.Entry(mainframe, width=7, textvariable=num1)
num1_entry.grid(column=2, row=1, sticky=(W, E))

num2 = StringVar()
num2_entry = ttk.Entry(mainframe, width=7, textvariable=num2)
num2_entry.grid(column=2, row=2, sticky=(W, E))

choices = ("+", "-", "*", "/", "**", "raiz")
choicesvar = StringVar(value=choices)
operationlist = Listbox(mainframe, listvariable=choicesvar)
operationlist.grid(column=3, row=1)

result = StringVar()
ttk.Label(mainframe, textvariable=result).grid(column=2, row=3, sticky=(W, E))

ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)


root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

num1_entry.focus()
num2_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()
