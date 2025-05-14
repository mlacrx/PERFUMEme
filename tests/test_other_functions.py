from src.perfumeme.utils import resolve_input_to_smiles_and_cid , get_odor, get_smiles, get_cid_from_smiles
import pandas as pd
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


def test_resolve_input_to_smiles_and_cid():
    """
    Checks that the function returns the correct (SMILES, CID),
    whether a name or a SMILES string is inserted.
    """
    expected_smiles = "CC(CCC=C(C)C)CCO"
    expected_cid = 8842

    # if the name of the molecule is the input
    compound = "Citronellol "
    smiles, cid = resolve_input_to_smiles_and_cid(compound)
    assert smiles == expected_smiles
    assert cid == expected_cid

    # if the Smile is the input
    compound_s = "CC(CCC=C(C)C)CCO"
    smiles, cid = resolve_input_to_smiles_and_cid(compound_s)
    assert smiles == expected_smiles
    assert cid == expected_cid


"""def test_get_odor(monkeypatch):
    # Create a fake DataFrame
    fake_df = pd.DataFrame({
        "Name": ["Citronellol"],
        "Odor_notes": ["floral;rose;fresh"]
    })

    # Patch the global df inside your module
    monkeypatch.setattr(perfumeme.utils.py, "df", fake_df)

    # Now test normally
    result = get_odor("citronellol")
    assert result == "floral;rose;fresh"
"""