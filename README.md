# MakeOpenData Projects

A [Data Package](https://frictionlessdata.io/data-packages/) collecting hackathon projects from the (no londer actively maintained) [make.opendata.ch wiki](https://make.opendata.ch/wiki), which is a [Dokuwiki](https://github.com/splitbrain/dokuwiki).

The dataset includes descriptions of activities that took place between approximately 2011-2018. Since 2016 we have been using a different documentation platform for hackathons, the data from which is collected at https://github.com/opendatach/hackopendata-archive

## Updating

Install a local Python environment using pip or Pipenv and run `scraper.py` to generate a new SQLite database.

The data is automatically updated with a scraper that runs on [Morph](https://morph.io). See https://morph.io/loleg/dokuwiki-projects

## License

The wiki project content is - unless otherwise noted - licensed under the [CC Attribution-Share Alike 4.0 International](http://creativecommons.org/licenses/by-sa/4.0/) license.

This Data Package itself is made available by its maintainers under the [Public Domain Dedication and License v1.0](http://www.opendatacommons.org/licenses/pddl/1.0/), a copy of the full text of which is in [LICENSE.md](LICENSE.md).
