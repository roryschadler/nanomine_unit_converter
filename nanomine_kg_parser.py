""" Provides an interface for rdflib Resources for Nanomine unit converter."""

import rdflib
from rdflib.resource import Resource

import re

sio = rdflib.Namespace("http://semanticscience.org/resource/")

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
