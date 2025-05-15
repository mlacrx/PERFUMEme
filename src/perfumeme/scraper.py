import json
from pathlib import Path
import pandas as pd
from .utils import get_smiles, get_odor

DATA_PATH = Path("data/molecules.json")

def load_data_smiles():
    """
    Loads molecule data from the local SMILES JSON database.

    Returns:
        list[dict]: A list of molecule entries, each represented as a dictionary.
        Returns an empty list if the file does not exist.

    Notes:
        The data is expected to be located at 'data/molecules.json'.
    """

    if DATA_PATH.exists():
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data_smiles(data):
    """
    Saves the given molecule data to the local SMILES JSON database.

    Args:
        data (list[dict]): A list of dictionaries representing molecule data to be saved.

    Notes:
        The data is saved to 'data/molecules.json' with UTF-8 encoding and indentation.
    """

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def add_molecule(compound_name):
    """
    Adds a new molecule and its SMILES representation to the local database.

    If the molecule already exists (case-insensitive match), it is not added again.

    Args:
        compound_name (str): The name of the compound to add.

    Raises:
        Exception: If an error occurs while retrieving the SMILES using `get_smiles`.

    Notes:
        This function uses `get_smiles` from the .utils module.
        The database is stored in 'data/molecules.json'.
    """

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


if __name__ == "__main__":
    with open("data/perfumes.json", "r", encoding="utf-8") as f:
        perfumes = json.load(f)

    for perfume in perfumes:
        for mol in perfume.get("molecules", []):
            add_molecule(mol)


def load_data_odor():
    """
    Loads perfume data from the local JSON file.

    Returns:
        list[dict]: A list of perfume entries from 'perfumes.json'.

    Notes:
        This function directly loads 'perfumes.json' from the working directory.
    """
    with open("perfumes.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_data_odor(data):
    """
    Saves perfume data to the local 'perfumes.json' file.

    Args:
        data (list[dict]): A list of perfume entries to save.

    Notes:
        The file is saved with UTF-8 encoding and indentation for readability.
    """
    with open("perfumes.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def add_odor_to_molecules():
    """
    Adds odor descriptors to perfume entries that do not yet have them.

    For each perfume without an 'odor' field, the function retrieves the odor string using
    `get_odor`, splits it into a list, and assigns it to the perfume entry.

    Raises:
        Exception: If an error occurs while retrieving odor data for a perfume.

    Notes:
        Modifies the 'perfumes.json' file in place.
        Relies on `get_odor` from the .utils module.
    """
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