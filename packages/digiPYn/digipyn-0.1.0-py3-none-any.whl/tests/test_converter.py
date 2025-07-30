import pytest
from digiPYn import DigiPinConverter
import requests # Keep this import for monkeypatching

def test_digipin_from_lat_long_valid():
    test_cases = [
        ((28.6139, 77.2090), "39J-438-TJC7"),
        ((19.0760, 72.8777), "4FK-595-8823"),
        ((17.31728105, 78.69983558), "427-KK4-C2MT")
    ]

    for coords, expected in test_cases:
        result = DigiPinConverter.get_digipin_from_lat_long(*coords)
        assert result == expected, f"Failed for {coords}. Expected {expected}, got {result}"

def test_digipin_from_lat_long_invalid():
    with pytest.raises(ValueError):
        DigiPinConverter.get_digipin_from_lat_long(50, 50)  # Latitude 50 is > maxLat (38.5)
    with pytest.raises(ValueError):
        DigiPinConverter.get_digipin_from_lat_long(20, 50)  # Longitude 50 is < minLon (63.5)
    with pytest.raises(ValueError):
        DigiPinConverter.get_digipin_from_lat_long("abc", 77.2)  # Non-numeric input


def test_lat_long_from_digipin_valid(): # Removed 'converter' argument
    test_cases = [
        ("39J-438-TJC7", (28.6139, 77.2090)),
        ("4FK-595-8823", (19.0760, 72.8777)),
        ("4P3-JK8-52C9", (12.9716, 77.5946))
    ]

    tolerance = 0.00005

    for digipin, expected in test_cases:
        lat, lon = DigiPinConverter.get_lat_long_from_digipin(digipin)
        assert pytest.approx(lat, abs=tolerance) == expected[0]
        assert pytest.approx(lon, abs=tolerance) == expected[1]


def test_lat_long_from_digipin_invalid():
    with pytest.raises(ValueError):
        DigiPinConverter.get_lat_long_from_digipin("ABC123")  # Too short

    with pytest.raises(ValueError):
        DigiPinConverter.get_lat_long_from_digipin("FCM-9KP-6LT-EXTRA")  # Too long

    with pytest.raises(ValueError):
        DigiPinConverter.get_lat_long_from_digipin("XYZ-123-456z")  # Invalid chars


def test_address_to_digipin(monkeypatch): # Removed 'converter' argument
    # Mock the API call for address conversion
    class MockResponse:
        @staticmethod
        def json():
            return {
                "status": "OK",
                "results": [{
                    "geometry": {
                        "location": {
                            "lat": 28.6139,
                            "lng": 77.2090
                        }
                    }
                }]
            }
        # Add raise_for_status method
        def raise_for_status(self):
            pass # Do nothing for a successful mock

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)

    result = DigiPinConverter.get_digipin_from_address("New Delhi, India")
    assert result == "39J-438-TJC7"


def test_address_to_digipin_api_failure(monkeypatch): # Removed 'converter' argument
    # Test API failure cases
    class MockFailedResponse:
        @staticmethod
        def json():
            return {
                "status": "ZERO_RESULTS",
                "error_message": "No results found"
            }

        def raise_for_status(self):
            pass

    def mock_get(*args, **kwargs):
        return MockFailedResponse()

    monkeypatch.setattr("requests.get", mock_get)

    # Call the static method directly on the class
    result = DigiPinConverter.get_digipin_from_address("Invalid Address")
    assert result is None