from perfumeme.perfume_molecule import odor_molecule_perfume, match_mol_to_odor, match_molecule_to_perfumes, what_notes
import pytest 

def test_match_molecule_to_perfume():
    """
    Check if the fonction is effective to match molecule and perfume 
    """
    #With a molecule present in perfumes
    molecule = "methyl anthranilate"
    perfumes = ["Alien by Mugler","La nuit de l'Homme by Yves Saint-Laurent", "Libre by Yves Saint-Laurent"]
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

def test_odor_molecule_perfume():
    """
    checks that the odor_molecule_perfume function works correctly, even with molecules that have no associated odours or perfumes, and does not crash if the molecule does not exist or is not in its database.
    """
    #Test with a molecule present in some perfumes
    expected_result = odor_molecule_perfume("methyl anthranilate")
    assert expected_result["perfumes"] == ["Alien by Mugler","La nuit de l'Homme by Yves Saint-Laurent", "Libre by Yves Saint-Laurent"]
    assert expected_result["odors"] == ["chocolate","coffee","floral","flower","fruity","grape","grapefruit","herbaceous","jasmin","lemon","lime","medicinal","musty","neroli","orange","powdery","strawberry","sweet"]

    #Test with a molecule not used in per 
    expected_res = odor_molecule_perfume("Iron")
    assert expected_res == "No perfumes found containg this molecule."

def test_what_notes():
    """
    Check if the function is effective to match perfume and notes
    """
    #Test with a perfume present in the database
    perfume = "La nuit de l'Homme"
    note_type = "top"
    expected_output = ["SAGE ESSENCE"]
    assert what_notes(perfume, note_type) == expected_output

    #Test with a perfume not in the database
    perfume_1 = "Iron"
    expected_output_1 = "Perfume not found."
    assert what_notes(perfume_1, note_type) == expected_output_1

    #Test with wrong note type
    perfume_2 = "Libre"
    note_type_2 = "middle"
    assert what_notes(perfume_2, note_type_2) == "Invalid note type. Please use 'top', 'heart', or 'base'."