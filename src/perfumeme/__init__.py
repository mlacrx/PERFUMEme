"""Determine if a molecule given by the user is present in a perfume and what are its main properties."""

from __future__ import annotations
from perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
from perfumeme.perfume_molecule import match_mol_to_odor, match_molecule_to_perfumes,odor_molecule_perfume, what_notes
from perfumeme.utils import get_smiles,get_pubchem_record_sections,get_cid_from_smiles,get_odor,get_pubchem_description,resolve_input_to_smiles_and_cid
from perfumeme.scraper import load_data_smiles, save_data_smiles,add_molecule,load_data_odor,save_data_odor,add_odor_to_molecules
from perfumeme.usable_function import usable_in_perfume

__version__ = "1.1.0"
import os
import shutil
from pathlib import Path
def _copy_data_file(filename: str):
    """Copies a data file from project data/ to ~/.perfumeme/ if it doesn't exist."""
    user_data_dir = Path.home() / ".perfumeme"
    user_data_dir.mkdir(parents=True, exist_ok=True)

    target = user_data_dir / filename
    if not target.exists():
        try:
            source = Path(__file__).resolve().parents[2] / "data" / filename
            if source.exists():
                shutil.copy(source, target)
            else:
                print(f"⚠️ Warning: '{filename}' not found in data/")
        except Exception as e:
            print(f"⚠️ Could not copy '{filename}': {e}")

_copy_data_file("perfumes.json")
_copy_data_file("molecules.json")
