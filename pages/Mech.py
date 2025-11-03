import streamlit as st
from auth import check_login
from ui.components import number_standard
from config.standards import STANDARDWERTE
import time

st.header("Mechanische Anlagen-Werte")

button = st.button("Speicher und weiter")

if button:
    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Wege.py")