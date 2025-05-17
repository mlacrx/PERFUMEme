"""Determine if a molecule given by the user is present in a perfume and what are its main properties."""

from __future__ import annotations
from perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
from perfumeme.perfume_molecule import match_mol_to_odor, match_molecule_to_perfumes,odor_molecule_perfume, what_notes
from perfumeme.utils import get_smiles,get_pubchem_record_sections,get_cid_from_smiles,get_odor,get_pubchem_description,resolve_input_to_smiles_and_cid
from perfumeme.scraper import load_data_smiles, save_data_smiles,add_molecule,load_data_odor,save_data_odor,add_odor_to_molecules
from perfumeme.usable_function import usable_in_perfume

__version__ = "1.0.7"