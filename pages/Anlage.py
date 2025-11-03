import streamlit as st
#from auth import check_login
from components import number_with_standard_row

st.header("Eingabe der Anlagendaten")

anzahl_krane = st.number_input("Anzahl der Krane", 1, 5, key="anzahl kraene")
anzahl_trichter = st.number_input("Anzahl der Trichter", 1, 10, key= "anzahl trichter")

verbrennung_je_trichter_tph = number_with_standard_row("Verbrennung je Trichter [t/h]", "vjt", 15, min_value = 1, step = 1)

