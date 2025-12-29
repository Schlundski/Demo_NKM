import streamlit as st
from auth import check_login
from ui.components import number_standard
from config.standards import STANDARDWERTE
import time

st.session_state["ist_anlage"]["rueckspeisung"] = {}
rueckspeisung_state = st.session_state["ist_anlage"]["rueckspeisung"]








button = st.button("Speicher und weiter")

if button:
    rueckspeisung_state.update(
        {
            "faktor greifer": 0,
            "FU-Wirkungsgrad greifer": 1,
            "faktor hub": 0,
            "FU-Wirkungsgrad hub": 1,
            "faktor kran": 0,
            "FU-Wirkungsgrad kran": 1,
            "faktor katze": 0,
            "FU-Wirkungsgrad katze": 1
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Auswertung.py")