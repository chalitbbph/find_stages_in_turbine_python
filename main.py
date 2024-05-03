import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import pandas as pd
import blade
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
     FigureCanvasTkAgg)
import numpy as np
from pyXSteam.XSteam import XSteam
import cal_part
import table_output
import lxml
import openpyxl

FONT = "arial"
COLOR= "White"
UNIT_P=["BarA","BarG","psiG","kPaG","kg/cm^2G"]
UNIT_T=["Degree C","Degree F","Degree K"]
UNIT_F=["Kgs/Hr","lb/Hr",'Tons/Hr']
UNIT_D=["mm","Inches"]
UNIT_DS=["RPM"]

root = Tk()
root.title("Stages Caculator")

root.geometry("1200x680")
root.resizable(True, True)
root.config(bg=COLOR)

steam_table = XSteam(XSteam.UNIT_SYSTEM_FLS)

pd.options.display.float_format = '{:.5f}'.format


##-------------------------------------------switch frame func-------------------------------------##

def show_page(frame):
    frame.tkraise()

page_1=Frame(root,bg=COLOR)
page_2=Frame(root,bg=COLOR)


for frame in (page_1,page_2):
    frame.grid(row=0,column=0,sticky='nsew')


##-------------------------------------------UI frame1-------------------------------------##

title_frame = Frame(page_1,bg=COLOR)
input_frame = Frame(page_1,bg=COLOR)
process_frame = Frame(page_1,bg=COLOR)
output_frame = Frame(page_1,bg=COLOR)
output_frame_btn =Frame(page_1,bg=COLOR)
power_frame = Frame(page_1,bg=COLOR)
power_frame_out = Frame(page_1,bg=COLOR)
cp_frame = Frame(page_1,bg=COLOR)


title_frame.pack(pady=5)
input_frame.pack(pady=5)
process_frame.pack(pady=5)
output_frame.pack(pady=5)
output_frame_btn.pack(pady=5)
power_frame.pack(pady=5)
power_frame_out.pack(pady=5)
cp_frame.pack(pady=5)



##-------------------------------------------finding val-------------------------------------##


def put_values():

    try:
        inlet_pressure = float(entry_inlet.get())
        outlet_pressure = float(entry_outlet.get())
        temperature = float(entry_temp.get())
        design_speed = float(entry_design_speed.get())
        diameter = float(entry_diameter.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter numeric values for all input fields.")
        return

    if not all([inlet_pressure, outlet_pressure, temperature, design_speed, diameter]):
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return

#-------------------------------------convert-------------------------------------------#

    val_d_ft = cal_part.convert_diameter(diameter,d_combo.get())
    val_t_f = cal_part.convert_to_fahrenheit(temperature,t_combo.get())
    val_pi = cal_part.convert_to_psi(inlet_pressure,p_combo.get())
    val_po = cal_part.convert_to_psi(outlet_pressure, p_o_combo.get())
    val_f = cal_part.unit_ib(float(entry_flow.get()),f_combo.get())
    entropy = steam_table.s_pt(val_pi,val_t_f)
    enthalpy_in = steam_table.h_ps(val_pi,entropy)
    enthalpy_out = steam_table.h_ps(val_po, entropy)
    blade_enthalpy = blade.calculate_h_in_btu(design_speed,val_d_ft)
    enthalpy_diff = enthalpy_in - enthalpy_out
    stages = float(enthalpy_diff/blade_enthalpy)
    power_t =table_output.entropy_to_power(enthalpy_diff,val_f)


    entry_entropy.delete(0, END)
    entry_entropy.insert(0, entropy)
    entry_enthalpy_inlet.delete(0, END)
    entry_enthalpy_inlet.insert(0, enthalpy_in)
    entry_enthalpy_out.delete(0, END)
    entry_enthalpy_out.insert(0, enthalpy_out)
    entry_enthalpy_diff.delete(0, END)
    entry_enthalpy_diff.insert(0, enthalpy_diff)
    entry_stage.delete(0,END)
    entry_stage.insert(0,stages)
    entry_power.delete(0,END)
    entry_power.insert(0,power_t)


##-------------------------------------------table funtion-------------------------------------------##

def values_first_stage():
    entropy = float(entry_entropy.get())
    inlet_pressure = float(entry_inlet.get())
    outlet_pressure = float(entry_outlet.get())
    inlet_temperature = float(entry_temp.get())



    enthalpy_inlet = float(entry_enthalpy_inlet.get())
    enthalpy_out = float(entry_enthalpy_out.get())
    stage_f = int(entry_stage_f.get())
    design_speed = float(entry_design_speed.get())
    h_diff = float(table_output.diff_h(enthalpy_inlet,enthalpy_out,stage_f))
    d = float(blade.diameter_feet(design_speed,h_diff))
    h_ideal = table_output.entholpy_idea(enthalpy_inlet,h_diff)
    h_actual = table_output.entholpy_actual(enthalpy_inlet,h_diff)
    p_i = cal_part.convert_to_psi(inlet_pressure,p_combo.get())
    p_1 = steam_table.p_hs(h_ideal,entropy)
    t_i = cal_part.convert_to_fahrenheit(inlet_temperature,t_combo.get())
    t_1 = steam_table.t_ph(p_1,h_actual)
    s_1 = steam_table.s_ph(p_1,h_actual)
    v_1 = steam_table.v_ph(p_1,h_actual)
    v_in =steam_table.v_pt(inlet_pressure,inlet_temperature)

    p_o = cal_part.convert_to_psi(outlet_pressure,p_o_combo.get())
    h_o  = steam_table.h_ps(p_o, entropy)
    power_t  = table_output.entropy_to_power(h_diff,cal_part.unit_ib(float(entry_flow.get()),f_combo.get()))
    return p_i,p_1,t_i,t_1,enthalpy_inlet,h_ideal,h_actual,entropy,s_1,v_in,v_1,d,p_o,h_o,h_diff,power_t


def create_table():
    pd.set_option('display.max_columns', None)
    design_speed = float(entry_design_speed.get())
    arr = values_first_stage()
    stages = int(entry_stage_f.get())
    stage = [f'Stage {i+1}'for i in range(stages)]
    dict = {}
    dict['Stage 1'] = arr

    for i in range(stages-1):
        list = []
        p_i = dict[f'Stage {i+1}'][1]
        t_i = dict[f'Stage {i+1}'][3]
        h_i = dict[f'Stage {i+1}'][6]
        s_i = dict[f'Stage {i+1}'][8]
        v_in = dict[f'Stage {i+1}'][10]

        p_o = dict[f'Stage {i+1}'][12]
        h_o = steam_table.h_ps(p_o,s_i)
        h_diff_among = h_i-h_o
        stage_left = stages - (i+1)
        h_diff = float(h_diff_among/stage_left)
        h_ideal = table_output.entholpy_idea(h_i,h_diff)
        h_actual = table_output.entholpy_actual(h_i,h_diff)
        d = blade.diameter_feet(design_speed, h_diff )

        p_1 = steam_table.p_hs(h_ideal,s_i)
        t_1 = steam_table.t_ph(p_1,h_actual)
        s_1 = steam_table.s_ph(p_1,h_actual)
        v_1 = steam_table.v_ph(p_1,h_actual)
        power = table_output.entropy_to_power(h_diff,cal_part.unit_ib(float(entry_flow.get()),f_combo.get()))
        list.extend(( p_i,p_1,t_i,t_1,h_i,h_ideal,h_actual,s_i,s_1,v_in,v_1,d,p_o,h_o,h_diff,power))
        dict[f'Stage {i+2}'] = list
    df = pd.DataFrame(dict,columns=stage, index=table_output.main_row)
    df.to_excel('80%_eff.xlsx', sheet_name='Stage in 80% efficiency')
    print(df)
    tkinter.messagebox.showinfo('Create steam stage','Success!')


##--------------------------------------------power outout--------------------------------------##

def gen_p():

    ml = float(entry_ml.get())
    gb = float(entry_gb.get())
    al = float(entry_al.get())
    mg = (100 - (float(entry_mg.get()))) *0.01
    pw = float(entry_power.get())

    pwml = pw-ml
    pwgl = pwml * gb *al *mg


    entry_gpt.delete(0,END)
    entry_gpt.insert(0,pwgl)






##----------------------------------------------------------------------------------##
label_Title = Label(title_frame,text="80% Effiency,0.46 Ratio Speed",font=FONT,fg="black",bg=COLOR)
label_Title.pack()

##----------------------------------------------------------------------------------##

label_inlet = Label(input_frame,text="Inlet Pressure: ",font=FONT,fg="black",bg=COLOR)
label_outlet = Label(input_frame,text="Outlet Pressure: ",font=FONT,fg="black",bg=COLOR)
label_temp=Label(input_frame,text="Temperature: ",font=FONT,fg="black",bg=COLOR)
label_flow = Label(input_frame,text="Flow: ",font=FONT,fg="black",bg=COLOR)
label_diameter = Label(input_frame,text="Diameter: ",font=FONT,fg="black",bg=COLOR)
label_design_speed = Label(input_frame,text="Design Speed: ",font=FONT,fg="black",bg=COLOR)


entry_inlet = Entry(input_frame,width=10,font=FONT)
entry_temp = Entry(input_frame,width=10,font=FONT)
entry_outlet = Entry(input_frame,width=10,font=FONT)
entry_flow = Entry(input_frame,width=10,font=FONT)
entry_diameter = Entry(input_frame,width=10,font=FONT)
entry_design_speed = Entry(input_frame,width=10,font=FONT)


p_combo = ttk.Combobox(input_frame,value=UNIT_P,font=FONT,width=10)
p_combo.set("BarG")
p_o_combo = ttk.Combobox(input_frame,value=UNIT_P,font=FONT,width=10)
p_o_combo.set("BarG")
t_combo = ttk.Combobox(input_frame,value=UNIT_T,font=FONT,width=10)
t_combo.set("Degree C")
f_combo = ttk.Combobox(input_frame,value=UNIT_F,font=FONT,width=10)
f_combo.set("Kgs/Hrs")
d_combo = ttk.Combobox(input_frame,value=UNIT_D,font=FONT,width=10)
d_combo.set("Inches")
ds_combo = ttk.Combobox(input_frame,value=UNIT_DS,font=FONT,width=10)
ds_combo.set("RPM")


label_inlet.grid(row=0,column=0,sticky="W")
entry_inlet.grid(row=0,column=1)
p_combo.grid(row=0,column=2)

label_temp.grid(row=1,column=0,sticky="W")
entry_temp.grid(row=1,column=1)
t_combo.grid(row=1,column=2)


label_outlet.grid(row=2,column=0,sticky='W')
entry_outlet.grid(row=2,column=1)
p_o_combo.grid(row=2,column=2)


label_flow.grid(row=3,column=0,sticky='W')
entry_flow.grid(row=3,column=1)
f_combo.grid(row=3,column=2)

label_diameter.grid(row=4,column=0,sticky='W')
entry_diameter.grid(row=4,column=1)
d_combo.grid(row=4,column=2)

label_design_speed.grid(row=5,column=0,sticky='W')
entry_design_speed.grid(row=5,column=1)
ds_combo.grid(row=5,column=2)

##-----------------------------------------------##

btn_cal = Button(process_frame,text="Calculate",font=FONT,command=put_values)
btn_cal.grid(row=0,column=0,ipadx=150)
##-----------------------------------------------##

label_entropy = Label(output_frame,text="Entropy  : ",font=FONT,fg="black",bg=COLOR)
entry_entropy = Entry(output_frame,width=15,font=FONT)
label_entropy_unit = Label(output_frame,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)


label_enthalpy_inlet = Label(output_frame,text="Enthalpy Input :",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_inlet = Entry(output_frame,width=15,font=FONT)
label_enthalpy_unit_inlet = Label(output_frame,text="Btu /ibm",font=FONT,fg="black",bg=COLOR)

label_enthalpy_out = Label(output_frame,text="Enthalpy Outlet : ",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_out = Entry(output_frame,width=15,font=FONT)
label_enthalpy_unit_out = Label(output_frame,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)

label_enthalpy_diff = Label(output_frame,text="Differential Enthalpy : ",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_diff = Entry(output_frame,width=15,font=FONT)
label_enthalpy_unit_diff = Label(output_frame,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)


label_stage = Label(output_frame,text="Number Of Stages :",font=FONT,fg="black",bg=COLOR)
entry_stage = Entry(output_frame,width=15,font=FONT)
label_stage_unit = Label(output_frame,text="   stages ",font=FONT,fg="black",bg=COLOR)


label_stage_f = Label(output_frame,text="Number Of Stages :",font=FONT,fg="black",bg=COLOR)
entry_stage_f = Entry(output_frame,width=15,font=FONT,bg='gray')
label_stage_unit_f = Label(output_frame,text="   stages ",font=FONT,fg="black",bg=COLOR)


label_power = Label(output_frame,text="Power Turbine:",font=FONT,fg="black",bg=COLOR)
entry_power = Entry(output_frame,width=15,font=FONT)
label_power_unit = Label(output_frame,text="   BTU/Hrs ",font=FONT,fg="black",bg=COLOR)


label_entropy.grid(row=0,column=0,sticky='W')
entry_entropy.grid(row=0,column=1)
label_entropy_unit.grid(row=0,column=2)

label_enthalpy_inlet.grid(row=1,column=0,sticky='W')
entry_enthalpy_inlet.grid(row=1,column=1)
label_enthalpy_unit_inlet.grid(row=1,column=2)

label_enthalpy_out.grid(row=2,column=0,sticky='W')
entry_enthalpy_out.grid(row=2,column=1)
label_enthalpy_unit_out.grid(row=2,column=2)

label_enthalpy_diff.grid(row=3,column=0,sticky='W')
entry_enthalpy_diff.grid(row=3,column=1)
label_enthalpy_unit_diff.grid(row=3,column=2)

label_stage.grid(row=4,column=0,sticky='W')
entry_stage.grid(row=4,column=1)
label_stage_unit.grid(row=4,column=2)

label_stage_f.grid(row=5,column=0,sticky='W')
entry_stage_f.grid(row=5,column=1)
label_stage_unit_f.grid(row=5,column=2)

label_power.grid(row=6,column=0,sticky='W')
entry_power.grid(row=6,column=1)
label_power_unit.grid(row=6,column=2)

##-----------------------------------------------##

label_cal_each_stage = Label(output_frame_btn,text="Find each stage values:",font=FONT,fg="black",bg=COLOR)
label_cal_each_stage.grid(row=0,column=0,padx=0)

btn_cal_each_stage = Button(output_frame_btn,text="Calculate",font=FONT,command=create_table)
btn_cal_each_stage.grid(row=0,column=1,ipadx=65)



##-----------------------------------------------##

label_ml = Label(power_frame,text="Mechanical Loss:",font=FONT,fg="black",bg=COLOR)
entry_ml = Entry(power_frame,width=15,font=FONT)
label_et1 = Label(power_frame,text="      " ,bg=COLOR)

label_gb = Label(power_frame,text="Gear Box eff.:",font=FONT,fg="black",bg=COLOR)
entry_gb = Entry(power_frame,width=15,font=FONT)
label_et2 = Label(power_frame,text="      ",bg=COLOR)

label_al = Label(power_frame,text="Alternator eff.:",font=FONT,fg="black",bg=COLOR)
entry_al = Entry(power_frame,width=15,font=FONT)
label_et3 = Label(power_frame,text="      ",bg=COLOR)

label_mg = Label(power_frame,text="Margin:",font=FONT,fg="black",bg=COLOR)
entry_mg = Entry(power_frame,width=15,font=FONT)
label_et4 = Label(power_frame, text="      ", bg=COLOR)

label_ml.grid(row=0,column=0,sticky='W',ipadx=3)
entry_ml.grid(row=0,column=1,ipadx=20)
label_et1.grid(row=0,column=2)


label_gb.grid(row=1,column=0,sticky='W',ipadx=3)
entry_gb.grid(row=1,column=1,ipadx=20)
label_et2.grid(row=1,column=2)

label_al.grid(row=2,column=0,sticky='W',ipadx=3)
entry_al.grid(row=2,column=1,ipadx=20)
label_et3.grid(row=2,column=2)

label_mg.grid(row=3,column=0,sticky='W',ipadx=3)
entry_mg.grid(row=3,column=1,ipadx=20)
label_et4.grid(row=3,column=2)

##-----------------------------------------------##


label_power = Label(power_frame,text="Find Power Generator:",font=FONT,fg="black",bg=COLOR)
label_power.grid(row=4,column=0,padx=3)

btn_cal_power = Button(power_frame,text="Calculate",font=FONT,command= gen_p)
btn_cal_power.grid(row=4,column=1,ipadx=63)


label_gpt = Label(power_frame_out,text="Generator Power:",font=FONT,fg="black",bg=COLOR)
entry_gpt = Entry(power_frame_out,width=15,font=FONT)
label_gptu = Label(power_frame_out,text="BTU/Hrs ",font=FONT,fg="black",bg=COLOR)


label_gpt.grid(row=0,column=0,sticky='W',ipadx=5)
entry_gpt.grid(row=0,column=1,padx=10)
label_gptu.grid(row=0,column=2,padx=10)

##------------------------UI frame2-----------------------##

title_frame2 = Frame(page_2,bg=COLOR)
input_frame2 = Frame(page_2,bg=COLOR)
process_frame2 = Frame(page_2,bg=COLOR)
output_frame2 = Frame(page_2,bg=COLOR)
output_frame_btn2 =Frame(page_2,bg=COLOR)
power_frame2 = Frame(page_2,bg=COLOR)
power_frame_out2 = Frame(page_2,bg=COLOR)
cp_frame2 = Frame(page_2,bg=COLOR)

title_frame2.pack(pady=5)
input_frame2.pack(pady=5)
process_frame2.pack(pady=5)
output_frame2.pack(pady=5)
output_frame_btn2.pack(pady=5)
power_frame2.pack(pady=5)
power_frame_out2.pack(pady=5)
cp_frame2.pack(pady=5)



#------------------------------------------------frame2---------------------------------------#


#------------------------------------------------val output---------------------------------------#
def put_values2():
    try:
        inlet_pressure = float(entry_inlet2.get())
        outlet_pressure = float(entry_outlet2.get())
        temperature = float(entry_temp2.get())
        design_speed = float(entry_design_speed2.get())
        diameter = float(entry_diameter2.get())

    except ValueError:
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return


    if not all([inlet_pressure, outlet_pressure, temperature, design_speed, diameter]):
        messagebox.showerror("Error", "Please fill in all the required fields.")
        return

#-------------------------------------convert-------------------------------------------#

    val_d_ft = cal_part.convert_diameter(diameter,d_combo2.get())
    val_t_f = cal_part.convert_to_fahrenheit(temperature,t_combo2.get())
    val_pi = cal_part.convert_to_psi(inlet_pressure,p_combo2.get())
    val_po = cal_part.convert_to_psi(outlet_pressure, p_o_combo2.get())
    val_f = cal_part.unit_ib(float(entry_flow2.get()),f_combo2.get())
    entropy = steam_table.s_pt(val_pi,val_t_f)
    enthalpy_in = steam_table.h_ps(val_pi,entropy)
    enthalpy_out = steam_table.h_ps(val_po, entropy)
    blade_enthalpy = blade.calculate_h_in_btu_2(design_speed,val_d_ft)
    enthalpy_diff = enthalpy_in - enthalpy_out
    stages = float(enthalpy_diff/blade_enthalpy)
    power_t =table_output.entropy_to_power(enthalpy_diff,val_f)
    blade_eff = round(blade.ratio_mu_co(blade.rotor_speed(design_speed,val_d_ft),enthalpy_diff),2)
    label_eff_val_a = blade.blade_eff(blade.rotor_speed(design_speed,val_d_ft),enthalpy_diff)


    entry_entropy2.delete(0, END)
    entry_entropy2.insert(0, entropy)
    entry_enthalpy_inlet2.delete(0, END)
    entry_enthalpy_inlet2.insert(0, enthalpy_in)
    entry_enthalpy_out2.delete(0, END)
    entry_enthalpy_out2.insert(0, enthalpy_out)
    entry_enthalpy_diff2.delete(0, END)
    entry_enthalpy_diff2.insert(0, enthalpy_diff)
    entry_stage2.delete(0,END)
    entry_stage2.insert(0,stages)
    entry_power2.delete(0,END)
    entry_power2.insert(0,power_t)
    label_br_val.delete(0, END)
    label_br_val.insert(0, blade_eff)
    label_eff_val.delete(0, END)
    label_eff_val.insert(0,label_eff_val_a)







def values_first_stage2():
    entropy = float(entry_entropy2.get())
    inlet_pressure = float(entry_inlet2.get())
    outlet_pressure = float(entry_outlet2.get())
    inlet_temperature = float(entry_temp2.get())



    enthalpy_inlet = float(entry_enthalpy_inlet2.get())
    enthalpy_out = float(entry_enthalpy_out2.get())
    stage_f = int(entry_stage_f2.get())
    design_speed = float(entry_design_speed2.get())
    h_diff = float(table_output.diff_h(enthalpy_inlet,enthalpy_out,stage_f))
    d = float(blade.diameter_feet(design_speed,h_diff))
    h_ideal = table_output.entholpy_idea(enthalpy_inlet,h_diff)
    h_actual = table_output.entholpy_actual_frame2(enthalpy_inlet,h_diff,float(label_eff_val.get()))
    p_i = cal_part.convert_to_psi(inlet_pressure,p_combo2.get())
    p_1 = steam_table.p_hs(h_ideal,entropy)
    t_i = cal_part.convert_to_fahrenheit(inlet_temperature,t_combo2.get())
    t_1 = steam_table.t_ph(p_1,h_actual)
    s_1 = steam_table.s_ph(p_1,h_actual)
    v_1 = steam_table.v_ph(p_1,h_actual)
    v_in =steam_table.v_pt(inlet_pressure,inlet_temperature)

    p_o = cal_part.convert_to_psi(outlet_pressure,p_o_combo2.get())
    h_o  = steam_table.h_ps(p_o, entropy)
    power_t  = table_output.entropy_to_power(h_diff,cal_part.unit_ib(float(entry_flow2.get()),f_combo2.get()))
    return p_i,p_1,t_i,t_1,enthalpy_inlet,h_ideal,h_actual,entropy,s_1,v_in,v_1,d,p_o,h_o,h_diff,power_t

#----------------------------------------------------------------------------------------------#

def create_table2():
    pd.set_option('display.max_columns', None)
    design_speed = float(entry_design_speed2.get())
    arr = values_first_stage2()
    stages = int(entry_stage_f2.get())
    stage = [f'Stage {i+1}'for i in range(stages)]
    dict = {}
    dict['Stage 1'] = arr

    for i in range(stages-1):
        list = []
        p_i = dict[f'Stage {i+1}'][1]
        t_i = dict[f'Stage {i+1}'][3]
        h_i = dict[f'Stage {i+1}'][6]
        s_i = dict[f'Stage {i+1}'][8]
        v_in = dict[f'Stage {i+1}'][10]

        p_o = dict[f'Stage {i+1}'][12]
        h_o = steam_table.h_ps(p_o,s_i)
        h_diff_among = h_i-h_o
        stage_left = stages - (i+1)
        h_diff = float(h_diff_among/stage_left)
        h_ideal = table_output.entholpy_idea(h_i,h_diff)
        h_actual = table_output.entholpy_actual_frame2(h_i,h_diff,float(label_eff_val.get()))
        d = blade.diameter_feet(design_speed, h_diff )

        p_1 = steam_table.p_hs(h_ideal,s_i)
        t_1 = steam_table.t_ph(p_1,h_actual)
        s_1 = steam_table.s_ph(p_1,h_actual)
        v_1 = steam_table.v_ph(p_1,h_actual)
        power = table_output.entropy_to_power(h_diff,cal_part.unit_ib(float(entry_flow2.get()),f_combo2.get()))
        list.extend(( p_i,p_1,t_i,t_1,h_i,h_ideal,h_actual,s_i,s_1,v_in,v_1,d,p_o,h_o,h_diff,power))
        dict[f'Stage {i+2}'] = list
    df = pd.DataFrame(dict,columns=stage, index=table_output.main_row)
    df.to_excel('Real_Eff.xlsx', sheet_name='Stage in real efficiency')
    print(df)
    tkinter.messagebox.showinfo('Create steam stage','Success!')
##-------------------------------------------find power-------------------------#


def gen_p2():

    ml = float(entry_ml2.get())
    gb = float(entry_gb2.get())
    al = float(entry_al2.get())
    mg = (100 - (float(entry_mg2.get()))) *0.01
    pw = float(entry_power2.get())

    pwml = pw-ml
    pwgl = pwml * gb *al *mg


    entry_gpt2.delete(0,END)
    entry_gpt2.insert(0,pwgl)
##-------------------------------------------Title-------------------------#

label_eff = Label(title_frame2,text='Effiency: ',font=FONT,fg="black",bg=COLOR)
label_eff_val = Entry(title_frame2,width=10,font=FONT)
label_br = Label(title_frame2,text="Blade Ratio: ",font=FONT,fg="black",bg=COLOR)
label_br_val = Entry(title_frame2,width=10,font=FONT)

label_eff.grid(row=0,column=0,sticky='w')
label_eff_val.grid(row=0,column=1,sticky='w')
label_br.grid(row=0,column=2,sticky='w')
label_br_val.grid(row=0,column=3,sticky='w')


##-------------------------------------------input-------------------------#


label_inlet = Label(input_frame2,text="Inlet Pressure: ",font=FONT,fg="black",bg=COLOR)
label_outlet = Label(input_frame2,text="Outlet Pressure: ",font=FONT,fg="black",bg=COLOR)
label_temp=Label(input_frame2,text="Temperature: ",font=FONT,fg="black",bg=COLOR)
label_flow = Label(input_frame2,text="Flow: ",font=FONT,fg="black",bg=COLOR)
label_diameter = Label(input_frame2,text="Diameter: ",font=FONT,fg="black",bg=COLOR)
label_design_speed = Label(input_frame2,text="Design Speed: ",font=FONT,fg="black",bg=COLOR)


entry_inlet2 = Entry(input_frame2,width=10,font=FONT)
entry_temp2 = Entry(input_frame2,width=10,font=FONT)
entry_outlet2 = Entry(input_frame2,width=10,font=FONT)
entry_flow2 = Entry(input_frame2,width=10,font=FONT)
entry_diameter2 = Entry(input_frame2,width=10,font=FONT)
entry_design_speed2 = Entry(input_frame2,width=10,font=FONT)


p_combo2 = ttk.Combobox(input_frame2, value=UNIT_P, width=10,font=FONT)
p_combo2.set("BarG")
p_o_combo2 = ttk.Combobox(input_frame2, value=UNIT_P, width=10,font=FONT)
p_o_combo2.set("BarG")
t_combo2 = ttk.Combobox(input_frame2, value=UNIT_T, width=10,font=FONT)
t_combo2.set("Degree C")
f_combo2 = ttk.Combobox(input_frame2, value=UNIT_F, width=10,font=FONT)
f_combo2.set("Kgs/Hrs")
d_combo2 = ttk.Combobox(input_frame2, value=UNIT_D, width=10,font=FONT)
d_combo2.set("Inches")
ds_combo2 = ttk.Combobox(input_frame2, value=UNIT_DS, width=10,font=FONT)
ds_combo2.set("RPM")

label_inlet.grid(row=0, column=0, sticky='w')
entry_inlet2.grid(row=0, column=1)
p_combo2.grid(row=0, column=2)

label_temp.grid(row=1, column=0, sticky='w')
entry_temp2.grid(row=1, column=1)
t_combo2.grid(row=1, column=2)

label_outlet.grid(row=2, column=0, sticky='w')
entry_outlet2.grid(row=2, column=1)
p_o_combo2.grid(row=2, column=2)

label_flow.grid(row=3, column=0, sticky='w')
entry_flow2.grid(row=3, column=1)
f_combo2.grid(row=3, column=2)

label_diameter.grid(row=4, column=0, sticky='w')
entry_diameter2.grid(row=4, column=1)
d_combo2.grid(row=4, column=2)

label_design_speed.grid(row=5, column=0, sticky='w')
entry_design_speed2.grid(row=5, column=1)
ds_combo2.grid(row=5, column=2)




##---------------------cal part--------------------##

btn_cal = Button(process_frame2,text="Calculate",font=FONT,command=put_values2)
btn_cal.grid(row=0,column=0,ipadx=150)

##-----------------------------------------------##

label_entropy = Label(output_frame2,text="Entropy  : ",font=FONT,fg="black",bg=COLOR)
entry_entropy2 = Entry(output_frame2,width=15,font=FONT)
label_entropy_unit = Label(output_frame2,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)


label_enthalpy_inlet = Label(output_frame2,text="Enthalpy Input :",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_inlet2 = Entry(output_frame2,width=15,font=FONT)
label_enthalpy_unit_inlet = Label(output_frame2,text="Btu /ibm",font=FONT,fg="black",bg=COLOR)

label_enthalpy_out = Label(output_frame2,text="Enthalpy Outlet : ",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_out2= Entry(output_frame2,width=15,font=FONT)
label_enthalpy_unit_out = Label(output_frame2,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)

label_enthalpy_diff = Label(output_frame2,text="Differential Enthalpy : ",font=FONT,fg="black",bg=COLOR)
entry_enthalpy_diff2 = Entry(output_frame2,width=15,font=FONT)
label_enthalpy_unit_diff = Label(output_frame2,text="    Btu /ibm R",font=FONT,fg="black",bg=COLOR)


label_stage = Label(output_frame2,text="Number Of Stages :",font=FONT,fg="black",bg=COLOR)
entry_stage2 = Entry(output_frame2,width=15,font=FONT)
label_stage_unit = Label(output_frame2,text="   stages ",font=FONT,fg="black",bg=COLOR)


label_stage_f = Label(output_frame2,text="Number Of Stages :",font=FONT,fg="black",bg=COLOR)
entry_stage_f2 = Entry(output_frame2,width=15,font=FONT,bg='gray')
label_stage_unit_f = Label(output_frame2,text="   stages ",font=FONT,fg="black",bg=COLOR)


label_power = Label(output_frame2,text="Power Turbine:",font=FONT,fg="black",bg=COLOR)
entry_power2 = Entry(output_frame2,width=15,font=FONT)
label_power_unit = Label(output_frame2,text="   BTU/Hrs ",font=FONT,fg="black",bg=COLOR)


label_entropy.grid(row=0,column=0,sticky='w')
entry_entropy2.grid(row=0,column=1)
label_entropy_unit.grid(row=0,column=2)

label_enthalpy_inlet.grid(row=1,column=0,sticky='w')
entry_enthalpy_inlet2.grid(row=1,column=1)
label_enthalpy_unit_inlet.grid(row=1,column=2)

label_enthalpy_out.grid(row=2,column=0,sticky='w')
entry_enthalpy_out2.grid(row=2,column=1)
label_enthalpy_unit_out.grid(row=2,column=2)

label_enthalpy_diff.grid(row=3,column=0,sticky="w")
entry_enthalpy_diff2.grid(row=3,column=1)
label_enthalpy_unit_diff.grid(row=3,column=2)

label_stage.grid(row=4,column=0,sticky='W')
entry_stage2.grid(row=4,column=1)
label_stage_unit.grid(row=4,column=2)

label_stage_f.grid(row=5,column=0,sticky='W')
entry_stage_f2.grid(row=5,column=1)
label_stage_unit_f.grid(row=5,column=2)

label_power.grid(row=6,column=0,sticky='W')
entry_power2.grid(row=6,column=1)
label_power_unit.grid(row=6,column=2)

##-----------------------------------------------##

label_cal_each_stage = Label(output_frame_btn,text="Find each stage values:",font=FONT,fg="black",bg=COLOR)
label_cal_each_stage.grid(row=0,column=0,padx=0)

btn_cal_each_stage = Button(output_frame_btn,text="Calculate",font=FONT,command=create_table)
btn_cal_each_stage.grid(row=0,column=1,ipadx=65)

##-----------------------------------------------##

label_ml = Label(power_frame2,text="Mechanical Loss:",font=FONT,fg="black",bg=COLOR)
entry_ml2 = Entry(power_frame2,width=15,font=FONT)
label_et1 = Label(power_frame2,text="      " ,bg=COLOR)

label_gb = Label(power_frame2,text="Gear Box eff.:",font=FONT,fg="black",bg=COLOR)
entry_gb2 = Entry(power_frame2,width=15,font=FONT)
label_et2 = Label(power_frame2,text="      ",bg=COLOR)

label_al = Label(power_frame2,text="Alternator eff.:",font=FONT,fg="black",bg=COLOR)
entry_al2 = Entry(power_frame2,width=15,font=FONT)
label_et3 = Label(power_frame2,text="      ",bg=COLOR)

label_mg = Label(power_frame2,text="Margin:",font=FONT,fg="black",bg=COLOR)
entry_mg2 = Entry(power_frame2,width=15,font=FONT)
label_et4 = Label(power_frame2, text="      ", bg=COLOR)

label_ml.grid(row=0,column=0,sticky='W',ipadx=3)
entry_ml2.grid(row=0,column=1,ipadx=20)
label_et1.grid(row=0,column=2)


label_gb.grid(row=1,column=0,sticky='W',ipadx=3)
entry_gb2.grid(row=1,column=1,ipadx=20)
label_et2.grid(row=1,column=2)

label_al.grid(row=2,column=0,sticky='W',ipadx=3)
entry_al2.grid(row=2,column=1,ipadx=20)
label_et3.grid(row=2,column=2)

label_mg.grid(row=3,column=0,sticky='W',ipadx=3)
entry_mg2.grid(row=3,column=1,ipadx=20)
label_et4.grid(row=3,column=2)

##-----------------------------------------------##

label_cal_each_stage = Label(output_frame_btn2,text="Find each stage values:",font=FONT,fg="black",bg=COLOR)
label_cal_each_stage.grid(row=0,column=0,padx=0)

btn_cal_each_stage = Button(output_frame_btn2,text="Calculate",font=FONT,command=create_table2)
btn_cal_each_stage.grid(row=0,column=1,ipadx=65)


##-----------------------------------------------##

label_power2 = Label(power_frame2,text="Find Power Generator:",font=FONT,fg="black",bg=COLOR)
label_power2.grid(row=4,column=0,padx=3)

btn_cal_power2 = Button(power_frame2,text="Calculate",font=FONT,command= gen_p2)
btn_cal_power2.grid(row=4,column=1,ipadx=63)


label_gpt2 = Label(power_frame_out2,text="Generator Power:",font=FONT,fg="black",bg=COLOR)
entry_gpt2 = Entry(power_frame_out2,width=15,font=FONT)
label_gptu2 = Label(power_frame_out2,text="BTU/Hrs ",font=FONT,fg="black",bg=COLOR)


label_gpt2.grid(row=0,column=0,sticky='W',ipadx=5)
entry_gpt2.grid(row=0,column=1,padx=10)
label_gptu2.grid(row=0,column=2,padx=10)


##-----------------------Matplot------------------------##

left_frame = Frame(root, bg=COLOR)
left_frame.grid(row=0, column=0, sticky="nsew")
label = Label(left_frame, text="Left Side", bg=COLOR)
label.grid(row=0, column=0)
right_frame = Frame(root, bg=COLOR)
right_frame.grid(row=0, column=1, sticky="nsew")
x_list = np.arange(0.05, 0.46, 0.01)
y = (-26.75*(x_list**4)) + (31.569*(x_list**3)) - (16.251*(x_list**2)) + (5.2618*x_list) - 0.0514
fig, ax = plt.subplots()

def plot(page_number):
    ax.clear()
    ax.plot(x_list, y, linewidth = 2, color='black',label='RATEAU LIMIT DESIGN')
    ax.set_title("BLADE EFFICIENCY CURVE")
    ax.set_xlabel("EFFICIENCY")
    ax.set_ylabel("PERIPHERAL VELOCITY OF ROTOR / STEAM VELOCITY AT EXIT")

    if page_number == 1:
        specific_index = -1
    elif page_number == 2:
        specific_val = label_br_val.get()

        if specific_val.strip():
            specific_val = float(specific_val)
            specific_index = np.abs(x_list - specific_val).argmin()
        else:
            specific_index = 0
    dot_marker, = ax.plot(x_list[specific_index], y[specific_index], marker='o', markersize=8, color='red',
                          label='Dot Marker')


    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")


    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)




##----------------------Switch frame-------------------------##

btn_change_page1 = Button(cp_frame, text="Change Page", font=FONT, command=lambda: show_page(page_2))
btn_change_page1.grid(row=0,column=0,ipadx=75,ipady=15)

btn_plot = Button(cp_frame, text="Plot Graph", font=FONT, command=lambda: plot(1))
btn_plot.grid(row=0,column=1,ipadx=75,ipady=15)

btn_change_page2 = Button(cp_frame2, text="Change Page", font=FONT, command=lambda: show_page(page_1))
btn_change_page2.grid(row=0,column=0,ipadx=75,ipady=15)

btn_plot2 = Button(cp_frame2, text="Plot Graph", font=FONT, command=lambda: plot(2))
btn_plot2.grid(row=0,column=1,ipadx=75,ipady=15)
##-----------------------Window------------------------##
page_1.tkraise()
root.mainloop()



