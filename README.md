# EIA Data Fetcher

This Python script allows users to fetch large datasets from the [U.S. Energy Information Administration (EIA)](https://www.eia.gov/) API using modular configuration files. It supports pagination, environment-based API key handling, and customizable outputs.

---

## Features

- Loads EIA API key securely from a `.env` file  
- Accepts JSON-based config files (URL + request body) based on the X-offset headers from EIA's API v2  
- Handles pagination automatically using `offset` and `length`  
- Saves results to a .CSV  

---

## 📂 Project Structure

```
top-level-folder/
├── fetch_eia.py                 # Main script
├── configs/
│   └── nc_plant_generation.json  # Sample API request config
├── outputs/
│   └── nc_plant_generation.csv   # Data output stored here
├── .env                         # Environment variables (not tracked in Git)
└── README.md
```

---

## 🔧 Setup

### 1. 📦 Install dependencies

Create a virtual environment and install the packages in `requirements.txt` file
```bash
pip install -r requirements.txt
```

---

### 2. 🔐 Create a `.env` file

In the root directory of your project, create a `.env` file containing your API key. Your API key can be obtained from the EIA website.

```env
EIA_API_KEY=your_api_key_here
```

> ⚠️ Do **not** share this file or commit it to GitHub. Add `.env` to your `.gitignore`.

---

### 3. Create config JSON file based on desired data from EIA

Some manual work here in assembling the .JSON file based on the header provided by the data path of interest. Store the target url and header (contains specific query information) in a JSON file.

Store the JSON file (e.g. `configs/nc_plant_generation.json`). Some examples are provided in the repo and also here:

```json
{
  "url": "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data",
  "header": {
    "frequency": "local-hourly",
    "data": ["value"],
    "facets": {},
    "start": "2019-01-01T00-05:00",
    "end": "2020-01-01T00-05:00",
    "sort": [{ "column": "period", "direction": "desc" }],
    "offset": 0,
    "length": 5000
  }
}
```

You can generate this structure using EIA’s [API query builder](https://www.eia.gov/opendata/browser/).

---

## 📈 Running the Script

```bash
python fetch_eia.py
```

May include a CLI and progress tracker in future updates to this repo.  

---

## Final Notes

- Data is written in chunks to handle large responses.
- The script **overwrites** the output CSV if it exists.

---