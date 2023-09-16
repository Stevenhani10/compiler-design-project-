import tkinter as tk
import re

root = tk.Tk()
root.title("Compiler")
root.state('zoomed')
root.configure(bg = "gray")

class Main:
    def __init__(self, root, Scanner_List):
        self.root = root
        self.Scanner_List = Scanner_List

    def GUI(self):
        self.Coding_Area = tk.Text(self.root, height=30, width=75, font=("Helvetica", 16), background="#282C34", foreground="#D7D7D7")
        self.Coding_Area.grid(row=0, column=0)

        self.Run_Button = tk.Button(self.root, text="Run", width=10, command=self.Submit_Code, font=("Helvetica", 16), background="#3D3F42", foreground="white")
        self.Run_Button.grid(row=1, column=0)

        self.Output_Area = tk.Label(self.root, text="", height=30, width=50, font=("Helvetica", 16), background="Black", foreground="White")
        self.Output_Area.grid(row=0, column=2)


    def Submit_Code(self):
        self.User_Input = self.Coding_Area.get("1.0", tk.END)
        self.Tokenize()
        self.Scan()
    
    def Tokenize(self):
        self.Tokenized_Input = re.findall(r'([-]?\d*\.\d+|\d+|[A-Za-z]+|\'[A-Za-z]+\'|\"(?:[^\"\\\n]|\\\"|\\\\)*\"|[!=<>]=|\|\||&&|[^\s\w\n])', self.User_Input)
        print(self.Tokenized_Input)

    def Scan(self):
        self.Scanner_Result = [[0, 0] for i in range(len(self.Tokenized_Input))]
        Declared_Variables = []
        for Word in range(0 , len(self.Tokenized_Input)):
            Flag_Found = False
            for key, value in self.Scanner_List.items():
                if self.Tokenized_Input[Word] == key:
                    
                        self.Scanner_Result[Word][0] = key
                        self.Scanner_Result[Word][1] = value
                        Flag_Found = True
                        break

            if Flag_Found == False:
                if re.match(r"(['\"])(?:(?=(\\?))\2.)*?\1", self.Tokenized_Input[Word]):
                    self.Scanner_Result[Word][0] = self.Tokenized_Input[Word]
                    self.Scanner_Result[Word][1] = "String"
                
                elif re.match(r'^-?\d+(\.\d+)?$', self.Tokenized_Input[Word]):
                    self.Scanner_Result[Word][0] = self.Tokenized_Input[Word]
                    self.Scanner_Result[Word][1] = "Integer"
                elif (len(self.Scanner_Result) > 0):
                    self.Scanner_Result[Word][0] = self.Tokenized_Input[Word]
                    self.Scanner_Result[Word][1] = "Variable"
                    Declared_Variables.append(self.Tokenized_Input[Word])

        self.Output_Area.configure(text = '\n'.join([f"{self.Scanner_Result[row][0]} -> {self.Scanner_Result[row][1]}" for row in range(len(self.Scanner_Result))]), anchor = "nw",  wraplength = 600)

Scanner_List = {"int" : "Identifiers", "float" : "Identifiers", "string" : "Identifiers", "double" : "Identifiers",
"bool" : "Identifiers", "char" : "Identifiers", "+" : "Operator", "-" : "Operator", "/" : "Operator", 
"%" : "Operator", "*" : "Operator", "(" : "Open Bracket", ")" : "Close Bracket", "{" : "Open Curly Bracket", 
"}" : "Close Curly Bracket", "," : "Comma", ";"  : "Semicolon", "&&" : "And", "||"  : "Or", "<" : "Less than", 
">" : "Greater than", "=" : "Become", "==" : "Equal", "!" : "Not", "for" : "Reserved words", "while" : "Reserved words", 
"if" : "Reserved words", "do" : "Reserved words", "return" : "Reserved words", "break" : "Reserved words", 
"continue" : "Reserved words", "end" : "Reserved words", "'" : "Quotation", '"': "Quotation",}

Main1 = Main(root, Scanner_List)
Main1.GUI()

root.mainloop()