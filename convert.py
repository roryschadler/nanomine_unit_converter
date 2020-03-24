""" Converts a value from one unit to another.
    Uses pint to do the actual conversion, expects the user to pass in
    pint-recognized unit names.
"""
from pint import UnitRegistry, UndefinedUnitError, DimensionalityError
import re
from math import log10, floor

Q_ = UnitRegistry().Quantity

def convert_to_other_units(meas_unit, meas_val, new_units):
    converted = []
    for new_unit in new_units:
        if new_unit != meas_unit:
            new_value = convert(meas_val, meas_unit, new_unit)
            converted.append((new_unit, new_value))
    return converted

def convert(value, from_unit, to_unit):
    """ Converts a value from one unit to another, and returns the result.
        Expects from_unit and to_unit are pint-recognized strings, else it
        returns None. If an invalid conversion is attempted, it also returns
        None.
    """
    try:
        converted = Q_(value, from_unit).to(to_unit)
    except UndefinedUnitError as exc:
        print("One of the units ({},{})"\
              " is not defined.".format(from_unit, to_unit))
        return None
    except DimensionalityError as exc:
        #print("The attempted unit conversion from"\
        #      " {} to {} is not possible.".format(from_unit, to_unit))
        return None
    else:
        converted_val = round_sig(converted.m,
                                  number_of_significant_figures(value))
        return converted_val

def round_sig(x, sig=2):
    return round(x, sig-int(floor(log10(abs(x)))))

def number_of_significant_figures(num):
    """ Returns the number of significant figures a value has. """
    if isinstance(num, int) or num.is_integer():
        num = int(num)
        sig_figs = len(str(num).strip('0'))
    else:
        num_parts = re.split(r'[\.eE]', str(num))
        sig_figs = len(num_parts[1])
    return sig_figs

def short_tests():
    print("Precision Tests")
    tests = [4.777776e-8, 4.777776e8, 4.777e8, 5.0, 5.123456789, 5,
             5.123456789e-15, 5.4e4, 5.4e-8, 5.4e45]
    for num in tests:
        print(num, "->", convert(num, "meter", "meter"))
    print("-" * 40, "\nConversion tests")
    print(convert(373, "kelvin", "celsius"))
    print(convert(373, "asdf", "celsius"))
    print(convert(373, "meter", "celsius"))

# short_tests()
