# Whyis-unit-converter

## Installation
- install [whyis](http://tetherless-world.github.io/whyis/install) using this command
  ```
  WHYIS_BRANCH=master bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/whyis/master/install.sh)
  ```
- whyis will be installed in /apps/whyis

- In your knowledge graph directory, add the unit converter agent to the list of inferencers in your config.py file:
  * Add the following import line: `import whyis_unit_converter.converter as converter`
  * Add the following line to the `inferencers` item in the `Config` dictionary constructor: `"UnitConverter": converter.UnitConverter()`

- Reload your knowledge graph to run the inferencer over it


## Loading unit definition and translation files
- To load your own unit definition and translation files, run `importconverterdict FILES`
- Your translation files can be in one of the following forms:

  * URI to unit mapping file. Used to map measurement types to their preferred units, if sio:hasPreferredUnit is not used in your knowledge graph.
  ```
  #mapping_file
  http://nanomine.org/ns/CharpyImpactEnergy=http://www.ontology-of-units-of-measure.org/resource/om-2/joulePerSquareMetre
  http://nanomine.org/ns/CrystalizationTemperature=http://www.ontology-of-units-of-measure.org/resource/om-2/kelvin
  ```

  * Translation file. Used to translate URIs into understandable units. Translations to understandable units are written as below. See [defining pint units](https://pint.readthedocs.io/en/0.11/defining.html) for more specific information about formatting.
  ```
  #translation_file
  http://www.ontology-of-units-of-measure.org/resource/om-2/degreeFahrenheit=5 / 9 * kelvin; offset: 233.15 + 200 / 9
  http://www.ontology-of-units-of-measure.org/resource/om-2/amperePerSquareMetre=ampere / meter ** 2
  http://nanomine.org/ns/unit/kpa=kilopascal
  ```


## Testing
- To test the unit converter, run `unitconvertertest` from a pip enabled endpoint.
