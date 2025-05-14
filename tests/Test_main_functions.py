from src.perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace
from src.perfumeme.usable_in_perfume import usable_in_perfume
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
    Test evaporation_trace() against known reference values for linalool and ethanol.
    Checks the presence, types, and realistic ranges of returned values.
    """
    vp_linalool = 0.16
    vp_temp_linalool = 25.0
    bp_linalool = 198  #°C
    enthalpy_linalool = 51400.0

    vp_l, bp_l, vp_temp_l, enthalpy_l, path_l = evaporation_trace("linalool") 
    assert abs(bp_l - bp_linalool) < 5 
    assert vp_linalool == vp_l and vp_temp_l == vp_temp_linalool
    assert enthalpy_l == enthalpy_linalool
 






def test_usable_in_perfume():
    
    """
    Check that the function take the good information from the 3 main functions  
    """
    # Test Case 1: Molecule with an odor, safe for skin, and appropriate volatility 
    molecule_1 = "coumarin"  
    msg_1, plot_path_1 = usable_in_perfume(molecule_1)
    print(f"Test 1 - {molecule_1}: {msg_1}")
    assert "👃 Smell detected." in msg_1, "Odor detection failed"
    assert "🧴 Skin-safe." in msg_1, "Skin safety not properly evaluated"
    assert "**heart note**" in msg_1, "Note classification is incorrect"

    # Test Case 2: Molecule with no detectable odor, safe for skin 
    molecule_2 = "water"  # Water has no odor
    msg_2, plot_path_2 = usable_in_perfume(molecule_2)
    print(f"Test 2 - {molecule_2}: {msg_2}")
    assert "🚫 No smell detected." in msg_2, "Odor should not be detected"
    assert "🧴 Skin-safe." in msg_2, "Water is generally safe for skin, this test should pass"

    # Test Case 3: Molecule with an odor but not always safe for skin 
    molecule_3 = "linalool"  
    msg_3, plot_path_3 = usable_in_perfume(molecule_3)
    print(f"Test 3 - {molecule_3}: {msg_3}")
    assert "👃 Smell detected." in msg_3, "Odor should be detected"
    assert "⚠️ Not confirmed safe for skin contact." in msg_3, "Skin safety should be flagged as not confirmed"
    assert "**base note**" in msg_3, "Note classification is incorrect"
    
    # Test Case 4: Molecule with no evaporation data 
    molecule_4 = "Squalane"  
    msg_4, plot_path_4 = usable_in_perfume(molecule_4)
    print(f"Test 4 - {molecule_4}: {msg_4}")
    assert "⚠️ Insufficient volatility data to classify the note." in msg_4, "Volatility data should be insufficient for this molecule"

