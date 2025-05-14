from src.perfumeme.usable_in_perfume import usable_in_perfume
import pytest

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
    assert "**base note**" in msg_1, "Note classification is incorrect"

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

