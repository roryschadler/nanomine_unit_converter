""" Finds and converts measurements in the Nanomine knowledge graph."""

from .convert import convert_to_other_units
from .dictionary import read_dictionary
from .nanomine_kg_parser import (attr_value,
                                attr_type,
                                attr_type_URI,
                                attr_unit,
                                measurement_attribute,
                                get_meas_attrs,
                                add_new_meas)

# dictionaries for conversion between units
convertible_units = read_dictionary("agents/converter/ontology_dicts/nanomine_dictionary.txt")
ontology_to_pint_dict = read_dictionary("agents/converter/ontology_dicts/ontology_units_to_pint_dictionary.txt")
unit_to_pint_dict = read_dictionary("agents/converter/ontology_dicts/old_unit_to_pint.txt")

def convert_and_add_measurements(kg):
    """ Takes Nanomine KG sample and adds measurement conversions to all units.
        Ignores attributes that are not in the list of convertible attributes
        given in the config file.
    """
    attributes = get_meas_attrs(kg)
    for attr in attributes:
        add_new_meas(kg, calculate_converted_units(attr))

def calculate_converted_units(attr):
    """ Calculate unit conversions if passed a convertible attribute."""
    if is_a_convertible_unit_attr(attr):
        # pull important values off attribute
        meas_type = attr_type(attr)
        meas_type_URI = attr_type_URI(attr)
        unit_URI = attr_unit(attr)
        meas_value = attr_value(attr)
        if (meas_type is None or meas_type_URI is None
            or unit_URI is None or meas_value is None):
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
        elif not unit_URI:
            # we don't have a unit, we can't convert, return empty list
            return []
        else:
            # unit is unrecognized
            print("WARNING: unit {} not recognizable".format(unit_URI))
            return []
        # do all unit conversion, return list of attributes
        converted_meas_tuples = convert_to_other_units(meas_unit, meas_value,
                                                       possible_units)
        converted = []
        for new_unit, new_val in converted_meas_tuples:
            if new_unit is not None and new_val is not None:
                converted.append(measurement_attribute(om_unit_to_uri(new_unit),
                                                   new_val,
                                                   meas_type_URI))
        return converted
    else:
        return []

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

def main():
    import rdflib
    from rdflib.resource import Resource
    totalgraph = rdflib.Graph()
    mysample = rdflib.URIRef("http://myref.org/mysample")
    nanopub = Resource(totalgraph, mysample)
    # mymeas = rdflib.BNode()
    val = rdflib.Literal(5)
    unit = rdflib.URIRef("http://www.ontology-of-units-of-measure.org/resource/om-2/nanometre")
    type = rdflib.URIRef("http://semanticscience.org/resource/Width")
    mymeas = Resource(totalgraph, rdflib.BNode())
    # g.add((mysample, rdflib.URIRef("http://semanticscience.org/resource/hasAttribute"), mymeas))
    mymeas.add(rdflib.URIRef("http://semanticscience.org/resource/hasValue"), val)
    mymeas.add(rdflib.URIRef("http://semanticscience.org/resource/hasUnit"), unit)
    mymeas.add(rdflib.URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"), type)
    nanopub.add(rdflib.URIRef("http://semanticscience.org/resource/hasAttribute"), mymeas)
    convert_and_add_measurements(nanopub)
    print(nanopub.graph.serialize(format='xml'))

# main()
