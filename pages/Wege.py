import streamlit as st
from auth import check_login
from ui.components import number_standard
from config.standards import STANDARDWERTE
import time

testanzahltrichter = 3
weg_trichter = {}

db_r = STANDARDWERTE["Referenzwege"]

weg_hebensenken_m = number_standard("Referenzweg Heben senken [m]", db_r["Heben/Senken in m"], 0, 1, 200, "wg_hs_m")
weg_katzfahrt_m = number_standard("Referenzweg Katzfahrt [m]", db_r["Katzfahrt"], 0, 1, 200, "wg_ktzfhrt_m")
weg_kranfahrt_m = number_standard("Referenzweg Kranfahrt Einlagern [m]", db_r["Kranfahrt Einlagern"], 0, 1, 200, "wg_krnfhrt_m")
weg_oeffnenschliessn_m = number_standard("Referenzweg Greifer Öffnen/Schließen", db_r["Öffnen/Schließen"], 0, 1, 200, "wg_ofnschl_m")
for zahl in range(testanzahltrichter):
    key = f"Trichterweg {zahl+1}"
    weg_trichter[zahl] = number_standard(f"Referenzweg Trichter {zahl+1}", db_r[f"Trichterweg {zahl+1}"], 0, 1, 200, f"wg_tr_{zahl+1}")


button = st.button("Speicher und weiter")

if button:
    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Geschw.py")