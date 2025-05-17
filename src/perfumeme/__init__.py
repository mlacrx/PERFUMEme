"""Determine if a molecule given by the user is present in a perfume and what are its main properties."""

from __future__ import annotations
from perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
from perfumeme.perfume_molecule import match_mol_to_odor, match_molecule_to_perfumes,odor_molecule_perfume, what_notes
from perfumeme.utils import get_smiles,get_pubchem_record_sections,get_cid_from_smiles,get_odor,get_pubchem_description,resolve_input_to_smiles_and_cid
from perfumeme.scraper import load_data_smiles, save_data_smiles,add_molecule,load_data_odor,save_data_odor,add_odor_to_molecules
from perfumeme.usable_function import usable_in_perfume

__version__ = "1.2.0"
import os
import requests
from pathlib import Path
def _download_if_missing(filename: str, url: str):
    """Download a data file to ~/.perfumeme if it doesn't exist."""
    user_data_dir = Path.home() / ".perfumeme"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    target = user_data_dir / filename

    if not target.exists():
        try:
            print(f"📥 Downloading {filename} from {url}...")
            r = requests.get(url)
            r.raise_for_status()
            with open(target, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"❌ Failed to download {filename}: {e}")

_perfumes_url = "https://raw.githubusercontent.com/mlacrx/PERFUMEme/main/data/perfumes.json"
_molecules_url = "https://raw.githubusercontent.com/mlacrx/PERFUMEme/main/data/molecules.json"

_download_if_missing("perfumes.json", _perfumes_url)
_download_if_missing("molecules.json", _molecules_url)
