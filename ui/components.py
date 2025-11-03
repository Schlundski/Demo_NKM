import streamlit as st

def number_standard(
        titel="not defined",
        standard=0.0,
        min=0.0,
        steps=0.1,
        max=15,
        key="not_defined"):

    "Unser UI Standard für numerische Eingaben, returned nur den Eingabe- bzw. Standardwert"
    
    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel)
    with col2:
        use_std = st.checkbox("Standard", value=True, key=f"use_default_{key}")

    ausgabe = st.number_input(
        titel,
        value=float(standard) if use_std else float(min),
        min_value=float(min),
        max_value=float(max),
        step=float(steps),
        disabled=True if use_std else False,
        key=f"value_{key}",
        label_visibility="collapsed"
    )

    return ausgabe
