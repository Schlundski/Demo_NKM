### Seite zum Zurücksetzen aller Eingaben und Session State, um von vorne zu beginnen. 
### Wird über den "Reset"-Button in der Seitenleiste aufgerufen.
import streamlit as st

# Alle Session State Einträge löschen, um mit einem "leeren" Zustand zu starten
st.session_state.clear()
# Danach zurück zur Startseite wechseln
st.switch_page("pages/startseite.py")