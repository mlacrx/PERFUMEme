import json
from pathlib import Path
import pandas as pd
from .utils import get_smiles, get_odor

DATA_PATH = Path("data/molecules.json")

def load_data_smiles():
    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_data_smiles(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def add_molecule(compound_name):
    data = load_data_smiles()
    if any(entry["name"].lower() == compound_name.lower() for entry in data):
        print(f"{compound_name} already in database.")
        return
    
    try:
        smiles = get_smiles(compound_name)
        data.append({"name": compound_name.lower(), "smiles": smiles})
        save_data_smiles(data)
        print(f"Added {compound_name} with SMILES: {smiles}")
    except Exception as e:
        print(f"Error: {e}")

"""
if __name__ == "__main__":
    with open("data/perfume.json", "r", encoding="utf-8") as f:
        perfumes = json.load(f)

    for perfume in perfumes:
        for mol in perfume.get("molecules", []):
            add_molecule(mol)


if __name__ == "__main__":
    add_molecule("vinylidene chloride")
"""

def load_data_odor():
    with open("perfume_database.json", "r", encoding="utf-8") as f:
        return json.load(f)

def save_data_odor(data):
    with open("perfume_database.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
def add_odor_to_molecules():
    data = load_data_odor()
    for entry in data:
        if "odor" not in entry:
            try:
                odor = get_odor(entry["name"])
                odor_list = [odor_item.strip() for odor_item in odor.split(";")]
                entry["odor"] = odor_list
                print(f"Added odor for {entry['name']}: {odor}")
            except Exception as e:
                print(f"Error fetching odor for {entry['name']}: {e}")
    save_data_odor(data)


if __name__ == "__main__":
    add_odor_to_molecules()