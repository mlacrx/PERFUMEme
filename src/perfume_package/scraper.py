import requests
import json # To read/write your database in JSON format.
from pathlib import Path # A clean way to work with file paths, cross-platform.

DATA_PATH = Path(__file__).parent / "data" / "dataset.json"

def get_smiles(compound_name): # Constructs a URL to get SMILES for a given compound name.
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound_name}/property/IsomericSMILES/JSON"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to get SMILES for {compound_name}")
    
    data = response.json() # Converts the API response from raw text into a Python dictionary.
    try:
        smiles = data["PropertyTable"]["Properties"][0]["IsomericSMILES"]
        return smiles
    except (KeyError, IndexError): # If the structure isn’t there (e.g. compound name was misspelled), this handles it gracefully.
        raise Exception("SMILES not found in response")

def load_data():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_molecule(compound_name):
    data = load_data()
    if any(entry["name"].lower() == compound_name.lower() for entry in data):
        print(f"{compound_name} already in database.")
        return
    
    try:
        smiles = get_smiles(compound_name)
        data.append({"name": compound_name, "smiles": smiles})
        save_data(data)
        print(f"Added {compound_name} with SMILES: {smiles}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    add_molecule("3,5-Dimethyl-3-cyclohexene carboxaldehyde")  # You can change this to any compound name
