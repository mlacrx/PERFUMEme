import numpy as np
from .main_fonctions import has_a_smell, is_toxic_skin, evaporation_trace

def usable_in_perfume(smiles: str):
    
    if not has_a_smell(smiles):
        return "❌ The molecule has no detectable smell.", None
    
    if not is_toxic_skin(smiles):
        return "❌ The molecule is not safe for skin contact if present in large quantity.", None

    vapor_pressure_value, boiling_point,vapor_pressure_temp = evaporation_trace(smiles)

    if vapor_pressure_value is None and boiling_point is None:
        return "⚠️ The molecule might be suitable, but lacks sufficient volatility data to classify."

    note_type = "undetermined"
    if vapor_pressure_value is not None:
        pvap_37 = vapor_pressure_value * np.exp(-0.1 * (37 - vapor_pressure_temp))
        if pvap_37 > 10:
            note_type = "top note"
        elif pvap_37 > 0.1:
            note_type = "heart note"
        else:
            note_type = "base note"

        if pvap_37 > 100:
            return f"❌ The molecule is too volatile (Pvap at 37°C: {pvap_37:.2f} mmHg) for perfume use."
        elif pvap_37 < 0.01:
            return f"❌ The molecule is not volatile enough (Pvap at 37°C: {pvap_37:.4f} mmHg) to be noticeable in a perfume."
    else:
        if boiling_point < 150:
            note_type = "top note"
        elif boiling_point <= 250:
            note_type = "heart note"
        else:
            note_type = "base note"

    return f"✅ The molecule is suitable for perfume use and behaves as a {note_type}."

