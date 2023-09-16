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
        self.Coding_Area = tk.Text(self.root, height=15, width=125, font=("Helvetica", 16), background="#282C34", foreground="#D7D7D7")
        self.Coding_Area.grid(row=0, column=0)

        self.scrollbar1 = tk.Scrollbar(self.root, command = self.Coding_Area.yview)
        self.scrollbar1.grid(row = 0, column = 1, sticky = 'ns')
        self.Coding_Area.config(yscrollcommand = self.scrollbar1.set)

        self.Run_Button = tk.Button(self.root, text="Run", width=10, command=self.Submit_Code, font=("Helvetica", 16), background="#3D3F42", foreground="white")
        self.Run_Button.grid(row=2, column=0)

        self.Output_Area = tk.Label(self.root, text="", height=15, width=125, font=("Helvetica", 16), background="Black", foreground="White")
        self.Output_Area.grid(row=1, column=0)

        self.Output_Area = tk.Text(self.root, height=15, width=125, font=("Helvetica", 16), background="Black", foreground="White", state="disabled")
        self.Output_Area.grid(row=1, column=0)

        self.scrollbar2 = tk.Scrollbar(self.root, command=self.Output_Area.yview)
        self.scrollbar2.grid(row=1, column=1, sticky="NS")

        self.Output_Area.config(yscrollcommand=self.scrollbar2.set)


    def Submit_Code(self):
        self.User_Input = self.Coding_Area.get("1.0", tk.END)
        self.Tokenize()
        self.Scan()
        self.Check_Declarations()
        # self.Check_Semicolon()
        self.Check_While()
        self.switch_check()
    
    def Tokenize(self):
        self.Lines = self.User_Input.strip().split('\n')
        for Index in range(0, len(self.Lines)):
            self.Lines[Index] = re.findall(r'([-]?\d*\.\d+|\d+|[A-Za-z]+|\'[A-Za-z]+\'|\"(?:[^\"\\\n]|\\\"|\\\\)*\"|[!=<>]=|\|\||&&|[^\s\w\n])', self.Lines[Index])
            
        # print("Lines Inputs = " + str(self.Lines))

    def Scan(self):
        self.Scanner_Result = [[[0, 0] for Column in range(len(self.Lines[Line]))]for Line in range(len(self.Lines))]
        self.Declared_Variables = []
        for Line in range(0 , len(self.Lines)):
            for Index in range(0, len(self.Lines[Line])):
                Flag_Found = False
                for key, value in self.Scanner_List.items():
                    if self.Lines[Line][Index] == key:
                        
                            self.Scanner_Result[Line][Index][0] = key
                            self.Scanner_Result[Line][Index][1] = value
                            Flag_Found = True
                            break
                    
                if Flag_Found == False:
                    if re.match(r"(['\"])(?:(?=(\\?))\2.)*?\1", self.Lines[Line][Index]):
                        self.Scanner_Result[Line][Index][0] = self.Lines[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "String"
                    
                    elif re.match(r'^-?\d+(\.\d+)?$', self.Lines[Line][Index]):
                        self.Scanner_Result[Line][Index][0] = self.Lines[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Integer"
                    elif (len(self.Scanner_Result) > 0 and self.Scanner_Result[Line][Index - 1][1] == "Identifiers"):
                        self.Scanner_Result[Line][Index][0] = self.Lines[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Variable"
                        self.Declared_Variables.append(self.Lines[Line][Index])
                    elif (len(self.Scanner_Result) > 0):
                        self.Scanner_Result[Line][Index][0] = self.Lines[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Variable"

        # print("Declared Variables = " + str(self.Declared_Variables))
        # print("Scanner Results = " + str(self.Scanner_Result))

    def Check_Declarations(self):
        self.Declaration_Erros = self.Scanner_Result.copy()
        for Line in range(0 , len(self.Scanner_Result)):
            for Index in range(0, len(self.Scanner_Result[Line])):
                if self.Scanner_Result[Line][Index][1] == "Variable" and not self.Scanner_Result[Line][Index][0] in self.Declared_Variables:
                    self.Declaration_Erros[Line][Index][1] = "Variable Not Declared"
        
        # print("Declaration Errors = " + str(self.Declaration_Erros))
        # self.Output_Area.configure(text = '\n'.join([f"{column[0]} -> {column[1]}" for row in self.Declaration_Erros for column in row]), anchor = "nw",  wraplength = 600)

    # def Check_Semicolon(self):
    #     self.SemiColon_Error = self.Declaration_Erros.copy()
    #     for Line in range(0 , len(self.Scanner_Result)):
    #         if self.Declaration_Erros[Line][len(self.Declaration_Erros[Line]) - 1][1] != "Semicolon":
    #             self.SemiColon_Error[Line].append([';', "Error: There is no semicolon"])
        
    #     print("SemiColon Errors = " + str(self.SemiColon_Error))
    #     self.Output_Area.configure(state="normal")
    #     self.Output_Area.delete(1.0, tk.END)
    #     self.Output_Area.insert(tk.END, '\n'.join([f"{column[0]} -> {column[1]}" for row in self.SemiColon_Error for column in row]))
    #     self.Output_Area.configure(state="disabled")

    def Check_While(self):
        counter=0;
        flag=False;
        order_list=['while','(',')','{' ,'}']
        for i in range(0,len(self.Scanner_Result)):
            for k in range(len(self.Scanner_Result[i])):
                if self.Scanner_Result[i][k][0] == 'while' and order_list[counter] == 'while':
                    self.Scanner_Result[i][k][1] = 'Reserved words'
                    counter += 1
                    flag=True
                elif self.Scanner_Result[i][k][0] == '(' and order_list[counter] == '(':
                        self.Scanner_Result[i][k][1] = 'Open Bracket'
                        counter += 1
                elif self.Scanner_Result[i][k][0] == ')' and order_list[counter] == ')':
                        self.Scanner_Result[i][k][1] = 'Close Bracket'
                        counter += 1
                elif self.Scanner_Result[i][k][0] == '{' and order_list[counter] == '{':
                        self.Scanner_Result[i][k][1] = 'Open Curly Bracket'
                        counter += 1
                elif self.Scanner_Result[i][k][0] == '}' and order_list[counter] == '}':
                        self.Scanner_Result[i][k][1] = 'Close Curly Bracket'
                        counter += 1
        if counter != len(order_list) and flag==True:
            self.Scanner_Result[len(self.Scanner_Result)-1].append(['Error in while loop  ',"Syntax Error: Missing or misplaced token."])
        # print("scanner list after while = " + str(self.Scanner_Result))
        self.Output_Area.configure(state="normal")
        self.Output_Area.delete(1.0, tk.END)
        self.Output_Area.insert(tk.END, '\n'.join([f"{column[0]} -> {column[1]}" for row in self.Scanner_Result for column in row]))
        self.Output_Area.configure(state="disabled")
        
        




    def switch_check(self):
        counter = 0
        flag = False
        flag_case = False
        order_list = ['switch', '(', ')', '{', 'case', ':', 'break', 'default', ':', '}']
        case_counter = 0
        colon_counter = 0
        break_counter = 0
        default_counter = 0
        switch_counter = 0
        case_holder=0
        default_holder=0

        for i in range(len(self.Scanner_Result)):
            for k in range(len(self.Scanner_Result[i])):
                token = self.Scanner_Result[i][k][0]

                # check_list.append(token)
                if token == order_list[counter]:
                    counter += 1

                if token == 'switch':
                    flag = True
                    switch_counter += 1
                if token == 'case':
                    flag_case = True
                    # print('flag case',flag_case, " flag switch" , flag)
                    case_counter += 1
                if token == ':':
                    colon_counter += 1
                if token == 'break':
                    break_counter += 1
                if token == 'default':
                    default_counter += 1
        print('Scanner_Result ',len(self.Scanner_Result))
        for i in range (len(self.Scanner_Result)):
            for k in range(len(self.Scanner_Result[i])):
                print(self.Scanner_Result[i][k][0])
                if(self.Scanner_Result[i][k][0] == 'default'):
                        default_holder=i
        for i in range(len(self.Scanner_Result)):
            for k in range (len(self.Scanner_Result[i])):
                if (self.Scanner_Result[i][k][0] == 'case'):
                    case_holder=i
                    print('error 1 case holder ',case_holder, ' default holder ',default_holder)  
        if flag and (counter !=len(order_list)):
            self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: invalid syntax of switch '])
        if(case_holder > default_holder and default_counter > 0):
            self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing case after default  ' ])

        elif flag_case==True and  case_counter != break_counter:
            self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing break   '])
            # print('flag case',flag_case, " flag switch" , flag)

        # elif flag and (counter != len(order_list) or switch_counter != 1 or  default_counter != 1  or case_counter != colon_counter - 1 ):
        #     print('error 2')
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing or misplaced token.'])
        
        elif flag and (case_counter != colon_counter - 1):
            self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: invalid syntax of colon ' ])
        elif flag_case==True and flag==False or case_counter != break_counter:
            self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing switch '+str(0)])
            print('flag case',flag_case, " flag switch" , flag)

        # if flag and (counter != len(order_list) or switch_counter != 1 or  default_counter != 1  or case_counter != colon_counter - 1 ):
        #     print('error 2')
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing or misplaced token.'])
        # if flag_case==True and  case_counter != break_counter:
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing break or case at line '])
        #     # print('flag case',flag_case, " flag switch" , flag)
        # if flag_case==True and flag==False or case_counter != break_counter:
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing switch '+str(0)])
        #     print('flag case',flag_case, " flag switch" , flag)
        print("scanner list after switch =", self.Scanner_Result)

        self.Output_Area.configure(state="normal")
        self.Output_Area.delete(1.0, tk.END)
        self.Output_Area.insert(tk.END, '\n'.join([f"{column[0]} -> {column[1]}" for row in self.Scanner_Result for column in row]))
        self.Output_Area.configure(state="disabled")










Scanner_List = {"int" : "Identifiers", "float" : "Identifiers", "string" : "Identifiers", "double" : "Identifiers",
"bool" : "Identifiers", "char" : "Identifiers", "+" : "Operator", "-" : "Operator", "/" : "Operator", 
"%" : "Operator", "*" : "Operator", "(" : "Open Bracket", ")" : "Close Bracket", "{" : "Open Curly Bracket", 
"}" : "Close Curly Bracket", "," : "Comma", ";"  : "Semicolon", "&&" : "And", "||"  : "Or", "<" : "Less than", 
">" : "Greater than", "=" : "Become", "==" : "Equal", "!" : "Not", "for" : "Reserved words", "while" : "Reserved words", 
"if" : "Reserved words", "do" : "Reserved words", "return" : "Reserved words", "break" : "Reserved words", 
"continue" : "Reserved words", "end" : "Reserved words", "'" : "Quotation", '"': "Quotation", ".": "Dot","switch":"Reserved words","case":"Reserved words",
"default":"Reserved words",":":"colon"}

Main1 = Main(root, Scanner_List)
Main1.GUI()

root.mainloop()