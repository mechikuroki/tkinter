from tkinter import *
from tkinter import messagebox
import re
class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora (ahora linda)")
        self.root.geometry("700x900")
        
        self.equation = ""
        
        self.display = Entry(root, font=("Helvetica", 24), borderwidth=5, relief="flat", justify='right')
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=20, sticky="nsew")

        buttons = {
                'seven': '7', 'eight' : '8', 'nine' : '9', 'division' : '/',
                'four' : '4', 'five' : '5', 'six' : '6', 'multiplication' : '*',
                'one' : '1', 'two' : '2', 'three' : '3', 'minus' : '-',
                'erase' : 'C', 'zero' : '0', 'decimalpoint' : '.', 'plus' : '+',
                'power' : '^', 'root' : '^(1/', 'lpsis' : '(', 'rpsis' : ')'
            }

        row_val = 2
        col_val = 0
        for name, button in buttons.items():
            action = lambda x=button: self.click_event(x)
            exec(f'self.{name}button = Button(root, text=button, width=5, height=2, bg="lightblue", font=("Helvetica", 14), command=action).grid(row=row_val, column=col_val, sticky="nsew", padx=2, pady=2)')
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1
        self.equalbutton = Button(root, text="=", width=5, height=2, bg="lightblue", font=("Helvetica", 14), command=lambda: self.click_event("=")).grid(row=7, column=0, columnspan=4, sticky="nsew", padx=2, pady=2)
        for i in range(4): root.grid_columnconfigure(i, weight=1)
        for i in range(8): root.grid_rowconfigure(i, weight=1)

    def click_event(self, key):
        if key == "=":
            self.calculate()
        elif key == "C":
            self.clear_screen()
        elif key == "^(1/":
            self.equation += "**(1/"
            self.update_display("^(1/")
        elif key == "^":
            self.equation += "**"
            self.update_display("^")
        else:
            self.equation += str(key)
            self.update_display(key)

    def update_display(self, val):
        current = self.display.get()
        self.display.delete(0, END)
        self.display.insert(0, current + val)

    def clear_screen(self):
        self.equation = ""
        self.display.delete(0, END)

    def calculate(self):
        try:
            self.equation = re.sub(r'\b0+(?=\d)', '', self.equation)
            result = eval(self.equation)
            self.display.delete(0, END)
            self.display.insert(0, str(result))
            self.equation = str(result)
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            self.clear_screen()


root = Tk()
my_calc = Calculator(root)
root.mainloop()
