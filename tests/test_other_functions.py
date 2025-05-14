from src.perfumeme.utils import resolve_input_to_smiles_and_cid , get_odor
import pandas as pd
import pytest 


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


def test_get_odor(monkeypatch):
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
