import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Assuming you have already initialized `root` somewhere before this code snippet
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


##-------------------------------------------switch frame fun-------------------------------------##

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



COLOR = 'white'

left_frame = tk.Frame(root, bg=COLOR)
left_frame.grid(row=0, column=0, sticky="nsew")

label = tk.Label(left_frame, text="Left Side", bg=COLOR)
label.grid(row=0, column=0)

right_frame = tk.Frame(root, bg=COLOR)
right_frame.grid(row=0, column=1, sticky="nsew")

x_list = np.arange(0.05, 0.46, 0.01)
y = (-26.75*(x_list**4)) + (31.569*(x_list**3)) - (16.251*(x_list**2)) + (5.2618*x_list) - 0.0514
fig, ax = plt.subplots()
ax.plot(x_list, y)
ax.set_title('Your Plot Title')  # Set the title here
ax.set_xlabel("X Label")

# Adding a dot marker at a specific data point
specific_index = 20  # Change this to the index of the data point where you want the dot
ax.plot(x_list[specific_index], y[specific_index], marker='o', markersize=8, color='red')

canvas = FigureCanvasTkAgg(fig, master=right_frame)
canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

# Configure grid weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Assuming you have defined page_1 somewhere before this code snippet
page_1.tkraise()
root.mainloop()