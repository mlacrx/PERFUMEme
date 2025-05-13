import json
from pathlib import Path

def match_molecule_to_perfumes(mol):
    """
    gives a list of perfumes which contain the molecule
    """
    DATA_PATH_PERF = Path("data/perfume.json")
    if DATA_PATH_PERF.exists():
        with open(DATA_PATH_PERF, "r", encoding="utf-8") as f:
            perfumes = json.load(f)
    else:
        return []
    
    mol_upper = mol.upper()
    matched_perfumes = []
    for perfume in perfumes:
        if mol_upper in perfume.get("molecules", []):
            matched_perfumes.append(f"{perfume["name"]} by {perfume["brand"]}")

    if matched_perfumes == []:
        return f"No perfumes found containg this molecule."
    else:
        return matched_perfumes


def match_mol_to_odor(mol):
    DATA_PATH_MOL = Path("data/molecules.json")
    if DATA_PATH_MOL.exists():
        with open(DATA_PATH_MOL, "r", encoding="utf-8") as f:
            molecules = json.load(f)
    else:
        return []
    
    mol_lower = mol.lower()
    
    matched_odors = []
    for molecule in molecules:
        if mol_lower == molecule.get("name", []).lower():
            matched_odors.append(molecule.get("odor", []))
            return molecule.get("odor")
    
    if matched_odors == []:
        if mol not in molecule.get("name", []):
            return f"Molecule not found."
        else:
            return f"No odors found for this molecule."


def combination(mol):
    """
    gives a dictionnary of perfumes which contain the molecule and the odor the molecule give to the perfume
    """
    dict_mol = {}
    if match_molecule_to_perfumes(mol) == f"No perfumes found containg this molecule." or match_mol_to_odor(mol) == f"Molecule not found.":
        return f"No perfumes found containg this molecule."
    else:
        dict_mol["perfumes"]= match_molecule_to_perfumes(mol)
        dict_mol["odors"]= match_mol_to_odor(mol)
        return dict_mol