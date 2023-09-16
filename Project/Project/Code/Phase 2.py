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
        self.Check_String_Syntax()
        self.Check_Declarations()
        self.Check_Syntax()
        self.Show_Results()

    def Tokenize(self):
        self.Lines = self.User_Input.strip().split('\n')
        self.Tokenized_Lines = self.Lines.copy()
        Pattern = r'([-]?\d*\.\d+|\d+|[A-Za-z]+(?:\d+[A-Za-z]*|\b)|\'[A-Za-z]+\'|\"(?:[^\"\\\n]|\\\"|\\\\)*\"|[!=<>]=|\|\||&&|[^\s\w\n])'
        for Index in range(0, len(self.Lines)):
            self.Tokenized_Lines[Index] = re.findall(Pattern, self.Lines[Index])
            
        self.Final_List = self.Tokenized_Lines.copy()
        print(self.Final_List)

    def Scan(self):
        self.Scanner_Result = [[[0, 0] for Column in range(len(self.Final_List[Line]))]for Line in range(len(self.Final_List))]
        self.Declared_Variables = []
        for Line in range(0 , len(self.Final_List)):
            for Index in range(0, len(self.Final_List[Line])):
                Flag_Found = False
                for key, value in self.Scanner_List.items():
                    if self.Final_List[Line][Index] == key:
                        
                        self.Scanner_Result[Line][Index][0] = key
                        self.Scanner_Result[Line][Index][1] = value
                        Flag_Found = True
                        break
                    
                if Flag_Found == False:
                    if re.match(r"(['\"])(?:(?=(\\?))\2.)*?\1", self.Final_List[Line][Index]):
                        self.Scanner_Result[Line][Index][0] = self.Final_List[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "String"

                    elif re.match(r'^-?\d+$', self.Final_List[Line][Index]):
                        self.Scanner_Result[Line][Index][0] = self.Final_List[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Integer"

                    elif re.match(r'^-?\d+(\.\d+)?$', self.Final_List[Line][Index]):
                        self.Scanner_Result[Line][Index][0] = self.Final_List[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Float"

                    elif (len(self.Scanner_Result) > 0 and self.Scanner_Result[Line][Index - 1][1] == "Identifiers") or ((len(self.Scanner_Result) > 0 and self.Scanner_Result[Line][Index - 1][1] == "Comma") and self.Scanner_Result[Line][0][1] == "Identifiers"):
                        self.Scanner_Result[Line][Index][0] = self.Final_List[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Variable"
                        self.Declared_Variables.append([self.Final_List[Line][Index], self.Scanner_Result[Line][0][0]])
                        
                    elif (len(self.Scanner_Result) > 0):
                        self.Scanner_Result[Line][Index][0] = self.Final_List[Line][Index]
                        self.Scanner_Result[Line][Index][1] = "Variable"
        self.Final_List = self.Scanner_Result.copy()
        self.Output(self.Scanner_Result.copy())

    def Check_Declarations(self):
        self.Declaration_Erros = self.Final_List.copy()
        for Line in range(0 , len(self.Declaration_Erros)):
            for Index in range(0, len(self.Declaration_Erros[Line])):
                if self.Declaration_Erros[Line][Index][1] == "Variable":
                    Flag_Found = False
                    for Variable_Index in range(0, len(self.Declared_Variables)):
                        if self.Declaration_Erros[Line][Index][0] == self.Declared_Variables[Variable_Index][0]:
                            Flag_Found = True
                            break
                    if Flag_Found == False:
                        self.Declaration_Erros[Line][Index][0] = f"Error: line {Line + 1} variable {self.Final_List[Line][Index][0]} not declared"
                        self.Declaration_Erros[Line][Index][1] = "Error"
        
        self.Final_List = self.Declaration_Erros.copy()
        self.Output(self.Declaration_Erros)

    def Check_String_Syntax(self):
        self.String_Syntax_Check = []
        for Line in range(0 , len(self.Final_List)):
            Temp_Line = []
            flag = False
            for Index in range(0, len(self.Final_List[Line])):
                if flag == True:
                    flag = False
                    continue
                if self.Final_List[Line][Index][1] == "Quotation":
                    if Index + 1 < len(self.Final_List[Line]):
                        Temp_Line.append([f"Error: line {Line + 1} you didn't close quotation marks at the end of {self.Final_List[Line][Index][0] + self.Final_List[Line][Index + 1][0]}", "Error"])
                    else:
                        Temp_Line.append([f"Error: line {Line + 1} you didn't close quotation marks at the end of line: {self.Lines[Line]}", "Error"])
                    flag = True
                else:
                    Temp_Line.append(self.Final_List[Line][Index])
            self.String_Syntax_Check.append(Temp_Line.copy())
        
        self.Final_List = self.String_Syntax_Check.copy()
        self.Output(self.String_Syntax_Check)

    def Check_Semicolon_Syntax(self):
        self.SemiColon_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Final_List)):
            if len(self.Final_List[Line]) > 0:
                if  self.SemiColon_Syntax_Check[Line][0][0] in ["return", "break", "do"] or (self.SemiColon_Syntax_Check[Line][0][1] != "Reserved words" and self.SemiColon_Syntax_Check[Line][0][1] not in ["Open Curly Bracket", "Close Curly Bracket"]):
                    if self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][1] != "Semicolon":
                        self.SemiColon_Syntax_Check[Line].append([f"Error: line {Line + 1} missing semicolon after: {self.Lines[Line]}", "Error"])
                    
                    elif self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][1] == "Semicolon":
                        if len(self.SemiColon_Syntax_Check[Line]) == 1:
                                self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][0] = f"Error: line {Line + 1} you can't write semicolon only in a line"
                                self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][1] = "Error"
                        
                        elif self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 2][1] not in ["Variable", "Integer", "String", "Float", "Boolean", "Error"] and self.SemiColon_Syntax_Check[Line][0][0] not in ["return", "break", "do"]:
                                self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][0] = f"Error: line {Line + 1} you can't write {self.Final_List[Line][len(self.Final_List[Line]) - 2][0]} before semicolon"
                                self.SemiColon_Syntax_Check[Line][len(self.SemiColon_Syntax_Check[Line]) - 1][1] = "Error"

        
        self.Final_List = self.SemiColon_Syntax_Check.copy()
        self.Output(self.SemiColon_Syntax_Check)

    def Check_Variable_Syntax(self):
        self.Variable_Syntax_Check = self.Final_List.copy()

        for Line in range(0 , len(self.Variable_Syntax_Check)):
            for Index in range(0, len(self.Variable_Syntax_Check[Line])):
                
                if self.Variable_Syntax_Check[Line][Index][1] in ["Variable", f"Line {Line + 1} Variable {self.Variable_Syntax_Check[Line][Index][0]} Not Declared"]:
                    if re.match(r"^[a-zA-Z0-9]+$", self.Variable_Syntax_Check[Line][Index][0]):
                            
                        if self.Variable_Syntax_Check[Line][Index - 1][1] not in ["Identifiers", "Operator", "Become", "Open Bracket", "And", "Or", "Less than", "Greater than", "Equal", "Not", "Comma", "Error"] and Index != 0:
                            self.Variable_Syntax_Check[Line][Index - 1][0] = f"Error: line {Line + 1} you should not write {self.Final_List[Line][Index - 1][0]} before variable {self.Final_List[Line][Index][0]}"
                            self.Variable_Syntax_Check[Line][Index - 1][1] = "Error"
                        
                        if self.Variable_Syntax_Check[Line][Index + 1][1] not in ["Operator", "Become", "Close Bracket", "Semicolon", "Open Bracket", "And", "Or", "Less than", "Greater than", "Equal", "Not", "Comma", "Error"]:
                            self.Variable_Syntax_Check[Line][Index + 1][0] = f"Error: line {Line + 1} you should not write {self.Final_List[Line][Index + 1][0]} after variable {self.Final_List[Line][Index][0]}"
                            self.Variable_Syntax_Check[Line][Index + 1][1] = "Error"
                    else:
                        self.Variable_Syntax_Check[Line][Index][0] = f"Error: line {Line + 1} Vaiable name should not contain special characters like that {self.Final_List[Line][Index][0]}"
                        self.Variable_Syntax_Check[Line][Index][1] = "Error"
        
        self.Final_List = self.Variable_Syntax_Check.copy()
        self.Output(self.Variable_Syntax_Check)

    def Check_Identifier_Syntax(self):
        self.Identifier_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Identifier_Syntax_Check)):
            for Index in range(0, len(self.Identifier_Syntax_Check[Line])):
                
                if self.Identifier_Syntax_Check[Line][Index][1] == "Identifiers":
                    if Index == 0:
                        if self.Identifier_Syntax_Check[Line][Index + 1][1] not in ["Variable", "Error"]:
                            self.Identifier_Syntax_Check[Line][Index + 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} or anything after {self.Final_List[Line][Index][0]} or any Identifier but variables"
                            self.Identifier_Syntax_Check[Line][Index + 1][1] = "Error"
                    else:
                        self.Identifier_Syntax_Check[Line][Index][0] = f"Line {Line + 1} You should not write {self.Final_List[Line][Index - 1][0]} or anything before {self.Final_List[Line][Index][0]} or any Identifier"
                        self.Identifier_Syntax_Check[Line][Index + 1][1] = "Error"
        
        self.Final_List = self.Identifier_Syntax_Check.copy()
        self.Output(self.Identifier_Syntax_Check)

    def Check_Become_Syntax(self):
        self.Become_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Become_Syntax_Check)):
            for Index in range(0, len(self.Become_Syntax_Check[Line])):
                
                if self.Become_Syntax_Check[Line][Index][1] == "Become":

                    if self.Become_Syntax_Check[Line][Index - 1][1] not in ["Variable", "Error"]:
                        self.Become_Syntax_Check[Line][Index - 1][0] = f"Error: Line {Line + 1} You can't write {self.Final_List[Line][Index - 1][0]} before {self.Final_List[Line][Index][0]}"
                        self.Become_Syntax_Check[Line][Index - 1][1] = "Error"

                    elif self.Become_Syntax_Check[Line][Index + 1][1] not in ["Variable", "Integer", "Boolean", "String", "Float", "Error"] and self.Become_Syntax_Check[Line][Index + 1][0] != "-":
                        self.Become_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} after {self.Final_List[Line][Index][0]}"
                        self.Become_Syntax_Check[Line][Index + 1][1] = "Error"
                    
                    elif self.Become_Syntax_Check[Line][Index - 1][1] == "Variable" and self.Become_Syntax_Check[Line][Index + 1][1] in  ["Variable", "Integer", "Boolean", "String", "Float"]:
                        if self.Become_Syntax_Check[Line][Index - 1][1] == self.Become_Syntax_Check[Line][Index + 1][1]:
                            for Variable_Index in range(0, len(self.Declared_Variables)):
                                if self.Become_Syntax_Check[Line][Index - 1][0] == self.Declared_Variables[Variable_Index][0]:
                                    flag_found = False
                                    for Variable_Index2 in range(0, len(self.Declared_Variables)):
                                        if self.Become_Syntax_Check[Line][Index + 1][0] == self.Declared_Variables[Variable_Index2][0]:
                                            if self.Declared_Variables[Variable_Index][1] == self.Declared_Variables[Variable_Index2][1]:
                                                flag_found = True
                                                break
                                    if flag_found:
                                        break
                        else:
                            for Variable_Index in range(0, len(self.Declared_Variables)):
                                if self.Become_Syntax_Check[Line][Index - 1][0] == self.Declared_Variables[Variable_Index][0]:
                                    if (self.Become_Syntax_Check[Line][Index + 1][1] == "Integer" and self.Declared_Variables[Variable_Index][1] in ["int", "float", "double"]) or (self.Become_Syntax_Check[Line][Index + 1][1] == "Float" and self.Declared_Variables[Variable_Index][1] in ["float", "double"]) or (self.Become_Syntax_Check[Line][Index + 1][1] == "String" and self.Declared_Variables[Variable_Index][1] in ["char", "string"]) or (self.Become_Syntax_Check[Line][Index + 1][1] == "Boolean" and self.Declared_Variables[Variable_Index][1] == "bool"):
                                        break
                                    else:
                                        self.Become_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't assign {self.Final_List[Line][Index + 1][0]} ({self.Become_Syntax_Check[Line][Index + 1][1]}) to a varaible ({self.Declared_Variables[Variable_Index][0]}) of type {self.Declared_Variables[Variable_Index][1]}"
                                        self.Become_Syntax_Check[Line][Index + 1][1] = "Error"
                                    
        
        self.Final_List = self.Become_Syntax_Check.copy()
        self.Output(self.Become_Syntax_Check)

    def Check_Condition_Syntax(self):
        self.Condition_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Condition_Syntax_Check)):
            for Index in range(0, len(self.Condition_Syntax_Check[Line])):
                
                if self.Condition_Syntax_Check[Line][Index][1] in ["And", "Or", "Less than", "Greater than", "Greater Equal", "Less Equal", "Not Equal", "Equal", "Not"]:
                    print(self.Condition_Syntax_Check[Line][0][0])
                    if self.Condition_Syntax_Check[Line][0][0] in ["while", "case"]:
                        if self.Condition_Syntax_Check[Line][Index - 1][1] not in ["Variable", "Integer", "Boolean", "String", "Float", "Error"]:
                            self.Condition_Syntax_Check[Line][Index - 1][0] = f"Error: Line {Line + 1} You can't write {self.Final_List[Line][Index - 1][0]} before {self.Final_List[Line][Index][0]}"
                            self.Condition_Syntax_Check[Line][Index - 1][1] = "Error"

                        elif self.Condition_Syntax_Check[Line][Index + 1][1] not in ["Variable", "Integer", "Boolean", "String", "Float", "Error"] and self.Become_Syntax_Check[Line][Index + 1][0] != "-":
                            self.Condition_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} after {self.Final_List[Line][Index][0]}"
                            self.Condition_Syntax_Check[Line][Index + 1][1] = "Error"
                        
                        elif self.Condition_Syntax_Check[Line][Index - 1][1] == "Variable" and self.Condition_Syntax_Check[Line][Index + 1][1] in  ["Variable", "Integer", "Boolean", "String", "Float"]:
                            if self.Condition_Syntax_Check[Line][Index - 1][1] == self.Condition_Syntax_Check[Line][Index + 1][1]:
                                for Variable_Index in range(0, len(self.Declared_Variables)):
                                    if self.Condition_Syntax_Check[Line][Index - 1][0] == self.Declared_Variables[Variable_Index][0]:
                                        flag_found = False
                                        for Variable_Index2 in range(0, len(self.Declared_Variables)):
                                            if self.Condition_Syntax_Check[Line][Index + 1][0] == self.Declared_Variables[Variable_Index2][0]:
                                                if self.Declared_Variables[Variable_Index][1] == self.Declared_Variables[Variable_Index2][1]:
                                                    flag_found = True
                                                    break
                                        if flag_found:
                                            break
                                        else:
                                            self.Condition_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't Compare a variable {self.Final_List[Line][Index + 1][0]} ({self.Declared_Variables[Variable_Index2][1]}) to a varaible ({self.Declared_Variables[Variable_Index][0]}) of type {self.Declared_Variables[Variable_Index][1]}"
                                            self.Condition_Syntax_Check[Line][Index + 1][1] = "Error"
                            else:
                                for Variable_Index in range(0, len(self.Declared_Variables)):
                                    if self.Condition_Syntax_Check[Line][Index - 1][0] == self.Declared_Variables[Variable_Index][0]:
                                        if (self.Condition_Syntax_Check[Line][Index + 1][1] == "Integer" and self.Declared_Variables[Variable_Index][1] in ["int", "float", "double"]) or (self.Condition_Syntax_Check[Line][Index + 1][1] == "Float" and self.Declared_Variables[Variable_Index][1] in ["float", "double"]) or (self.Become_Syntax_Check[Line][Index + 1][1] == "String" and self.Declared_Variables[Variable_Index][1] in ["char", "string"]) or (self.Become_Syntax_Check[Line][Index + 1][1] == "Boolean" and self.Declared_Variables[Variable_Index][1] == "bool"):
                                            break
                                        else:
                                            self.Condition_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't Compare {self.Final_List[Line][Index + 1][0]} ({self.Condition_Syntax_Check[Line][Index + 1][1]}) to a varaible ({self.Declared_Variables[Variable_Index][0]}) of type {self.Declared_Variables[Variable_Index][1]}"
                                            self.Condition_Syntax_Check[Line][Index + 1][1] = "Error"
                    else:
                        self.Condition_Syntax_Check[Line][Index + 1][0] = f"Error: Line {Line + 1} You can't write a condition in this line {self.Lines[Line]} without while or case at the start"
                        self.Condition_Syntax_Check[Line][Index + 1][1] = "Error"
        self.Final_List = self.Become_Syntax_Check.copy()
        self.Output(self.Become_Syntax_Check)

    def Check_Operator_Syntax(self):
        self.Operator_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Operator_Syntax_Check)):
            for Index in range(0, len(self.Operator_Syntax_Check[Line])):
                
                if self.Operator_Syntax_Check[Line][Index][1] == "Operator":

                    if self.Operator_Syntax_Check[Line][Index - 1][1] not in ["Variable", "Close Bracket", "Integer", "Float", "Error"] and self.Operator_Syntax_Check[Line][Index][0] != '-':
                        self.Operator_Syntax_Check[Line][Index - 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index - 1][0]} before {self.Final_List[Line][Index][0]}"
                        self.Operator_Syntax_Check[Line][Index - 1][1] = "Error"

                    elif self.Operator_Syntax_Check[Line][Index + 1][1] not in ["Variable", "Open Bracket", "Integer", "Float" "Error"]:
                        self.Operator_Syntax_Check[Line][Index + 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} after {self.Final_List[Line][Index][0]}"
                        self.Operator_Syntax_Check[Line][Index + 1][1] = "Error"
        
        self.Final_List = self.Operator_Syntax_Check.copy()
        self.Output(self.Operator_Syntax_Check)
    
    def Check_Integer_Syntax(self):
        self.Integer_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.Integer_Syntax_Check)):
            for Index in range(0, len(self.Integer_Syntax_Check[Line])):
                
                if self.Integer_Syntax_Check[Line][Index][1] in ["Integer", "Float"]:

                    if Index - 1 > 0 and self.Integer_Syntax_Check[Line][Index - 1][1] not in ["Operator", "Open Bracket", "Become", "And", "Or", "Less than", "Greater than",  "Greater Equal", "Less Equal", "Not Equal", "Become", "Equal", "Not", "Error"] and self.Integer_Syntax_Check[Line][Index - 1][0] != "case":
                        self.Integer_Syntax_Check[Line][Index - 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index - 1][0]} before {self.Final_List[Line][Index][0]}"
                        self.Integer_Syntax_Check[Line][Index - 1][1] = "Error"

                    elif Index + 1 < len(self.Integer_Syntax_Check[Line]) and self.Integer_Syntax_Check[Line][Index + 1][1] not in ["Operator", "Close Bracket", "Semicolon", "Comma", "And", "Or", "Less than", "Greater than",  "Greater Equal", "Less Equal", "Not Equal", "Become", "Equal", "Not", "colon", "Error"]:
                        self.Integer_Syntax_Check[Line][Index + 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} after {self.Final_List[Line][Index][0]}"
                        self.Integer_Syntax_Check[Line][Index + 1][1] = "Error"
        
        self.Final_List = self.Integer_Syntax_Check.copy()
        self.Output(self.Integer_Syntax_Check)

    def Advanced_Check_String_Syntax(self):
        self.String_Syntax_Check = self.Final_List.copy()
        for Line in range(0 , len(self.String_Syntax_Check)):
            for Index in range(0, len(self.String_Syntax_Check[Line])):
                
                if self.String_Syntax_Check[Line][Index][1] == "String" and Index != 0:

                    if self.String_Syntax_Check[Line][Index - 1][1] not in ["Open Bracket", "Become", "Error"]:
                        self.String_Syntax_Check[Line][Index - 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index - 1][0]} before {self.Final_List[Line][Index][0]}"
                        self.String_Syntax_Check[Line][Index - 1][1] = "Error"

                    elif self.String_Syntax_Check[Line][Index + 1][1] not in ["Close Bracket", "Semicolon", "Comma", "Error"]:
                        self.String_Syntax_Check[Line][Index + 1][0] = f"Line {Line + 1} You can't write {self.Final_List[Line][Index + 1][0]} after {self.Final_List[Line][Index][0]}"
                        self.String_Syntax_Check[Line][Index + 1][1] = "Error"
        
        self.Final_List = self.String_Syntax_Check.copy()
        self.Output(self.String_Syntax_Check)

    def Check_While_Syntax(self):
        self.While_Syntax_Check = self.Final_List.copy()
        counter=0
        flag=False
        order_list=['while','(',')','{' ,'}']
        for i in range(0,len(self.Final_List)):
            for k in range(len(self.Final_List[i])):
                if self.While_Syntax_Check[i][k][0] == 'while' and order_list[counter] == 'while':
                    counter += 1
                    flag=True
                elif self.While_Syntax_Check[i][k][0] == '(' and order_list[counter] == '(':
                        counter += 1
                elif self.While_Syntax_Check[i][k][0] == ')' and order_list[counter] == ')':
                        counter += 1
                elif self.While_Syntax_Check[i][k][0] == '{' and order_list[counter] == '{':
                        counter += 1
                elif self.While_Syntax_Check[i][k][0] == '}' and order_list[counter] == '}':
                        counter += 1
        if counter != len(order_list) and flag==True:
            self.While_Syntax_Check[len(self.While_Syntax_Check)-1].append(['Error in while loop  ',"Syntax Error: Missing or misplaced token."])
        
        self.Final_List = self.While_Syntax_Check.copy()
        self.Output(self.While_Syntax_Check)

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

        for i in range(len(self.Final_List)):
            for k in range(len(self.Final_List[i])):
                token = self.Final_List[i][k][0]

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
        for i in range (len(self.Final_List)):
            for k in range(len(self.Final_List[i])):
                if(self.Final_List[i][k][0] == 'default'):
                        default_holder=i
        for i in range(len(self.Final_List)):
            for k in range (len(self.Final_List[i])):
                if (self.Final_List[i][k][0] == 'case'):
                    case_holder=i 
        if flag and (counter !=len(order_list)):
            self.Final_List[len(self.Final_List) - 1].append(['Error in switch', 'Syntax Error: invalid syntax of switch '])
        if(case_holder > default_holder and default_counter > 0):
            self.Final_List[len(self.Final_List) - 1].append(['Error in switch', 'Syntax Error: Missing case after default  ' ])

        elif flag_case==True and  case_counter != break_counter:
            self.Final_List[len(self.Final_List) - 1].append(['Error in switch', 'Syntax Error: The structure of switch is not correct   '])
            # print('flag case',flag_case, " flag switch" , flag)

        # elif flag and (counter != len(order_list) or switch_counter != 1 or  default_counter != 1  or case_counter != colon_counter - 1 ):
        #     print('error 2')
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing or misplaced token.'])
        
        elif flag and (case_counter != colon_counter - 1):
            self.Final_List[len(self.Final_List) - 1].append(['Error in switch', 'Syntax Error: invalid syntax of colon ' ])
        elif flag_case==True and flag==False or case_counter != break_counter:
            self.Final_List[len(self.Final_List) - 1].append(['Error in switch', 'Syntax Error: Missing switch '+str(0)])
        # if flag and (counter != len(order_list) or switch_counter != 1 or  default_counter != 1  or case_counter != colon_counter - 1 ):
        #     print('error 2')
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing or misplaced token.'])
        # if flag_case==True and  case_counter != break_counter:
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing break or case at line '])
        #     # print('flag case',flag_case, " flag switch" , flag)
        # if flag_case==True and flag==False or case_counter != break_counter:
        #     self.Scanner_Result[len(self.Scanner_Result) - 1].append(['Error in switch', 'Syntax Error: Missing switch '+str(0)])
        #     print('flag case',flag_case, " flag switch" , flag)

        self.Output(self.Final_List)

    def Check_Syntax(self):
        self.Check_Semicolon_Syntax()
        self.Check_Variable_Syntax()
        self.Check_Identifier_Syntax()
        self.Check_Become_Syntax()
        self.Check_Condition_Syntax()
        self.Check_Operator_Syntax()
        self.Check_Integer_Syntax()
        self.Advanced_Check_String_Syntax()
        self.Check_While_Syntax()
        self.switch_check()

    def Show_Results(self):
        print("Lines Inputs = " + str(self.Tokenized_Lines))
        print("Scanner Results = " + str(self.Scanner_Result))
        print("String Errors = " + str(self.String_Syntax_Check) )
        print("Declared Variables = " + str(self.Declared_Variables))
        print("Declaration Errors = " + str(self.Declaration_Erros))
        print("SemiColon Errors = " + str(self.SemiColon_Syntax_Check))
        print("Syntax Errors = " + str(self.Variable_Syntax_Check))
        print("While Errors = " + str(self.While_Syntax_Check))

    def Output(self, List):
        self.Output_Area.configure(state="normal")
        self.Output_Area.delete(1.0, tk.END)
        self.Output_Area.insert(tk.END, '\n'.join([f"{column[0]} -> {column[1]}" for row in List for column in row]))
        self.Output_Area.configure(state="disabled")

Scanner_List = {"int" : "Identifiers", "float" : "Identifiers", "string" : "Identifiers", "double" : "Identifiers",
"bool" : "Identifiers", "char" : "Identifiers", "+" : "Operator", "-" : "Operator", "/" : "Operator", 
"%" : "Operator", "*" : "Operator", "(" : "Open Bracket", ")" : "Close Bracket", "{" : "Open Curly Bracket", 
"}" : "Close Curly Bracket", "," : "Comma", ";"  : "Semicolon", "&&" : "And", "||"  : "Or", "<" : "Less than", 
">" : "Greater than", "=" : "Become", "==" : "Equal", "!" : "Not", ">=" : "Greater Equal", "<=" : "Less Equal", "!=" : "Not Equal", "for" : "Reserved words", "while" : "Reserved words", 
"if" : "Reserved words", "do" : "Reserved words", "return" : "Reserved words", "break" : "Reserved words", 
"continue" : "Reserved words", "end" : "Reserved words", "'" : "Quotation", '"': "Quotation", ".": "Dot", "switch": "Reserved words", "case": "Reserved words", "default": "Reserved words", ":": "colon", "true": "Boolean", "false": "Boolean"}

Main1 = Main(root, Scanner_List)
Main1.GUI()

root.mainloop()