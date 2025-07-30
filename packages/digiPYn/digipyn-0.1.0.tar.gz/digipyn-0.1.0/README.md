
# DigiPinConverter

A Python library to convert geographic coordinates (latitude/longitude) to DIGIPIN — a unique 10-character grid-based location identifier — and vice versa. It also supports address-to-DIGIPIN conversion using the Google Maps Geocoding API.

---

## 🚀 Features

- Convert **latitude/longitude → DIGIPIN**
- Convert **DIGIPIN → latitude/longitude**
- Convert **Address → DIGIPIN** (via Google Maps API)
- Based on Government of India’s standard 4x4 DIGIPIN grid system
- Lightweight and easy to integrate

---

## 📦 Installation

```bash
pip install digiPYn
```



> Use the `-e` flag if you’re developing or testing locally.
```bash
pip install -e .
```
---

## 🧠 Usage

```python
from digiPYn import DigiPinConverter

# Initialize the converter
converter = DigiPinConverter()

# Convert coordinates to DigiPIN
digipin = converter.get_digipin_from_lat_long(15.00236, 78.08250)
print("DigiPIN:", digipin)

# Convert DigiPIN to coordinates
lat, lon = converter.get_lat_long_from_digipin(digipin)
print("Coordinates:", lat, lon)

# Convert address to DigiPIN (Google Maps API key required)
digipin_from_address = converter.get_digipin_from_address("Kurnool, India")
print("Address DigiPIN:", digipin_from_address)
```

---

## 🔐 API Key Configuration

To use the address-to-DIGIPIN conversion feature, a **Google Maps Geocoding API key** is required.

### 🔄 How It Works

- The **first time** the Google Maps API is called, the user will be prompted to input their API key.
- The key is then securely saved in a `config.json` file at a platform-specific location:
  - **Windows**: `%APPDATA%/digipin_converter/config.json`
  - **Linux/macOS**: `~/.config/digipin_converter/config.json`

This behavior is handled automatically by the library's `config.py` module.

### 🧼 Delete the API Key

To remove the saved API key at any time, simply call:

```python
from digipYn.config import delete_api_key
delete_api_key()
```

This will delete the `config.json` file storing your credentials.

### 💡 Pro Tip (Optional Manual Setup)

If you prefer, you can also manually set the environment variable `GOOGLE_API_KEY` before running your script:

```bash
export GOOGLE_API_KEY="your_key_here"  # Linux/macOS
set GOOGLE_API_KEY=your_key_here       # Windows CMD
$env:GOOGLE_API_KEY="your_key_here"    # Windows PowerShell
```

The library will prioritize this over the saved config file.

---

## 📁 Project Structure

```
digipin_converter/
├── digipin_converter/
│   ├── __init__.py
│   ├── converter.py       # DigiPinConverter class
│   └── config.py          # Handles API key config
├── tests/
│   └── test_converter.py  # Unit tests
├── setup.py
├── pyproject.toml
└── README.md
```

---

## ✅ Dependencies

- `requests`

Install with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Running Tests

Basic example using `pytest`:

```bash
pytest tests/
```

---

## 📃 License

This project is open-source and available under the MIT License.

---

## 📚 References

- This library is based on the DIGIPIN grid logic developed by [CEPT-VZG](https://github.com/CEPT-VZG/digipin).
  You can find the original implementation [here](https://github.com/CEPT-VZG/digipin).

---

## 🙏 Credits

- DIGIPIN grid logic adapted from the original work by [CEPT-VZG](https://github.com/CEPT-VZG/digipin).

---

## ✍️ Author

Created by **Kawsshikh Sajjana Gandla**  
Feel free to contribute or report issues.


