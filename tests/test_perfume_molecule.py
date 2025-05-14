from src.perfumeme.perfume_molecule import combination, match_mol_to_odor, match_molecule_to_perfumes
import pytest 

def test_match_molecule_to_perfume():
    """
    Check if the fonction is effective to match molecule and perfume 
    """
    #With a molecule present in perfumes
    molecule = "methyl anthranilate"
    perfumes = ["Alien by Mugler","La nuit de l'Homme by Yves Saint-Laurent", "Libre by Yves Saint Laurent"]
    assert match_molecule_to_perfumes(molecule) == perfumes

    #With a molecule not used in perfumes
    molecule_1 = "Iron"
    expected_output = "No perfumes found containg this molecule."
    assert match_molecule_to_perfumes(molecule_1) ==  expected_output

def test_match_mol_to_odor():
    """
    Check if the fonction associate the molecules with the good flagrances
    """
    #with a molecule in the database
    molecule_1 = "coumarin"
    expected_output1 = ["coumarinic","green","hay","mown","spicy","sweet","tonka","vanilla"]
    assert match_mol_to_odor(molecule_1) == expected_output1
    #with a molecule not in the database
    molecule_2 = "gold"
    expected_output2 = "Molecule not found."
    assert match_mol_to_odor(molecule_2) == expected_output2
    #With a molecule in the database but has no odor
    molecule_3  = "butylene glycol"
    expected_output3 = "No odors found for this molecule."
    assert match_mol_to_odor(molecule_3) == expected_output3