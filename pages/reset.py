### Seite zum Zurücksetzen aller Eingaben und Session State, um von vorne zu beginnen. 
### Wird über den "Reset"-Button in der Seitenleiste aufgerufen.
import streamlit as st
from streamlit_lottie import st_lottie
import json
import time

# Alle Session State Einträge löschen, um mit einem "leeren" Zustand zu starten
st.session_state.clear()

# Animation anzeigen, um den Reset-Vorgang zu visualisieren
with open("assets/kran_entsorgung.json", "r") as f:
    lottie_animation = json.load(f)

st_lottie(
    lottie_animation,
    speed=1,
    reverse=False,
    loop=True,
    quality="high",
    height=700,
    width=700)

time.sleep(6)  # Kurze Pause, damit die Animation sichtbar ist

# Danach zurück zur Startseite wechseln
st.switch_page("pages/startseite.py")