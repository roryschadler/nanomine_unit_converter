""" Provides an interface for rdflib Resources for Nanomine unit converter."""

import rdflib
import re

sio = rdflib.Namespace("http://semanticscience.org/resource/")

def measurement_attribute(unit_URI, new_value, unit_type):
    """ Creates a new sio:hasAttribute object."""
    new_meas = rdflib.resource.Resource(rdflib.Graph(), rdflib.BNode())
    new_meas.add(sio.hasUnit, rdflib.URIRef(unit_URI))
    new_meas.add(sio.hasValue, rdflib.Literal(new_value))
    new_meas.add(rdflib.RDF.type, unit_type)
    new_meas.add(rdflib.RDF.type, rdflib.URIRef("http://nanomine.org/nm/ConvertedUnit"))
    return new_meas

def attr_type(attr):
    """ Returns the type of the given attribute, cleaned up"""
    try:
        type = next(attr.objects(rdflib.RDF.type)).identifier
        return re.split("[/#]", type)[-1].strip()
    except IndexError:
        return type
    except StopIteration:
        return ""

def attr_type_URI(attr):
    """ Returns the type of the given attribute."""
    try:
        return next(attr.objects(rdflib.RDF.type)).identifier
    except StopIteration:
        return ""

def attr_unit(attr):
    """ Returns the unit of the given attribute, cleaned up"""
    try:
        unit = next(attr.objects(sio.hasUnit)).identifier
        return re.split("[/#]", unit)[-1].strip()
    except IndexError:
        return unit
    except StopIteration:
        return ""

def attr_value(attr):
    """ Returns the value of the given attribute, cleaned up"""
    try:
        return next(attr.objects(sio.hasValue)).value
    except StopIteration:
        return ""

def attr_preferred_units(attr):
    """ asdf"""
    pref_unit_query = '''SELECT ?prefUnit WHERE {
    ?type <http://semanticscience.org/resource/hasPreferredUnit> ?prefUnit .
}'''
    pref_units = []
    for ut in attr.objects(rdflib.RDF.type):
        unittype = ut.identifier
    for result in attr.graph.query(pref_unit_query, initBindings={"type":unittype}):
        try:
            pref_units.append(re.split("[/#]", result.prefUnit.value)[-1].strip())
        except IndexError:
            to_unit = temp
    return pref_units
