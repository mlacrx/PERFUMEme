import requests
import json
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

DATA_PATH = Path("/Users/lilia/Documents/EPFL/BA.4/prog/project/PERFUMEme/data/smiles.json")

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
"""
def get_odor(compound_name):
    search_url = "https://odor.rpbs.univ-paris-diderot.fr/search"
    search_data = {"query": compound_name}
    search_response = requests.post(search_url, data=search_data)
    if search_response.status_code != 200:
        raise Exception(f"Failed to get search results for {compound_name}")
    
    # Parse the search results to find the correct molecule link
    soup = BeautifulSoup(search_response.text, "html.parser")
    result_links = soup.find_all("a", class_="result-link")  # Adjust selector based on the website's structure
    for link in result_links:
        if link.get_text(strip=True).lower() == compound_name.lower():
            molecule_url = f"https://odor.rpbs.univ-paris-diderot.fr{link['href']}"
            break
    else:
        raise Exception(f"No exact match found for {compound_name}")
    
    # Fetch the molecule page to extract odor information
    molecule_response = requests.get(molecule_url)
    if molecule_response.status_code != 200:
        raise Exception(f"Failed to fetch molecule page for {compound_name}")
    
    molecule_soup = BeautifulSoup(molecule_response.text, "html.parser")
    odor_section = molecule_soup.find("div", class_="odor-description")  # Adjust selector based on the website's structure
    if odor_section:
        odor_info = odor_section.get_text(strip=True)
        return odor_info
    else:
        raise Exception(f"Odor information not found for {compound_name}")

"""
df = pd.read_excel("/Users/lilia/Documents/EPFL/BA.4/prog/project/Pred-O3_BDD_04-03-2024.xlsx", engine="openpyxl")

def get_odor(compound_name):
    row = df[df["Name"].str.lower() == compound_name.lower()]
    if not row.empty:
        return row.iloc[0]["Odor_notes"]
    else:
        raise Exception(f"Odor information not found for {compound_name}")
    
def add_odor_to_molecules():
    data = load_data()
    for entry in data:
        if "odor" not in entry:  # Skip if odor information is already present
            try:
                odor = get_odor(entry["name"])
                odor_list = [odor_item.strip() for odor_item in odor.split(";")]
                entry["odor"] = odor_list
                print(f"Added odor for {entry['name']}: {odor}")
            except Exception as e:
                print(f"Error fetching odor for {entry['name']}: {e}")
    save_data(data)


if __name__ == "__main__":
    add_odor_to_molecules()