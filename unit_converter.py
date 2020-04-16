""" Finds and converts measurements in the Nanomine knowledge graph."""

import pkg_resources
from contextlib import closing
from io import StringIO
from numbers import Real

from .convert import convert_to_other_units, load_user_definitions
from .dictionary import read_dictionary
from .nanomine_kg_parser import *

# dictionaries for conversion between units
unit_type_dict = read_dictionary("dicts/nanomine_dictionary.txt")
translations = read_dictionary("dicts/translations.txt")

try:
    with closing(pkg_resources.resource_stream(__name__, "dicts/pint_defs.txt")) as f:
        rbytes = f.read()
        load_user_definitions(StringIO(rbytes.decode('utf-8')))
except Exception as e:
    msg = getattr(e, 'message', '') or str(e)
    raise ValueError("While opening {}\n{}".format(f, msg))

def convert_attr_to_units(attr):
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
            return []

        # THIS WILL FUNCTION ONCE preferredUnit IS ADDED TO THE KG AND IS PASSED IN BY THE UNIT CONVERTER AGENT
        to_units = attr_preferred_units(attr)
        if not to_units:
            # THIS SHOULD BE REMOVED ONCE preferredUnit IS ADDED TO THE KG
            # get pint-friendly unit names
            to_units = [un for un in unit_type_dict[meas_type]]

        if unit_URI in translations:
            meas_unit = translations[unit_URI][0]
        else:
            meas_unit = unit_URI

        # do all unit conversion, return list of attributes
        converted_meas_tuples = convert_to_other_units(meas_unit, meas_value,
                                                       to_units)
        converted = []
        for new_unit, new_val in converted_meas_tuples:
            # if the conversion returned everything it was supposed to
            if new_unit is not None and new_val is not None:
                converted.append(measurement_attribute(om_unit_to_uri(new_unit),
                                                   new_val,
                                                   meas_type_URI))
        return converted

def is_a_convertible_unit_attr(attr):
    """ Returns true if attribute's type is in Nanomine dictionary.
        Possibly redundant if nanomine_kg_parser has been implemented
        correctly, checking for allowed types as it goes."""
    return attr_type(attr) in unit_type_dict

def om_unit_to_uri(unit):
    """ Creates a URI for a given unit"""
    return "http://www.ontology-of-units-of-measure.org/resource/om-2/" + unit
