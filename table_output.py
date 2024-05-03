import pandas as pd

import blade

from pyXSteam.XSteam import XSteam
steam_table = XSteam(XSteam.UNIT_SYSTEM_FLS)

list = []
main_row = ['Pressure Inlet(psiG)', 'Pressure At Stage(psiG)','Temperature Inlet(Degree F)','Temperature At The Stage(Degree F)',
            'Enthalpy Inlet(Btu /ibm)', 'Ideal Heat Drop(Btu /ibm)','Actual Heat Drop(Btu /ibm)','Entropy Inlet(Btu /ibm R)','Entropy At The Stage(Btu /ibm R )','Specific Volume Inlet(in^3/ibm)',
            'Specific Volume Outlet(in^3/ibm)','Blade Diameter(feet)','Pressure Outlet(psiG)','Enthalpy Outlet(Btu /ibm)','Enthalpy Difference (Btu /ibm)','Power (BTU/Hrs)']



def diff_h(hi,ho,stage):
    return format((hi-ho)/stage,'4f')

def entholpy_idea(h1,diff_h):
    return h1-diff_h

def entholpy_actual(h1,diff_h):
    return h1-(diff_h*0.8)


def entholpy_actual_frame2(h1,diff_h,eff):
    return h1-(diff_h*eff)


def stage_table(col):
    return  pd.DataFrame( columns=col,index=main_row)


def entropy_to_power(entropy, flow_rate):


    energy_flow_rate_btu_per_hr = entropy * flow_rate

    return energy_flow_rate_btu_per_hr


