import csv
from Tkinter import *
import Tkinter as ttk 
from ttk import *
import operator
import tkMessageBox

root = Tk()
root.title("Unit Converter")
root.geometry("380x100")
#Variables declared
units_optionmenu = StringVar() #OptionMenu, get all category.
unitselection_from = StringVar() 
unitselection_to = StringVar()
input_value = StringVar() #Initial value
Results = StringVar()

def get_units_1(*args): #From | unitselection_from
    match = units_optionmenu.get()
    reader = csv.reader(open('units.csv', 'rb', ))
    units_1 = [""]
    units_2 = [""]
    input_value.set("Enter value here")
    Results.set("")
    Button(root, text="Convert", command=Convert, width=20).grid(row=4, column=2, sticky=E)
    for num, row in enumerate(reader):
        if match in row[0]:
            units_1.append(row[1])
            units_2.append(row[1])
            dropdowns_1 = OptionMenu(root, unitselection_from, *units_1) 
            unitselection_from.set("From")
            dropdowns_1.grid(column=1, row=3, sticky=W)
            dropdowns_1.config(width=20)
            dropdowns_2 = OptionMenu(root, unitselection_to, *units_2) 
            unitselection_to.set("To")
            dropdowns_2.grid(column=2, row=3, sticky=E)
            dropdowns_2.config(width=20)

def Convert():
    checktemp = units_optionmenu.get()
    formula_to_base = unitselection_from.get() #Dropdown FROM
    formula_to_convert = unitselection_to.get() #Dropdown TO
    if checktemp != "Temperature":
        if formula_to_convert != "To":
            try:
                user_input_value = float(input_value.get()) #Get textbox value
                reader = csv.reader(open('units.csv', 'rb', ))
                for num, row in enumerate(reader):  
                    if formula_to_base in row[1]:
                        formula_to_base = row[3]
                        operators_base = row[2] #Operator to BASE value
                        break
                reader = csv.reader(open('units.csv', 'rb', )) 
                for num, row in enumerate(reader):
                    if formula_to_convert in row[1]:
                        formula_to_convert = row[3]
                        operator_convert = row[5]
                        break
                formula_to_base = float(formula_to_base)
                formula_to_convert = float(formula_to_convert)
                ops = {"+": operator.add,
                       "-": operator.sub,
                       "*": operator.mul,
                       "/": operator.div}
                op_base = ops[operators_base] #Operators that convert input to set BASE 
                op_conv = ops[operator_convert] #Convert to output
                conv_to_baseunit = float(op_base(user_input_value, formula_to_base)) #Change to initial base of respective unit
                conv_to_baseunit = float(conv_to_baseunit)
                post_result = op_conv(conv_to_baseunit, formula_to_convert)
                Results.set("= %s" %format(post_result))
            except Exception: 
                tkMessageBox.showerror("Unit Converter", "Invalid input / choice")
        else:
            tkMessageBox.showerror("Unit Converter", "Invalid input / choice")
    else:
        temperature()

def temperature():
    formula_to_base = unitselection_from.get() #Dropdown FROM
    formula_to_convert = unitselection_to.get() #Dropdown TO
    try:
        user_input_value = float(input_value.get())
        if formula_to_base == "Kelvin":
            to_Celsius = user_input_value - 273.15
        elif formula_to_base == "Fahrenheit":
            to_Celsius = (user_input_value-32)*5/9
        elif formula_to_base == "Celsius":
            to_Celsius = user_input_value

        if formula_to_convert == "Fahrenheit":
            post_result = (to_Celsius*9/5)+32
        elif formula_to_convert == "Celsius":
            post_result = to_Celsius
        elif formula_to_convert == "Kelvin":
            post_result = to_Celsius+273.15
        Results.set("= %s" %format(post_result))
    except Exception: 
        tkMessageBox.showerror("Unit Converter", "Invalid input / choice")

#Read type unit from units.csv
reader = csv.reader(open('units.csv', 'rb', ))
units = [""] #Array
for num, row in enumerate(reader):
    if row[0] in units:
        continue
    else:
        units.append(row[0])
        dropdown = OptionMenu(root, units_optionmenu, command=get_units_1, *units) 
        units_optionmenu.set("Select Conversion method")
        dropdown.grid(column=1, row=0)
        dropdown.config(width=30)

Entry(root, textvariable=input_value, width=25).grid(row=1, column=1, sticky=W)
Entry(root, textvariable=Results, width=25).grid(row=1, column=2, sticky=E)

root.mainloop()