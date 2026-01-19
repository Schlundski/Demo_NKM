import streamlit as st
from auth import check_login
from ui.components import number_standard
from config.standards import STANDARDWERTE
import time
from ui.theme import set_background_auto_theme

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)

st.set_page_config(layout = "centered")

weg_trichter = {}

db_r = STANDARDWERTE["Referenzwege"]

st.title("Wege")

# Container im Session State
ist_state = st.session_state["ist_anlage"]
wege_state = ist_state.setdefault("wege", {})

weg_hebensenken_m = number_standard(
    "Referenzweg Heben senken [m]",
    db_r["Heben/Senken"],
    0,
    1,
    200,
    "wg_hs_m",
    nachkommastellen=0
)
weg_katzfahrt_m = number_standard(
    "Referenzweg Katzfahrt [m]",
    db_r["Katzfahrt"],
    0,
    1,
    200,
    "wg_ktzfhrt_m",
    nachkommastellen=0
)
weg_kranfahrt_m = number_standard(
    "Referenzweg Kranfahrt Einlagern [m]",
    db_r["Kranfahrt Einlagern"],
    0,
    1,
    200,
    "wg_krnfhrt_m",
    nachkommastellen=0
)
weg_oeffnenschliessn_m = number_standard(
    "Referenzweg Greifer Öffnen/Schließen",
    db_r["Öffnen/Schließen"],
    0,
    1,
    200,
    "wg_ofnschl_m",
    nachkommastellen=0
)

for zahl in range(int(ist_state["anlage"]["anzahl_trichter"])):
    key = f"Trichterweg {zahl + 1}"
    weg_trichter[zahl] = number_standard(
        f"Referenzweg Trichter {zahl + 1}",
        db_r[key],
        0,
        1,
        200,
        f"wg_tr_{zahl + 1}",
        nachkommastellen=0,
    )

button = st.button("Speicher und weiter")

if button:
    wege_state.update(
        {
            "weg_hebensenken_m": weg_hebensenken_m,
            "weg_katzfahrt_m": weg_katzfahrt_m,
            "weg_kranfahrt_einlagern_m": weg_kranfahrt_m,
            "weg_oeffnen_schliessen_m": weg_oeffnenschliessn_m,
            "weg_trichter_m": weg_trichter,
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Rückspeisung.py")
