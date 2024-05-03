import math

import numpy as np

np.set_printoptions(precision=2, suppress=True)
x_list = np.arange(0.05, 0.46, 0.01)
y_list = [18,2,22,26,31,35,37,39,43,44,46,48,51,53,55,56,58,59,61,62,63.5,65,65.5,66.5,68,70,70.5,71.5,72.5,73,74,76,76.5,77,77.5,78,79,80,80,80,80]

def rotor_speed(design_speed,diameter):

    return  (math.pi* design_speed * diameter) / 60

def steam_speed(design_speed,diameter):

    rotor_s = rotor_speed(design_speed,diameter)
    steam_speed =rotor_s/.46

    return steam_speed



def calculate_h_in_btu(n,d):

    h_btu = (steam_speed(n,d)/224)**2

    return h_btu


def steam_speed_enthalpy(h):

    return float(224* math.sqrt(h))

def diameter_feet(n,h_diff):
    co = (steam_speed_enthalpy(h_diff))
    sse = 0.42*co
    return (60*sse)/(math.pi*n)

def ratio_mu_co(mu, h):
    co = steam_speed_enthalpy(h)
    return round(mu / co,2)

def blade_eff(mu,h):
    x = ratio_mu_co(mu,h)
    y = (-26.75 * (x ** 4)) + (31.569 * (x ** 3)) - (16.251 * (x ** 2)) + (5.2618 * x) - 0.0514

    return round(y,2)


def steam_speed2(design_speed,diameter,blade_eff):

    rotor_s = rotor_speed(design_speed,diameter)
    steam_speed =rotor_s/ blade_eff

    return steam_speed
def calculate_h_in_btu_2(n,d):

    h_btu = (steam_speed(n,d)/224)**2

    return h_btu
if __name__ == '__main__':
    print(ratio_mu_co(rotor_speed(9000,16),230.8))