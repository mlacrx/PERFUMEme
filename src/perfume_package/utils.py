import requests
import matplotlib.pyplot as plt
import numpy as np


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
    
def evaporation_trace (smiles):
    try:
        url_cid = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/smiles/{smiles}/cids/JSON"
        response_cid = requests.get(url_cid)
        response_cid.raise_for_status()
        cids = response_cid.json().get("IdentifierList", {}).get("CID", [None])[0]
        if cids is None:
            print("No CID found for this SMILES.")
            return None, None
        
        url_prop = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug_view/data/compound/{cids}/JSON"
        response_prop = requests.get(url_prop)
        response_prop.raise_for_status()
        data = response_prop.json()
        sections = data.get("Record",{}).get("Section",[])
        pvap = None
        boiling_point = None

        def parse_sections (sections):
            nonlocal pvap, boiling_point
            fallback_celsius = None
            for section in sections:
                heading = section.get("TOCHeading", "").lower()
                if "vapor pressure" in heading:
                    for info in section.get("Information", []):
                        val = info.get("Value", {}).get("StringWithMarkup",[{}])[0].get("String","")
                        if "25" in val and "mmHg" in val:
                            try:
                                pvap=float(val.split()[0])
                            except:
                                continue

                if "boiling point" in heading:
                    for info in section.get("Information", []):
                        value = info.get("Value", {}).get("StringWithMarkup",[{}])[0].get("String","")
                        if "°F" in value:
                            try:
                                 f =float(value.split()[0].replace("°F","").replace("F","").strip())
                                 boiling_point = (f-32)*5/9
                                 return           
                            except:
                                 continue
                        elif "°C" in value or "C" in value:
                            try:
                                c_str = value.split()[0].replace ("°C","").replace("C","").strip()
                                fallback_celsius = float (c_str)
                            except:
                                continue
                parse_sections(section.get("Section",[]))
            
            if boiling_point is None and fallback_celsius is not None:
                boiling_point = fallback_celsius
        
        parse_sections(sections)
        
        if pvap is not None:
            time = np.linspace(0,12,300)
            k=0.1
            evap_rate = np.exp(-k*time/pvap)
            evap_rate /=evap_rate[0]
            plt.figure(figsize=(10,5))
            plt.plot (time, evap_rate, label="Evaporation rate (standardised)", color = 'green')
            plt.title (f"Evaporation model - Pvap:{pvap:.2f}mmHg({volatility})")
            plt.xlabel("Time (hours)")
            plt.ylabel ("Relative concentration")
            plt.grid(True)
            plt.legend ()
            plt.tight_layout()
            plt.show()
        elif boiling_point is not None:
            time = np.linspace(0,24,300)
            k = 0.2
            evap_rate = np.exp(-k*time/(boiling_point/10))
            evap_rate /=evap_rate[0]
            plt.figure(figsize=(10,5))
            plt.plot (time, evap_rate, label=f"Estimated evaporation (Teb = {boiling_point:.1f}°C)", color = 'blue')
            plt.title ("Estimated evaporation curve (boiling point)")
            plt.xlabel("Time (hours)")
            plt.ylabel ("Relative concentration")
            plt.grid(True)
            plt.legend ()
            plt.tight_layout()
            plt.show()
        else:
             print ("Insufficient data to plot the evaporation curve.")
            
    
    except Exception as e:
        print(f"Error : {e}")

    


