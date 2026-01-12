import streamlit as st
from auth import check_login
from ui.components import rueckspeisung_standard
from config.standards import STANDARDWERTE
import time
from ui.theme import set_background_auto_theme

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)


check_login()

st.session_state["ist_anlage"]["rueckspeisung"] = {}
rueckspeisung_state = st.session_state["ist_anlage"]["rueckspeisung"]

st.title("Rückspeisungen")

rueckspeisung_greifer = rueckspeisung_standard(
    "Rückspeisung Greifer", 
    0.98, 0, 0.01, 1, 
    "rckspng_grfr", 
    "Hat die Anlage eine Rückspeisung bei Greifer Öffnen/Schließen?", 
    2
)

rueckspeisung_hub = rueckspeisung_standard(
    "Rückspeisung Hubfahrt",
    0.98,
    0,
    0.01,
    1,
    "rckspng_hb",
    "Hat die Anlage eine Rückspeisung bei der Hubfahrt?",
    2
)

rueckspeisung_kran = rueckspeisung_standard(
    "Rückspeisung Kranfahrt",
    0.98,
    0,
    0.01,
    1,
    "rckspng_krn",
    "Hat die Anlage eine Rückspeisung bei der Kranfahrt?",
    2
)

rueckspeisung_katz = rueckspeisung_standard(
    "Rückspeisung Katzfahrt",
    0.98,
    0,
    0.01,
    1,
    "rckspng_ktzfhrt",
    "Hat die Anlage eine Rückspeisung bei der Katzfahrt?",
    2
)

button = st.button("Speicher und weiter")

if button:
    rueckspeisung_state.update(
        {
            "faktor greifer": rueckspeisung_greifer[1],
            "FU-Wirkungsgrad greifer": rueckspeisung_greifer[0],
            "faktor hub": rueckspeisung_hub[1],
            "FU-Wirkungsgrad hub": rueckspeisung_hub[0],
            "faktor kran": rueckspeisung_kran[1],
            "FU-Wirkungsgrad kran": rueckspeisung_kran[0],
            "faktor katze": rueckspeisung_katz[1],
            "FU-Wirkungsgrad katze": rueckspeisung_katz[0]
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Auswertung.py")