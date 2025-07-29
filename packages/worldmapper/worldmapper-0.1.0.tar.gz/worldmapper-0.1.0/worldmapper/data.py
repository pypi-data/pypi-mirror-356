import json
import os
from typing import Dict, List, Optional, Any

class WorldMapper:
    """
    A class to access world country, state, and city data.
    """
    
    def __init__(self):
        """Initialize WorldMapper with the JSON data."""
        self._data = self._load_data()
    
    def _load_data(self) -> List[Dict[str, Any]]:
        """Load data from the world.json file."""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, 'world.json')
        
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def get_all_countries(self) -> List[Dict[str, Any]]:
        """Get all countries data."""
        return self._data
    
    def get_country_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Get country data by name."""
        for country in self._data:
            if country.get('name', '').lower() == name.lower():
                return country
        return None
    
    def get_country_by_alpha2(self, alpha2: str) -> Optional[Dict[str, Any]]:
        """Get country data by alpha2 code."""
        for country in self._data:
            if country.get('alpha2', '').lower() == alpha2.lower():
                return country
        return None
    
    def get_country_by_alpha3(self, alpha3: str) -> Optional[Dict[str, Any]]:
        """Get country data by alpha3 code."""
        for country in self._data:
            if country.get('alpha3', '').lower() == alpha3.lower():
                return country
        return None
    
    def get_countries_by_continent(self, continent: str) -> List[Dict[str, Any]]:
        """Get all countries in a specific continent."""
        return [
            country for country in self._data
            if country.get('continent', '').lower() == continent.lower()
        ]
    
    def get_countries_by_region(self, region: str) -> List[Dict[str, Any]]:
        """Get all countries in a specific region."""
        return [
            country for country in self._data
            if country.get('region', '').lower() == region.lower()
        ]
    
    def get_countries_by_currency(self, currency: str) -> List[Dict[str, Any]]:
        """Get all countries using a specific currency."""
        return [
            country for country in self._data
            if country.get('currency', '').lower() == currency.lower()
        ]
    
    def search_countries(self, query: str) -> List[Dict[str, Any]]:
        """Search countries by name, capital, or other fields."""
        query = query.lower()
        results = []
        
        for country in self._data:
            # Search in name, capital, alpha codes
            searchable_fields = [
                country.get('name', ''),
                country.get('capital', ''),
                country.get('alpha2', ''),
                country.get('alpha3', '')
            ]
            
            if any(query in field.lower() for field in searchable_fields):
                results.append(country)
        
        return results