from __future__ import division
from past.utils import old_div
import nltk, re, pprint
from whyis import autonomic
from rdflib import *
from rdflib.resource import Resource
from whyis import nanopub
from .unit_converter import calculate_converted_units, is_a_convertible_unit_attr

from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

class UnitConverter(autonomic.UpdateChangeService):
    activity_class = whyis.UnitConverter

    def getInputClass(self):
        return URIRef("http://nanomine.org/ns/PolymerNanocomposite")

    def getOutputClass(self):
        return URIRef("http://nanomine.org/ns/PolymerNanocomposite")

    def get_query(self):
        uri = "http://nanomine.org/sample/e116-s29-prasad-2018"
        query = '''SELECT DISTINCT ?s WHERE {{
    _:doi <http://semanticscience.org/resource/hasPart> ?s .
    ?s <http://semanticscience.org/resource/hasAttribute> ?a . 
    ?a <http://semanticscience.org/resource/hasUnit> []; 
       <http://semanticscience.org/resource/hasValue> [] .
    FILTER( ?s NOT IN(<{0}>) ) .
    FILTER NOT EXISTS {{ ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://nanomine.org/nm/ConvertedUnit> }} .
}}'''.format(uri)
        return query

    def process(self, i, o):
        converted = []
        for attr in i.objects(sio.hasAttribute):
            if is_a_convertible_unit_attr(attr):
                converted.extend(calculate_converted_units(attr))
        for new_meas in converted:
            o.add(sio.hasAttribute, new_meas)
            new_meas_URI = new_meas._identifier
            for p_, o_ in new_meas.predicate_objects():
                if isinstance(o_, Resource):
                    o._graph.add((new_meas_URI, p_._identifier, o_._identifier))
                else:
                    o._graph.add((new_meas_URI, p_._identifier, o_))
