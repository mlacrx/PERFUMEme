from src.perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
import pytest


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
    Test evaporation_trace() against known reference values for linalool and coumarin.
    Checks the presence, types, and realistic ranges of returned values.
    """
    vp_linalool = 0.16
    vp_temp_linalool = 25
    bp_linalool = 198  #°C
    enthalpy_linalool = 51400.0

    vp_l, bp_l, vp_temp_l, enthalpy_l, path_l = evaporation_trace("linalool") 
    assert abs(bp_l - bp_linalool) < 5 
    assert vp_linalool == vp_l and vp_temp_l == vp_temp_linalool
    assert enthalpy_l == enthalpy_linalool

    vp_coumarin = 0.01
    vp_temp_coumarin = 47
    bp_coumarin = 297.78
    enthalpy_coumarin = None

    vp_c, bp_c, vp_temp_c, enthalpy_c, path_c = evaporation_trace("coumarin")
    assert vp_coumarin == vp_c
    assert abs (bp_c-bp_coumarin)<5
    assert vp_temp_c == vp_temp_coumarin
    assert enthalpy_coumarin == enthalpy_c
