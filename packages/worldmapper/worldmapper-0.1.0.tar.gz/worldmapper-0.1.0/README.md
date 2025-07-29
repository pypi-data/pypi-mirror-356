# WorldMapper

A Python package for accessing comprehensive world country, state, and city information.

## Installation

```bash
pip install worldmapper


## Usage

from worldmapper import WorldMapper

# Initialize the data
wm = WorldMapper()

# Get all countries
countries = wm.get_all_countries()

# Get country by name
usa = wm.get_country_by_name("United States")

# Get country by alpha2 code
us = wm.get_country_by_alpha2("US")

# Get countries by continent
european_countries = wm.get_countries_by_continent("Europe")

# Search countries
results = wm.search_countries("samoa")