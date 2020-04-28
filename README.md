# Nanomine-unit-converter

# Installation
- install [whyis](http://tetherless-world.github.io/whyis/install) using this command
  ```
  WHYIS_BRANCH=master bash < <(curl -skL https://raw.githubusercontent.com/tetherless-world/whyis/master/install.sh)
  ```
- whyis will be installed in /apps/whyis
- install nanomine-graph app following:
  ```
  sudo su - whyis
  cd /apps
  git clone https://github.com/tetherless-world/nanomine-graph.git
  cd /apps/nanomine-graph
  pip install -e .
  exit
  sudo service apache2 restart
  sudo service celeryd restart
  sudo su - whyis
  pip install unit_converter
  cd /apps/whyis
  python manage.py createuser -e (email) -p (password) -f (frstname) -l (lastname) -u (username) --roles=admin
  ```

- In the nanomine-graph directory, add the unit converter agent to the list of inferencers in the config.py file:
  * Add the following import line: `import nanomine_unit_converter.converter as converter`
  * Add the following line to the `inferencers` item in the `Config` dictionary constructor: `"UnitConverter": converter.UnitConverter()`

- In your terminal, load the ontology and XML Ingest Semantic ETL file:
  ```
  cd /apps/whyis
  python manage.py load -i /apps/nanomine-graph/setl/ontology.setl.ttl -f turtle
  python manage.py load -i /apps/nanomine-graph/setl/xml_ingest.setl.ttl -f turtle
  python manage.py load -i 'http://semanticscience.org/ontology/sio-subset-labels.owl' -f xml
  ```

- Load any Nanomine XML files you may already have. There is a collection floating around among developers. For production, the curation service will post XML files to the Whyis instance when they're ready to be used.

  ```
  cd /apps/whyis
  python manage.py load -i </path/to/local_files.ttl> -f turtle
  ```

- To test the unit converter, locate your `nanomine_unit_converter` installation, and run the following:
```
  cp ./test_Unit_Converter.py /apps/nanomine-graph/tests/test_nanomine_unit_converter.py
  cd /apps/whyis
  python manage.py test --test test_nanomine_unit_converter
```