import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from perfumeme.main_functions import has_a_smell, is_toxic_skin, evaporation_trace


def usable_in_perfume(smiles_or_name: str):
    """
    Evaluates whether a molecule is suitable for use in perfume formulations.

    This function checks three main criteria: whether the molecule has an odor, whether it is safe for dermal 
    exposure, and whether its volatility is appropriate for perfumery. It uses vapor pressure data (or boiling 
    point as a fallback) to determine the note classification (top, heart, or base). A graph of the evaporation 
    curve is generated and annotated with the note type.

    Args:
        smiles_or_name (str): The SMILES string or compound name.

    Returns:
        tuple:
            - msg (str): A summary string indicating perfume suitability, note classification, and safety.
            - annotated_path (str or None): File path to the saved annotated evaporation curve image, or None 
              if no plot was generated.
    
    Notes:
        - Uses `has_a_smell`, `is_toxic_skin`, and `evaporation_trace` from the package.
        - Evaporation note classification is based on vapor pressure extrapolated to 37°C (body temperature).
        - If vapor pressure data is missing, boiling point is used to estimate volatility.
        - The resulting plot is saved and optionally annotated with note classification.
    """
    smell_ok = has_a_smell(smiles_or_name)
    toxicity_ok = not is_toxic_skin(smiles_or_name)

    pvap, boiling_point, pvap_temp, enthalpy, plot_path = evaporation_trace(smiles_or_name)

    if pvap is None and boiling_point is None:
        note_type = "undetermined"
        volatility_comment = "⚠️ Insufficient volatility data to classify the note."
        annotated_path = plot_path
    else:

        pvap_37 = pvap * np.exp(-0.1 * (37 - pvap_temp)) if pvap and pvap_temp else None
        
        if pvap_37:
            if pvap_37 > 100:
                note_type = "too volatile"
                volatility_comment = f"❌ Too volatile for perfume use (Pvap at 37°C: {pvap_37:.2f} mmHg)."
            elif pvap_37 < 0.01:
                note_type = "not volatile enough"
                volatility_comment = f"❌ Not volatile enough (Pvap at 37°C: {pvap_37:.4f} mmHg)."
            elif pvap_37 > 10:
                note_type = "top note"
                volatility_comment = f"✅ Acts as a **top note** (Pvap at 37°C: {pvap_37:.2f} mmHg)."
            elif pvap_37 > 0.1:
                note_type = "heart note"
                volatility_comment = f"✅ Acts as a **heart note** (Pvap at 37°C: {pvap_37:.2f} mmHg)."
            else:
                note_type = "base note"
                volatility_comment = f"✅ Acts as a **base note** (Pvap at 37°C: {pvap_37:.2f} mmHg)."
        else:
            if boiling_point < 150:
                note_type = "top note"
            elif boiling_point <= 250:
                note_type = "heart note"
            else:
                note_type = "base note"
            volatility_comment = f"Estimated from boiling point: **{note_type}**."

        if plot_path:
            img = mpimg.imread(plot_path)
            fig, ax = plt.subplots()
            ax.imshow(img)
            ax.axis('off')
            if has_a_smell(smiles_or_name):
                note_display = f"Note: {note_type.upper()}"
            else:
                note_display="No odor"
            ax.text(0.05,0.9, note_display, transform=ax.transAxes,
                    fontsize = 8, fontweight='bold', color = 'darkblue',
                    bbox = dict(facecolor = 'white', alpha=0.6, edgecolor = 'none'))
            annotated_path = plot_path.replace(".png","_annotated.png")
            plt.savefig(annotated_path, bbox_inches = 'tight', dpi=700)
            plt.show()
            plt.close()
        else:
            annotated_path = None

    msg = "Perfume suitability summary:\n"
    msg += "👃 Smell detected.\n" if smell_ok else "🚫 No smell detected.\n"
    msg += "🧴 Skin-safe.\n" if toxicity_ok else "⚠️ Not confirmed safe for skin contact.\n"
    msg += f"{volatility_comment}"

    return msg, annotated_path