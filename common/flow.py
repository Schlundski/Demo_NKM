### Diese Datei enthält Funktionen, die den Fluss der Anwendung steuern, z.B. Feedback nach dem Speichern von Daten und Weiterleitung zur nächsten Seite.
## Importieren nötiger Funktionen und Module

import streamlit as st

def success_feedback(this_page, next_page):

    if st.session_state.get(f"{this_page}_saved"):

        if st.button("Weiter", key=f"weiter_{this_page}"):
            st.session_state[f"{this_page}_saved"] = False
            st.switch_page(f"pages/{next_page}.py")