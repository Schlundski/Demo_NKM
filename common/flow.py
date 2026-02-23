### Diese Datei enthält Funktionen, die den Fluss der Anwendung steuern, z.B. Feedback nach dem Speichern von Daten und Weiterleitung zur nächsten Seite.
## Importieren nötiger Funktionen und Module
import streamlit as st

## Funktion für Feedback nach dem Speichern von Daten und Weiterleitung zur nächsten Seite
def success_feedback(this_page, next_page):
    if st.session_state.get(f"{this_page}_saved"):
        st.success(f"Eingaben der Seite \"{this_page}\" erfolgreich gespeichert ✅")

        if st.button("Weiter", f"weiter_{this_page}"):
            st.session_state[f"{this_page}_saved"] = False  # Flag setzen, dass diese Seite gespeichert wurde
            st.switch_page(f"pages/{next_page}.py")