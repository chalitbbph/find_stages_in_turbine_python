import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('My_output')
pd.set_option('display.max_columns', None)

main_row = ['Pressure Inlet(psi)', 'Pressure At Stage(psi)','Temperature Inlet(Degree F)','Temperature At The Stage(Degree F)',
            '', 'Ideal Heat Drop(Btu /ibm)','Actual Heat Drop(Btu /ibm)','Entropy Inlet(Btu /ibm R)','Entropy At The Stage(Btu /ibm R )','Specific Volume Inlet(in^3/ibm)',
            'Specific Volume Outlet(in^3/ibm)','Blade Diameter(feet)','Pressure Outlet(psi)','Enthalpy Outlet(Btu /ibm)','Entropy difference']
plt.xlabel("Enthalpy Inlet(Btu /ibm)")
plt.ylabel("Y Label")
x = df.iloc[[4,5,6]]
y = df.iloc[-2]

plt.show()