""" asdf"""

import rdflib
from rdflib.resource import Resource

import re

sio = rdflib.Namespace("http://semanticscience.org/resource/")

def get_meas_attrs(g):
    """ Wrapper for getting objects of sio:hasAttribute."""
    return g.objects(sio.hasAttribute)

def measurement_attribute(unit_URI, new_value, unit_type):
    """ Creates a new sio:hasAttribute object."""
    new_meas = Resource(rdflib.Graph(), rdflib.BNode())
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

def add_new_meas(g, new_meas_list):
    if isinstance(g, Resource):
        graph = g._graph
    else:
        graph = g
    for new_meas in new_meas_list:
        graph.add(sio.hasAttribute, new_meas)
        for p, o in new_meas.predicate_objects():
            if isinstance(o, Resource):
                graph.add((new_meas._identifier, p._identifier, o._identifier))
            else:
                graph.add((new_meas._identifier, p._identifier, o))

