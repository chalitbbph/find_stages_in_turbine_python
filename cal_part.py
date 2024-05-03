

def celsius_to_fahrenheit(celsius):
    return (celsius * 9/5) + 32

def kelvin_to_fahrenheit(kelvin):
    return (kelvin - 273.15) * 9/5 + 32

def convert_to_fahrenheit(degrees, unit):
    if unit == 'Degree C':
        return celsius_to_fahrenheit(degrees)
    elif unit == 'Degree k':
        return kelvin_to_fahrenheit(degrees)
    elif unit == 'Degree F':
        return degrees
    else:
        raise ValueError("Invalid unit. Please enter 'Degree C', 'Degree k', or 'Degree F'.")

def convert_diameter(val,unit):
    if unit == "Inches":
        return val / 12
    elif unit == "mm":
        return val * 0.00328084
    else:
        return val

def convert_diameter_in(val,unit):
    if unit == "Inches":
        return val
    elif unit == "mm":
        return val * 25.4

def convert_to_psi(value, unit):
    conversions_psi = {
        "BarA": 14.5038,
        "BarG": 14.5038,
        "psi": 1,
        "kPa": 0.145038,
        "kg/cm^2": 14.2233
    }

    if unit in conversions_psi:
        return value * conversions_psi[unit]
    else:
        raise ValueError("Unsupported unit")



def convert_to_barg(value, unit):
    conversions_bar = {
        "BarA": 1.01325,
        "BarG": 1,
        "psiG": 14.5038,
        "kPaG": 100,
        "kg/cm^2G": 1.01972
    }

    if unit in conversions_bar:
        if unit == "BarG":
            return value
        else:
            return value*conversions_bar
    else:
        return "Unit not found in conversions dictionary."


def unit_ib(mass_flow_rate, unit):

    kg_to_lb = 2.20462

    if unit == 'Kgs/Hr':
        mass_flow_rate = mass_flow_rate * kg_to_lb
    elif unit == 'Tons/Hr':
        mass_flow_rate = mass_flow_rate * kg_to_lb * 1000
    return mass_flow_rate

def calculate_power(enthalpy, mass_flow_rate):
    power_btu_per_s = enthalpy * mass_flow_rate
    return power_btu_per_s

