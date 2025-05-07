import requests
import json
from pathlib import Path
import pandas as pd


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
    
df = pd.read_csv("data/withodors.csv")

def get_odor(compound_name):
    row = df[df["Name"].str.lower() == compound_name.lower()]
    if not row.empty:
        return row.iloc[0]["Odor_notes"]
    else:
        raise Exception(f"Odor information not found for {compound_name}")
    
def get_cid_from_smiles(smiles):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
    response = requests.get(url)
    response.raise_for_status()
    cids = response.json().get("IdentifierList", {}).get("CID", [])
    if not cids:
        raise Exception("No CID found for the given SMILES")
    return cids[0]


    
def get_pubchem_description(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/description/JSON"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("InformationList",{}).get("Information",[])

def get_pubchem_record_sections(cid):
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data.get("Record", {}).get("Section",[])
