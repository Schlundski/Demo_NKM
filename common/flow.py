### Diese Datei enthält Funktionen, die den Fluss der Anwendung steuern, z.B. Feedback nach dem Speichern von Daten und Weiterleitung zur nächsten Seite.
## Importieren nötiger Funktionen und Module

import streamlit as st

def success_feedback(this_page, next_page):

    # Speichern-Button, Feedback Text und Weiter-Button nebeneinander
    col1, col2, col3 = st.columns([1,1,4], vertical_alignment="top")
    with col1:
        st.button("Speichern", key=f"speichern_{this_page}")
    with col2:
        if st.session_state.get(f"{this_page}_saved"):

            if st.button("Weiter", key=f"weiter_{this_page}"):
                st.session_state[f"{this_page}_saved"] = False
                st.switch_page(f"pages/{next_page}.py")
                st.stop()
    with col3:
        if st.session_state.get(f"{this_page}_saved"):
            st.success("Daten erfolgreich gespeichert!", icon="✅")
            st.toast(f"{this_page} gespeichert ✅", icon="✅")