""" Finds and converts measurements in the Nanomine knowledge graph."""

from numbers import Real

from .convert import convert_to_other_units, load_user_definitions
from .dictionary import read_dictionary
from .nanomine_kg_parser import *

# dictionaries for conversion between units
convertible_units = read_dictionary("agents/converter/ontology_dicts/nanomine_dictionary.txt")
ontology_to_pint_dict = read_dictionary("agents/converter/ontology_dicts/ontology_units_to_pint_dictionary.txt")
unit_to_pint_dict = read_dictionary("agents/converter/ontology_dicts/old_unit_to_pint.txt")

# new dictionaries for unit conversion
translations = read_dictionary("agents/converter/dicts/translations.txt")
load_user_definitions("agents/converter/dicts/pint_defs.txt")

def calculate_converted_units(attr):
    """ Calculate unit conversions if passed a convertible attribute."""
    if not is_a_convertible_unit_attr(attr):
        return []
    else:
        # pull important values off attribute
        meas_type = attr_type(attr)
        meas_type_URI = attr_type_URI(attr)
        unit_URI = attr_unit(attr)
        meas_value = attr_value(attr)
        if (meas_type is None
            or meas_type_URI is None
            or unit_URI is None
            or meas_value is None
            or not isinstance(meas_value, Real)):
            # if any data is empty, or the value is not a number
            return []
        possible_units = []

        # get pint-friendly unit names
        for unit in convertible_units[meas_type]:
            possible_units.append(ontology_to_pint_dict[unit][0])
        if unit_URI in unit_to_pint_dict:
            # unit URI is in old units (pre apr 2020)
            meas_unit = unit_to_pint_dict[unit_URI][0]
        elif unit_URI in ontology_to_pint_dict:
            # unit URI is in OM (post apr 2020)
            meas_unit = ontology_to_pint_dict[unit_URI][0]
        else:
            # unit is unrecognized
            # print("WARNING: unit {} not recognizable".format(unit_URI))
            return []
        
        # do all unit conversion, return list of attributes
        converted_meas_tuples = convert_to_other_units(meas_unit, meas_value,
                                                       possible_units)
        converted = []
        for new_unit, new_val in converted_meas_tuples:
            # if the conversion returned everything it was supposed to
            if new_unit is not None and new_val is not None:
                converted.append(measurement_attribute(om_unit_to_uri(new_unit),
                                                   new_val,
                                                   meas_type_URI))
        return converted

def is_a_convertible_unit_attr(attr):
    """ Returns true if attribute's type is in Nanomine dictionary"""
    return attr_type(attr) in convertible_units

def om_unit_to_uri(unit):
    """ Creates a URI for a given unit"""
    base = "http://www.ontology-of-units-of-measure.org/resource/om-2/"
    for k, v in ontology_to_pint_dict.items():
        if unit in v:
            unit_URI = k
            break
    return base + unit_URI
