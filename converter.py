from __future__ import division
from past.utils import old_div
import nltk, re, pprint
from whyis import autonomic
from rdflib import *
from whyis import nanopub
from .unit_converter import calculate_converted_units

from whyis.namespace import sioc_types, sioc, sio, dc, prov, whyis

class UnitConverter(autonomic.UpdateChangeService):
    activity_class = whyis.UnitConverter

    def getInputClass(self):
        return None

    def getOutputClass(self):
        return URIRef("http://nanomine.org/ns/ConvertedUnit")

    def get_query(self):
        return '''select ?s where {
    _:doi <http://semanticscience.org/resource/hasPart> ?s.
    ?s <http://semanticscience.org/resource/hasAttribute> ?a.
    ?a <http://semanticscience.org/resource/hasUnit> ?u;
        <http://semanticscience.org/resource/hasValue> ?v.
    FILTER NOT EXISTS { ?s <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://nanomine.org/nm/convertedUnit> }
} LIMIT 20'''

    def process(self, i, o):
        for attr in i.objects(sio.hasAttribute):
            converted = calculate_converted_units(i, attr)
        for new_meas in converted:
            o.add(sio.hasAttribute, new_meas)
            for p, new_o in new_meas.predicate_objects():
                print(p, new_o)
