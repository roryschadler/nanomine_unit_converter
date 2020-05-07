# Whyis-unit-converter

# Installation
- install [whyis](http://tetherless-world.github.io/whyis/install) using this command
  ```
  WHYIS_BRANCH=master bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/whyis/master/install.sh)
  ```
- whyis will be installed in /apps/whyis

- In your knowledge graph directory, add the unit converter agent to the list of inferencers in your config.py file:
  * Add the following import line: `import whyis_unit_converter.converter as converter`
  * Add the following line to the `inferencers` item in the `Config` dictionary constructor: `"UnitConverter": converter.UnitConverter()`

- Reload your knowledge graph to run the inferencer over it

# Loading unit translation files
- Your translation files can be in one of the following forms:
  * Unit definitions file. Used to translate compound units or units with non-standard spellings into understandable units. See [defining pint units](https://pint.readthedocs.io/en/0.11/defining.html) for more specific information about formatting.
  ```
  #definitions_file
  joulePerSquareMetre = joule / meter ** 2
  metre = meter
  degreeFahrenheit = 5 / 9 * kelvin; offset: 233.15 + 200 / 9
  ```

  * URI to unit mapping file. Used to map measurement types to their preferred units, if sio:hasPreferredUnit is not used in your knowledge graph.
  ```
  #mapping_file
  CharpyImpactEnergy=joulePerSquareMetre
  CrystalizationTemperature=kelvin
  ThermalDiffusivity=squareMetrePerSecond-Time
  ```

  * Translation file. Used to translate un-parsable URIs into understandable units. No slug or fragment may contain a dash "-" or slash "/", unless that slug is translated in the translation file. Translations to understandable units are written as below. See [defining pint units](https://pint.readthedocs.io/en/0.11/defining.html) for more specific information about formatting.
  ```
  #translation_file
  minute-Time = minute
  w-mk = watts / meter / kelvin
  mol-m-3 = mole / meter ** 3
  ```

# Testing
- To test the unit converter, run `unitconvertertest` from a pip enabled endpoint.
