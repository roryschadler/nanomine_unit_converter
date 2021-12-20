""" Provides an interface for rdflib Resources for Whyis unit converter."""

import rdflib
import re

from whyis.namespace import sio, prov

def measurement_attribute(unit_URI, new_value, unit_type, old_attr_uri):
    """ Creates a new sio:hasAttribute object."""
    new_meas = rdflib.resource.Resource(rdflib.Graph(), rdflib.BNode())
    new_meas.add(sio.hasUnit, rdflib.URIRef(unit_URI))
    new_meas.add(sio.hasValue, rdflib.Literal(new_value))
    new_meas.add(rdflib.RDF.type, unit_type)
    new_meas.add(rdflib.RDF.type, rdflib.URIRef("http://nanomine.org/nm/ConvertedUnit"))
    new_meas.add(prov.wasDerivedFrom, old_attr_uri)
    return new_meas

def attr_type(attr):
    """ Returns the slug of the URI for the object of RDF.type for the given subject."""
    try:
        temp = attr_type_URI(attr)
        type_slug = re.split("[/#]", temp)[-1].strip()
        return type_slug
    except IndexError:
        return temp
    except StopIteration:
        return ""

def attr_type_URI(attr):
    """ Returns the raw URI for the object of RDF.type for the given subject."""
    try:
        type_URI = next(attr.objects(rdflib.RDF.type)).identifier
        return type_URI
    except StopIteration:
        return ""

def attr_unit(attr):
    """ Returns the slug of the URI for the object of sio.hasUnit for the given subject."""
    try:
        unit = next(attr.objects(sio.hasUnit)).identifier
        return unit
    except StopIteration:
        return ""

def attr_value(attr):
    """ Returns the object of sio.hasValue for the given subject."""
    try:
        return next(attr.objects(sio.hasValue)).value
    except StopIteration:
        return ""

def attr_preferred_units(attr):
    """ Returns the given attribute's preferred units, if any.
        Expects well-formed attribute for querying."""
    pref_unit_query = '''SELECT ?prefUnit WHERE {
    ?type <http://nanomine.org/ns/hasPreferredUnit> ?prefUnit .
}'''
    pref_units = []
    ut_URI = attr_type_URI(attr)

    if not ut_URI:
        return []

    for result in attr.graph.query(pref_unit_query, initBindings={"type":ut_URI}):
        pref_units.append(result.prefUnit.value)
    return pref_units

def attr_incomplete_preferred_units(attr):
    """ Returns the given attribute's incomplete preferred units, if any.
        Expects well-formed attribute for querying."""
    has_derived_attr_with_pref_unit_query = '''ASK {
    [] <http://www.w3.org/ns/prov#wasDerivedFrom> ?attr;
       <http://semanticscience.org/resource/hasUnit> ?prefUnit.
}'''
    attr_URI = attr.identifier
    preferred_unit_URI_list = attr_preferred_units(attr)
    incomplete_preferred_units = []
    # query result evaluates to True if the given graph pattern has a solution
    for preferred_unit_URI in preferred_unit_URI_list:
        initBindings = {"attr": attr_URI, "prefUnit": rdflib.URIRef(preferred_unit_URI)}
        # if attr has no derived attribute in this preferred unit
        if not bool(attr.graph.query(has_derived_attr_with_pref_unit_query, initBindings=initBindings)):
            incomplete_preferred_units.append(preferred_unit_URI)
    return incomplete_preferred_units
