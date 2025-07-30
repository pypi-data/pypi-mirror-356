# Copyright 2025 Department of Posts
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Author: Kawsshikh Sajjana Gandla
# Email: kawsshikhsajjan7@gmail.com
# Date: June 18, 2025
#
# This file contains adaptations from original work by Department of Posts,
# with additional contributions and modifications by Kawsshikh Sajjana Gandla.

# [Your Python code starts here]



import math
import requests
import json
from .config import get_api_key, delete_api_key

class DigiPinConverter:
    # Default Grid assigned by GOI
    DIGIPIN_GRID = [
        ['F', 'C', '9', '8'],
        ['J', '3', '2', '7'],
        ['K', '4', '5', '6'],
        ['L', 'M', 'P', 'T']
    ]

    GRID_1D = [item for sublist in DIGIPIN_GRID for item in sublist]

    # Pre-calculated character to index map, available at the class level
    _char_to_index_map = {char: i for i, char in enumerate(GRID_1D)}

    # Default Bounds assigned by GOI
    BOUNDS = {
        "minLat": 2.5,
        "maxLat": 38.5,
        "minLon": 63.5,
        "maxLon": 99.5
    }

    # Removed __init__ as it's no longer necessary for static method usage.
    # If there was truly instance-specific setup, you would keep it.

    @staticmethod
    def get_digipin_from_lat_long(lat, long):
        """
        Converts geographical coordinates (latitude, longitude) to a DIGIPIN.
        This is now a static method, callable directly on the class.

        Args:
            lat (float): Latitude.
            long (float): Longitude.

        Returns:
            str: DIGIPIN - A 10 digit unique identifier of location.

        Raises:
            ValueError: If input latitude or longitude is not a number,
                        or if coordinates are out of the predefined bounds.
        """
        if not isinstance(lat, (int, float)) or not isinstance(long, (int, float)):
            raise ValueError("Latitude and Longitude must be numeric.")

        # Access class-level BOUNDS directly
        min_lat, max_lat = DigiPinConverter.BOUNDS["minLat"], DigiPinConverter.BOUNDS["maxLat"]
        min_lon, max_lon = DigiPinConverter.BOUNDS["minLon"], DigiPinConverter.BOUNDS["maxLon"]

        if not (min_lat <= lat <= max_lat):
            raise ValueError(f"Latitude {lat} is out of bounds. Must be between {min_lat} and {max_lat}.")
        if not (min_lon <= long <= max_lon):
            raise ValueError(f"Longitude {long} is out of bounds. Must be between {min_lon} and {max_lon}.")

        digipin_parts = []
        current_min_lat, current_max_lat = min_lat, max_lat
        current_min_lon, current_max_lon = min_lon, max_lon

        for level in range(1, 11):
            lat_div = (current_max_lat - current_min_lat) / 4
            long_div = (current_max_lon - current_min_lon) / 4

            # Calculate row and column
            row = min(3, max(0, int((current_max_lat - lat) / lat_div)))
            col = min(3, max(0, int((long - current_min_lon) / long_div)))

            # Access class-level DIGIPIN_GRID directly
            digipin_parts.append(DigiPinConverter.DIGIPIN_GRID[row][col])

            if level == 3 or level == 6:
                digipin_parts.append('-')

            # Update bounds for the next level
            new_max_lat = current_max_lat - row * lat_div
            new_min_lat = new_max_lat - lat_div

            new_min_lon = current_min_lon + col * long_div
            new_max_lon = new_min_lon + long_div

            current_min_lat, current_max_lat = new_min_lat, new_max_lat
            current_min_lon, current_max_lon = new_min_lon, new_max_lon

        return "".join(digipin_parts)

    @staticmethod
    def get_lat_long_from_digipin(digipin):
        """
        Converts a DIGIPIN to its approximate geographical coordinates (latitude, longitude).
        Returns the center point of the DIGIPIN's smallest defined area.
        This is now a static method, callable directly on the class.

        Args:
            digipin (str): The DIGIPIN string.

        Returns:
            tuple: A tuple (latitude, longitude) representing the center of the DIGIPIN area.

        Raises:
            ValueError: If the digipin is invalid (length, characters).
        """
        cleaned_digipin = digipin.replace('-', '').upper()
        if len(cleaned_digipin) != 10:
            raise ValueError("Invalid digipin: it should have 10 alphanumeric characters (excluding hyphens).")

        # Access class-level BOUNDS and _char_to_index_map directly
        min_lat, max_lat = DigiPinConverter.BOUNDS["minLat"], DigiPinConverter.BOUNDS["maxLat"]
        min_lon, max_lon = DigiPinConverter.BOUNDS["minLon"], DigiPinConverter.BOUNDS["maxLon"]

        current_min_lat, current_max_lat = min_lat, max_lat
        current_min_lon, current_max_lon = min_lon, max_lon

        for pin_char in cleaned_digipin:
            try:
                idx = DigiPinConverter._char_to_index_map[pin_char]
            except KeyError:
                raise ValueError(f"Invalid digipin character: '{pin_char}' not found in the grid.")

            row = idx // 4
            col = idx % 4

            lat_div = (current_max_lat - current_min_lat) / 4
            long_div = (current_max_lon - current_min_lon) / 4

            # Update bounds based on the character's row and column
            new_max_lat = current_max_lat - row * lat_div
            new_min_lat = new_max_lat - lat_div

            new_min_lon = current_min_lon + col * long_div
            new_max_lon = new_min_lon + long_div

            current_min_lat, current_max_lat = new_min_lat, new_max_lat
            current_min_lon, current_max_lon = new_min_lon, new_max_lon

        # Calculate the center of the final, smallest cell
        lat = round((current_min_lat + current_max_lat) / 2, 6)
        lon = round((current_min_lon + current_max_lon) / 2, 6)
        return lat, lon

    @staticmethod
    def get_digipin_from_address(address):
        """
        Converts an address to its DIGIPIN using the Google Geocoding API.
        This is now a static method, callable directly on the class.

        Args:
            address (str): The geographical address string.

        Returns:
            str: DIGIPIN - A 10 digit unique identifier of location.
                 Returns None if geocoding fails.

        Raises:
            ValueError: If the API_KEY is not set.
        """
        API_KEY = get_api_key()

        if not API_KEY:
            raise ValueError("API_KEY must be set. Please ensure it's configured in .config.")

        base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        params = {
            "address": address,
            "key": API_KEY
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            if data["status"] == "OK":
                location = data["results"][0]["geometry"]["location"]
                # Call the static method directly on the class
                DIGIPIN = DigiPinConverter.get_digipin_from_lat_long(location["lat"], location["lng"])
                return DIGIPIN
            else:
                print(f"Error from Google Geocoding API: {data['status']} - {data.get('error_message', 'No error message provided.')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Network or request error during Google Geocoding API call: {e}")
            return None
        except json.JSONDecodeError:
            print(f"Failed to parse JSON response from Google Geocoding API.")
            return None
        except IndexError:
            print(f"No results found for address: '{address}'.")
            return None