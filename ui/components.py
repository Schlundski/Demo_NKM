import streamlit as st

# Vorlage:
    ## Zeile 1: Titel (links) + Standard-Checkbox (rechts) – teilen sich die Breite
    #row1_col1, row1_col2 = st.columns([5, 2])
    #with row1_col1:
    #    st.markdown("**Verbrennung je Trichter [t/h]**")
    # row1_col2:
    #    use_std_vjt = st.checkbox("Standard", value=True, key="vjt_use_default")

    ## Zeile 2: Eingabebox über die ganze Breite
    # = st.number_input(
    #    "Verbrennung je Trichter [t/h]",
    #    value=15.0,
    #    min_value=0.0,
    #    step=0.1,
    #    format="%.1f",
    #    disabled=use_std_vjt,
    #    key="vjt_value",
    #    label_visibility="collapsed"  # Label ausblenden, da oben schon Titel steht
    

    #verbrennung_je_trichter_tph = 15.0 if use_std_vjt else float(vjt_val)

def number_with_standard_row(
        string titel,
        
)

