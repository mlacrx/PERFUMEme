import requests
import matplotlib.pyplot as plt
import numpy as np
import re
import math

def has_a_smell(smiles):
    try:
       
        url_cid = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
        response_cid = requests.get(url_cid)
        response_cid.raise_for_status()
        cids = response_cid.json().get("IdentifierList", {}).get("CID", [])

        if not cids:
            print("No CID found for this SMILES.")
            return False

        cid = cids[0]  

        url_desc = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/description/JSON"
        response_desc = requests.get(url_desc)
        response_desc.raise_for_status()
        data = response_desc.json()
        descriptions = data.get("InformationList", {}).get("Information", [])

        for entry in descriptions:
            description = entry.get("Description", "").lower()
            if any(keyword in description for keyword in ["odor", "odour", "fragrance", "aroma", "scent", "smell"]):
                return True
        return False

    except requests.exceptions.RequestException as e:
        print(f"PubChem request error : {e}")
        return False
    except Exception as e:
        print(f"Unexpected error : {e}")
        return False
    

def is_toxic_skin(smiles):
    try:
        url_cid = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
        response_cid = requests.get(url_cid)
        response_cid.raise_for_status()
        cids = response_cid.json().get("IdentifierList", {}).get("CID", [None])[0]

        if cids is None:
            print("No CID found for this SMILES.")
            return False

        
        url_desc = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cids}/JSON"
        response_desc = requests.get(url_desc)
        response_desc.raise_for_status()
        data = response_desc.json()
        sections = data.get("Record", {}).get("Section", [])

        def look_toxicity_skin (sections):
            for section in sections:
                heading = section.get("TOCHeading","").lower()
                if any (word in heading for word in ["toxicity","safety","hazards"]):
                    sub_sections = section.get("Section",[])
                    for ss in sub_sections:
                        sub_heading = ss.get("TOCHeading","").lower()
                        if any(word in sub_heading for word in ["skin","dermal"]):
                            return True
                        if look_toxicity_skin(ss.get("Section",[])):
                            return True
                if look_toxicity_skin(section.get("Section",[])):
                    return True
            return False
        
        return look_toxicity_skin(sections)

    except requests.exceptions.RequestException as e:
        print(f"PubChem request error : {e}")
        return False
    except Exception as e:
        print(f"Unexpected error : {e}")
        return False
    

def evaporation_trace(smiles):
    try:
        r = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON")
        r.raise_for_status()
        cid = r.json()["IdentifierList"]["CID"][0]

        r = requests.get(f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cid}/JSON")
        r.raise_for_status()
        data = r.json()
        sections = data.get("Record", {}).get("Section", [])

        vapor_pressure_value = None
        vapor_pressure_temp = None
        vapor_pressure_unit = None
        found_vapor_pressure = False
        boiling_point = None
        fallback_celsius = None
        enthalpy_vap = None

        def parse_sections(sections):
            nonlocal vapor_pressure_value, vapor_pressure_temp, vapor_pressure_unit, found_vapor_pressure
            nonlocal boiling_point, fallback_celsius, enthalpy_vap

            for section in sections:
                heading = section.get("TOCHeading", "").lower()

                if any(keyword in heading for keyword in ["enthalpy", "heat", "vaporization", "evaporation"]):
                    for info in section.get("Information", []):
                        string_list = info.get("Value", {}).get("StringWithMarkup", [])
                        for item in string_list:
                            text = item.get("String", "").lower()
                            match_enthalpy = re.search(r"([\d\.]+)\s*(kj/mol|j/mol)", text)
                            if match_enthalpy:
                                try:
                                    h_val = float(match_enthalpy.group(1))
                                    unit = match_enthalpy.group(2)
                                    enthalpy_vap = h_val * 1000 if "kj" in unit else h_val
                                except:
                                    continue

                if "vapor pressure" in heading:
                    for info in section.get("Information", []):
                        val = info.get("Value", {})
                        raw_string = val.get("StringWithMarkup", [{}])[0].get("String", "").lower()
                        match_pressure = re.search(r"([\d\.eE-]+)\s*(mmhg|kpa|pa)", raw_string)
                        match_temp = re.search(r"at\s+([\d\.]+)\s*°?\s*([cf])", raw_string)
                        if match_pressure:
                            pressure = float(match_pressure.group(1))
                            unit = match_pressure.group(2)
                            if unit == "kpa":
                                pressure *= 7.50062
                            elif unit == "pa":
                                pressure /= 133.322
                            temp = None
                            if match_temp:
                                t_val = float(match_temp.group(1))
                                t_unit = match_temp.group(2)
                                temp = t_val if t_unit == "c" else (t_val - 32) * 5 / 9
                            vapor_pressure_value = pressure
                            vapor_pressure_temp = temp if temp is not None else 25
                            vapor_pressure_unit = "mmHg"
                            found_vapor_pressure = True

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

                if "Section" in section:
                    parse_sections(section["Section"])

        parse_sections(sections)


        
        time = np.linspace(0, 25, 300)
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

            plt.figure(figsize=(10, 5))
            plt.plot(time, evap_rate, label="Model with Clausius-Clapeyron", color="green")
            plt.xlabel("Time (hours)")
            plt.ylabel("Relative concentration")
            plt.title("Evaporation curve based on vapor pressure")
            plt.grid(True)
            plt.legend()
            plt.show()

        elif boiling_point:
            evap_rate = np.exp(-0.2 * time / (boiling_point / 10))
            evap_rate /= evap_rate[0]
            plt.figure(figsize=(10, 5))
            plt.plot(time, evap_rate, label=f"Fallback model - Tb = {boiling_point:.1f} °C", color="blue")
            plt.title("Estimated evaporation curve")
            plt.xlabel("Time (hours)")
            plt.ylabel("Relative concentration")
            plt.grid(True)
            plt.legend()
            plt.show()


    except Exception as e:
        print(f"❌ Error : {e}")
    return vapor_pressure_value, boiling_point,vapor_pressure_temp, enthalpy_vap






