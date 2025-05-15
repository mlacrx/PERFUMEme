import matplotlib.pyplot as plt
import numpy as np
import re
import math
from perfumeme.utils import get_pubchem_description, get_pubchem_record_sections, resolve_input_to_smiles_and_cid


def has_a_smell(compound_name_or_smiles):
    """
    Checks if a given compound has a detectable smell based on its description from PubChem.

    The function takes either a compound name or SMILES notation as input. It retrieves the corresponding 
    SMILES string (if a compound name is provided), fetches the PubChem CID (Compound ID), and then checks 
    the compound's description for keywords related to odor or fragrance.

    Args:
        compound_name_or_smiles (str): The compound name or SMILES string for the chemical compound.

    Returns:
        bool: True if the compound has a detectable smell (it contains keywords like "odor", "fragrance", 
              "scent", etc. in its description), False otherwise.

    Raises:
        Exception: If the compound name or SMILES is invalid or if there is an issue retrieving data from PubChem.
    """
    smiles, cid = resolve_input_to_smiles_and_cid(compound_name_or_smiles)
    descriptions = get_pubchem_description(cid)

    for entry in descriptions:
        description = entry.get("Description", "").lower()
        if any(keyword in description for keyword in ["odor", "odour", "fragrance", "aroma", "scent", "smell"]):
            return True
    return False


def is_toxic_skin(compound_name_or_smiles):
    """
    Determines whether a given compound has skin or dermal toxicity information in its PubChem safety data.

    The function takes either a compound name or SMILES string. It resolves the compound to a PubChem CID,
    retrieves its detailed record sections, and searches recursively for information related to skin or dermal 
    toxicity in the "Toxicity", "Safety", or "Hazards" sections.

    Args:
        compound_name_or_smiles (str): The name or SMILES representation of the compound.

    Returns:
        bool: True if the compound has documented skin or dermal toxicity information in PubChem, False otherwise.

    Raises:
        Exception: If the compound name or SMILES is invalid or if data cannot be retrieved from PubChem.
    """

    smiles, cid = resolve_input_to_smiles_and_cid(compound_name_or_smiles)
    sections = get_pubchem_record_sections(cid)
    
    def look_toxicity_skin (sections):
        for section in sections:
            heading = section.get("TOCHeading","").lower()
            if any (word in heading for word in ["toxicity","safety","hazards"]):
                for sub in section.get("Section",[]):
                    sub_heading = sub.get("TOCHeading","").lower()
                    if any (k in sub_heading for k in ["skin", "dermal"]):
                        return True
                    if look_toxicity_skin(sub.get("Section",[])):
                        return True
            if look_toxicity_skin(section.get("Section",[])):
                return True
        return False
    
    return look_toxicity_skin(sections)
  

def evaporation_trace(compound_name_or_smiles: str, save_path: str = "evaporation_curve.png"):
    """
    Computes and plots the evaporation profile of a compound using thermodynamic data from PubChem.

    The function attempts to retrieve vapor pressure, temperature of measurement, boiling point, and 
    enthalpy of vaporization from the compound's PubChem record. If sufficient data is available,
    it simulates the evaporation curve using the Clausius-Clapeyron equation or a fallback exponential model.
    The resulting curve is saved as an image.

    Args:
        compound_name_or_smiles (str): The compound's common name or SMILES string.
        save_path (str, optional): Path to save the resulting plot image. Defaults to "evaporation_curve.png".

    Returns:
        tuple:
            - vapor_pressure_value (float or None): Vapor pressure in mmHg if found, else None.
            - boiling_point (float or None): Boiling point in °C if found, else None.
            - vapor_pressure_temp (float or None): Temperature at which vapor pressure was measured, in °C.
            - enthalpy_vap (float or None): Enthalpy of vaporization in J/mol.
            - save_path (str): The path where the plot was saved.


    Notes:
        - Uses a recursive parser to extract data from PubChem sections.
        - Falls back to a simplified exponential model if insufficient data is available for the Clausius-Clapeyron model.
        - Requires matplotlib and numpy to be installed.
    """

    smiles, cid = resolve_input_to_smiles_and_cid(compound_name_or_smiles)
    sections = get_pubchem_record_sections(cid)

    vapor_pressure_value = None
    vapor_pressure_temp = None
    boiling_point = None
    fallback_celsius = None
    enthalpy_vap = None

    def parse_sections(sections):
        nonlocal vapor_pressure_value, vapor_pressure_temp, boiling_point, fallback_celsius, enthalpy_vap

        for section in sections:
            heading = section.get("TOCHeading", "").lower()

            if "vapor pressure" in heading:
                for info in section.get("Information", []):
                    val = info.get("Value", {})
                    strings = [s.get("String", "") for s in val.get("StringWithMarkup", [])]

                    for raw in strings:
                        raw_lower = raw.lower()

                        matches = re.findall(
                            r"([\d\.,eE+-]+)\s*(?:\[)?\s*(mmhg|kpa|pa)\s*(?:\])?(?:\s*(?:at)?\s*([\d\.,]+)?\s*°?\s*([cf]))?",
                            raw_lower
                        )

                        for match in matches:
                            if vapor_pressure_value is not None:
                                break 

                            val_str, unit, temp_str, temp_unit = match

                            try:
                                pressure = float(val_str.replace(",", ""))
                                if pressure >= 100:
                                    continue 
                                if unit == "kpa":
                                    pressure *= 7.50062
                                elif unit == "pa":
                                    pressure /= 133.322
                                vapor_pressure_value = pressure
                            except:
                                continue

                            if temp_str and temp_unit:
                                try:
                                    temp = float(temp_str.replace(",", ""))
                                    vapor_pressure_temp = temp if temp_unit == "c" else int ((temp - 32) * 5 / 9)
                                except:
                                    vapor_pressure_temp = 25
                            else:
                                vapor_pressure_temp = 25

                        if vapor_pressure_value is not None:
                            break

            if "boiling point" in heading:
                for info in section.get("Information", []):
                    val = info.get("Value", {}).get("StringWithMarkup", [{}])[0].get("String", "").lower()
                    if "°f" in val:
                        try:
                            f = float(val.split()[0].replace("°f", "").replace("f", "").strip())
                            boiling_point = (f - 32) * 5 / 9
                        except:
                            continue
                    elif "°c" in val or "c" in val:
                        try:
                            c = float(val.split()[0].replace("°c", "").replace("c", "").strip())
                            fallback_celsius = c
                        except:
                            continue

            if any(k in heading for k in ["enthalpy", "heat", "vaporization", "evaporation"]):
                for info in section.get("Information", []):
                    for item in info.get("Value", {}).get("StringWithMarkup", []):
                        text = item.get("String", "").lower()
                        match_h = re.search(r"([\d\.]+)\s*(kj/mol|j/mol|kcal/mole)", text)
                        if match_h:
                            val = float(match_h.group(1))
                            unit = match_h.group(2)

                            if "kj" in unit:
                                enthalpy_vap = val * 1000 
                            elif "kcal" in unit:
                                enthalpy_vap = val * 4184 
                            else:
                                enthalpy_vap = val 

            if "Section" in section:
                parse_sections(section["Section"])

    parse_sections(sections)

    if boiling_point is None and fallback_celsius:
        boiling_point = fallback_celsius

    time = np.linspace(0, 25, 300)
    plt.figure(figsize=(10, 5))

    if enthalpy_vap and vapor_pressure_value and vapor_pressure_temp:
        R = 8.314
        T = vapor_pressure_temp + 273.15
        ln_P = math.log(vapor_pressure_value)
        C = ln_P + (enthalpy_vap / (R * T))

        def P(T_kelvin):
            return np.exp(C - enthalpy_vap / (R * T_kelvin))

        temp_curve = np.linspace(298, 318, len(time))
        pressures = P(temp_curve)
        evap_rate = np.exp(-0.05 * time / pressures)
        evap_rate /= evap_rate[0]

        plt.plot(time, evap_rate, label="Clausius-Clapeyron Model", color="green")
    elif boiling_point:
        evap_rate = np.exp(-0.2 * time / (boiling_point / 10))
        evap_rate /= evap_rate[0]
        plt.plot(time, evap_rate, label=f"Fallback Model - Tb = {boiling_point:.1f}°C", color="blue")
    else:
        print("⚠️ Not enough data to calculate evaporation curve.")
        return None, None, None, None, None

    plt.xlabel("Time (hours)")
    plt.ylabel("Relative Concentration")
    plt.title(f"Evaporation Curve of {compound_name_or_smiles}")
    plt.grid(False)
    plt.legend()
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

    return vapor_pressure_value, boiling_point, vapor_pressure_temp, enthalpy_vap, save_path
