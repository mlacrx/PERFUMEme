import requests

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
        print(f"Erreur de requête PubChem : {e}")
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        return False
