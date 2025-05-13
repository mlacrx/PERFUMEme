from src.perfume_package.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
from src.perfume_package.usable_in_perfume import usable_in_perfume
from src.perfume_package.utils import get_smiles, get_cid_from_smiles
import pytest



def test_get_smiles():
    """
    Check if the smile given is associated to the good molecule
    """
    compound_name = "geraniol"
    expected_smiles = "CC(=CCC/C(=C/CO)/C)C"  # Le SMILES attendu pour geraniol
    smiles = get_smiles(compound_name)
    assert smiles == expected_smiles


def test_get_cid_from_smiles():
    """
    Check if the cid given corresponds to the SMILE and therefore to the good molecule 
    """
    smile = "CC(=CCC/C(=C/CO)/C)C"
    expected_cid = "637566"
    cid = get_cid_from_smiles(smile)
    assert str(cid) == expected_cid


def test_has_a_smell():
    """
    check that a molecule odorous/odorless is detected corectly and that an invalid entry do not crash the fonction
    """
    #Test with known odorous molecule SMILE
    assert has_a_smell("CC(=CCC/C(=C/CO)/C)C") is True #geraniol
    #Test with known odorous molecule Name
    assert has_a_smell("geraniol") is True 

    #Test with known odourless molecule SMILE and name: Water
    assert has_a_smell("O") is False 
    assert has_a_smell("Water") is False

    #Test with invalid smile or name 
    assert has_a_smell("XYZ") is False 
    


def test_is_toxic_skin():
    """
    Check that toxic and non-toxic molecules are identified as such and doesn't crash with an incorrect name/smile
    """
    #Test with known toxic molecule
    assert is_toxic_skin("C1=CC(=CC=C1O)O") is True 
    #Test with known toxic molecule
    assert is_toxic_skin("Hydroquinone") is True 

    #Test with known non toxic molecule SMILE
    assert is_toxic_skin("O") is False  
    #Test with known non toxic molecule name
    assert is_toxic_skin("Water") is False 


    #Test with invalid smile/name
    assert is_toxic_skin("XYZ") is False

def test_evaporation_trace():
    """
    Check that the function returns numeric values or None for each molecule and doesn't crash
    """
    # Test with known molecule (e.g., Ethanol)
    vp, bp, temp, enthalpy, save_path = evaporation_trace("CCO")  
  
    assert isinstance(vp, (int,float, type(None))) # Vapor Pressure should be float or None
    assert isinstance(bp, (int,float, type(None))) # Boiling Point should be float or None
    assert isinstance(temp, (int,float, type(None))) # Temperature should be float or None
    assert isinstance(enthalpy, (int,float, type(None))) # Enthalpy should be float or None
    assert isinstance(save_path, (str, type(None))) # Save_path should be str or None 



"""
def test_usable_in_perfume():

    Check that the function take the good information from the 3 main functions and that molecules are classified as usable or not  

    #With a molecule used in perfume
    assert usable_in_perfume("Linalool") is True #test with linalool
    #with a molecule not usable in perfume beacause doesn't have a smell
    assert usable_in_perfume("Glycerol") is False
    #with a molecule not usable beacause of its toxicity 
    assert usable_in_perfume("Hydrogen Cyanide") is False

"""

