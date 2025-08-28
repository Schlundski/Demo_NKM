import streamlit as st
import pandas as pd
import time

st.title("🔧 Faktoren eingeben")
st.write("\n\n\n\n\n\n")

# (Komma/Punkt) in float wandeln
def to_float(x, default=None):
    try:
        return float(str(x).replace(",", "."))
    except Exception:
        return default

## Faktorenuswahl
auswahl_standard = st.selectbox(
    "Daten manuell eingeben oder Bestandsanlagenvorlagen verwenden?",
    ["Manuell", "AVG Köln"],
    key="std_preset"
)
if auswahl_standard == "AVG Köln":
    pass

# Allgemeines & Müllmengen
st.write("# :blue[Allgemeines & Müllmengen]")
st.write(":grey[Allgemeines]")
auswahl_kranzahl            = st.number_input("Anzahl der Kräne", key="anzahl_kraene")
auswahl_trichterzahl        = st.number_input("Anzahl der Trichter", min_value=1, max_value=10, key="anzahl_trichter")
auswahl_trichterverbrennung = st.number_input("Verbrennung je Trichter in Mg/h", key="trichter_verbrennung_Mg_h")

auswahl_greifer_select = st.selectbox(
    "Greifer auswählen oder Daten  manuell eingeben?",
    [
        "Manuell eingeben",
        "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1",
        "Vierseil_Mehrschalen Müllgreifer Mrs Greifer 1-26-6315-6316"
    ],
    key="greifer_auswahl"
)
if auswahl_greifer_select == "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
    auswahl_greifer_gewicht = 3.050
    auswahl_greifer_motor   = 18.8
    auswahl_greifer_inhalt  = 2.75
elif auswahl_greifer_select == "Vierseil_Mehrschalen Müllgreifer Mrs Greifer 1-26-6315-6316":
    auswahl_greifer_gewicht = 3.800
    auswahl_greifer_motor   = st.number_input("Hubmotorleistung Greifer Öffnen/Schließen in kW", key="greifer_motor_kW")
    auswahl_greifer_inhalt  = 4
elif auswahl_greifer_select == "Manuell eingeben":
    auswahl_greifer_gewicht = st.number_input("Leergewicht Greifer in Mg", key="greifer_leergewicht_Mg")
    auswahl_greifer_motor   = st.number_input("Motorleistung Greifer für Öffnen/Schließen in kW (Hubmotor oder Hydraulikmotor)", key="greifer_motor_kW")
    auswahl_greifer_inhalt  = st.number_input("Greifervolumen in m³", key="greifer_volumen_m3")

st.write(":grey[Müllmengen]")
auswahl_müll = st.selectbox(
    " Bei Müllmengen mit Standard rechnen oder eigene Werte eingeben?",
    ["Standard", "Werte eingeben"],
    key="muell_modus"
)
if auswahl_müll == "Werte eingeben":
    auswahl_müll_gesamtmenge_jahr = st.number_input("Müllmenge in Mg pro Jahr", key="muell_gesamt_Mg_a")
    auswahl_müll_anliefermenge_h  = st.number_input("Anliefermenge in Mg pro Stunde", key="muell_anliefer_Mg_h")
    auswahl_müll_anlieferdauer    = st.number_input("Anlieferdauer in Stunden", key="muell_anlieferdauer_h")
    auswahl_müll_dichte_einlagern = st.number_input("Abfalldichte im Greifer bei Einlagerung in Mg/m³", key="muell_dichte_einlagerung_Mg_m3")
    auswahl_müll_dichte_trichter  = st.number_input("Abfalldichte im Greifer bei Trichterbeschickung in Mg/m³", key="muell_dichte_trichter_Mg_m3")
if auswahl_müll == "Standard":
    pass  # Standardtabelle noch nachzutragen

# Referenzwege
st.write("\n\n")
st.write("# :blue[Angaben zu Referenzwegen und Bewegungen]")
st.write(":grey[Referenzwege]")
auswahl_referenzweg_hebensenken     = st.number_input("Referenzweg Heben/Senken in m", key="weg_heben_m")
auswahl_referenzweg_katzfahrt       = st.number_input("Referenzweg Katzfahrt in m", key="weg_katz_m")
auswahl_referenzweg_kranfahrt       = st.number_input("Referenzweg Kranfahrt in m", key="weg_kran_m")
auswahl_referenzweg_oeffnenschliessen = st.number_input("Referenzweg Greifer Öffnen/Schließen in m", key="weg_oeffnen_m")

if auswahl_trichterzahl == 1:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
elif auswahl_trichterzahl == 2:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
elif auswahl_trichterzahl == 3:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
    auswahl_referenzweg_trichter3 = st.number_input("Referenzweg Kranfahrt Trichter 3 in m", key="weg_trichter_3_m")
elif auswahl_trichterzahl == 4:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
    auswahl_referenzweg_trichter3 = st.number_input("Referenzweg Kranfahrt Trichter 3 in m", key="weg_trichter_3_m")
    auswahl_referenzweg_trichter4 = st.number_input("Referenzweg Kranfahrt Trichter 4 in m", key="weg_trichter_4_m")
elif auswahl_trichterzahl == 5:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
    auswahl_referenzweg_trichter3 = st.number_input("Referenzweg Kranfahrt Trichter 3 in m", key="weg_trichter_3_m")
    auswahl_referenzweg_trichter4 = st.number_input("Referenzweg Kranfahrt Trichter 4 in m", key="weg_trichter_4_m")
    auswahl_referenzweg_trichter5 = st.number_input("Referenzweg Kranfahrt Trichter 5 in m", key="weg_trichter_5_m")
elif auswahl_trichterzahl == 6:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
    auswahl_referenzweg_trichter3 = st.number_input("Referenzweg Kranfahrt Trichter 3 in m", key="weg_trichter_3_m")
    auswahl_referenzweg_trichter4 = st.number_input("Referenzweg Kranfahrt Trichter 4 in m", key="weg_trichter_4_m")
    auswahl_referenzweg_trichter5 = st.number_input("Referenzweg Kranfahrt Trichter 5 in m", key="weg_trichter_5_m")
    auswahl_referenzweg_trichter6 = st.number_input("Referenzweg Kranfahrt Trichter 6 in m", key="weg_trichter_6_m")
elif auswahl_trichterzahl == 7:
    auswahl_referenzweg_trichter1 = st.number_input("Referenzweg Kranfahrt Trichter 1 in m", key="weg_trichter_1_m")
    auswahl_referenzweg_trichter2 = st.number_input("Referenzweg Kranfahrt Trichter 2 in m", key="weg_trichter_2_m")
    auswahl_referenzweg_trichter3 = st.number_input("Referenzweg Kranfahrt Trichter 3 in m", key="weg_trichter_3_m")
    auswahl_referenzweg_trichter4 = st.number_input("Referenzweg Kranfahrt Trichter 4 in m", key="weg_trichter_4_m")
    auswahl_referenzweg_trichter5 = st.number_input("Referenzweg Kranfahrt Trichter 5 in m", key="weg_trichter_5_m")
    auswahl_referenzweg_trichter6 = st.number_input("Referenzweg Kranfahrt Trichter 6 in m", key="weg_trichter_6_m")
    auswahl_referenzweg_trichter7 = st.number_input("Referenzweg Kranfahrt Trichter 7 in m", key="weg_trichter_7_m")

st.write(":grey[Bewegungen]")
auswahl_bewegung_hebensenken     = st.number_input("Geschwindigkeit Heben/Senken in m/min", key="v_heben_m_min")
auswahl_bewegung_katzfahrt       = st.number_input("Geschwindigkeit Katzfahrt in m/min", key="v_katz_m_min")
auswahl_bewegung_kranfahrt       = st.number_input("Geschwindigkeit Kranfahrt in m/min", key="v_kran_m_min")
auswahl_bewegung_oeffnenschliessen = st.number_input("Geschwindigkeit Greifer Öffnen/Schließen", key="v_oeffnen_einh")

st.write(":grey[Beschleunigungen]")
auswahl_beschleunigung_hebensenken     = st.number_input("Beschleuigung Heben/Senken in m/s²", key="a_heben_m_s2")
auswahl_beschleunigung_katzfahrt       = st.number_input("Beschleunigung Katzfahrt in m/s²", key="a_katz_m_s2")
auswahl_beschleunigung_kranfahrt       = st.number_input("Beschleunigung Kranfahrt in m/s²", key="a_kran_m_s2")
auswahl_beschleunigung_oeffnenschliessen = st.number_input("Beschleunigung Greifer Öffnen/Schließen in m/s²", key="a_oeffnen_m_s2")

##-----------------------------------------------------------------
# Speichern & Wechseln
if st.button("Auswahl speichern & zur Auswertung"):
    # Greiferwerte aus Auswahl ableiten (Konstanten oder Eingaben)
    gaus = st.session_state.get("greifer_auswahl")
    if gaus == "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        g_gewicht_Mg = 3.05
        g_motor_kW   = 18.8
        g_vol_m3     = 2.75
    elif gaus == "Vierseil_Mehrschalen Müllgreifer Mrs Greifer 1-26-6315-6316":
        g_gewicht_Mg = 3.8
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))
        g_vol_m3     = 4.0
    else:  # Manuell eingeben
        g_gewicht_Mg = to_float(st.session_state.get("greifer_leergewicht_Mg"))
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))
        g_vol_m3     = to_float(st.session_state.get("greifer_volumen_m3"))

    # Trichter-Referenzwege als Liste
    n_tr = int(st.session_state.get("anzahl_trichter", 0) or 0)
    trichter_refwege = []
    for i in range(1, n_tr + 1):
        trichter_refwege.append(to_float(st.session_state.get(f"weg_trichter_{i}_m")))

    # Faktoren-Dict zusammenstellen
    st.session_state["faktoren"] = {
        "preset": st.session_state.get("std_preset"),
        "allgemein": {
            "anzahl_kraene": int(st.session_state.get("anzahl_kraene", 0) or 0),
            "anzahl_trichter": n_tr,
            "verbrennung_pro_trichter_Mg_h": to_float(st.session_state.get("trichter_verbrennung_Mg_h")),
        },
        "greifer": {
            "auswahl": gaus,
            "leergewicht_Mg": g_gewicht_Mg,
            "motorleistung_kW": g_motor_kW,
            "volumen_m3": g_vol_m3,
        },
        "muell": {
            "modus": st.session_state.get("muell_modus"),
            "gesamtmenge_Mg_a": to_float(st.session_state.get("muell_gesamt_Mg_a")),
            "anliefermenge_Mg_h": to_float(st.session_state.get("muell_anliefer_Mg_h")),
            "anlieferdauer_h": to_float(st.session_state.get("muell_anlieferdauer_h")),
            "dichte_einlagerung_Mg_m3": to_float(st.session_state.get("muell_dichte_einlagerung_Mg_m3")),
            "dichte_beschickung_Mg_m3": to_float(st.session_state.get("muell_dichte_trichter_Mg_m3")),
        },
        "referenzwege": {
            "heben_senken_m": to_float(st.session_state.get("weg_heben_m")),
            "katzfahrt_m": to_float(st.session_state.get("weg_katz_m")),
            "kranfahrt_m": to_float(st.session_state.get("weg_kran_m")),
            "oeffnen_schliessen_m": to_float(st.session_state.get("weg_oeffnen_m")),
            "trichterwege_m": trichter_refwege,  # Liste: Index 0 = Trichter 1
        },
        "geschwindigkeiten": {
            "heben_senken_m_min": to_float(st.session_state.get("v_heben_m_min")),
            "katzfahrt_m_min": to_float(st.session_state.get("v_katz_m_min")),
            "kranfahrt_m_min": to_float(st.session_state.get("v_kran_m_min")),
            "oeffnen_schliessen_einh": to_float(st.session_state.get("v_oeffnen_einh")),
        },
        "beschleunigungen": {
            "heben_senken_m_s2": to_float(st.session_state.get("a_heben_m_s2")),
            "katzfahrt_m_s2": to_float(st.session_state.get("a_katz_m_s2")),
            "kranfahrt_m_s2": to_float(st.session_state.get("a_kran_m_s2")),
            "oeffnen_schliessen_m_s2": to_float(st.session_state.get("a_oeffnen_m_s2")),
        },
    }

    st.session_state["ready_for_analysis"] = True
    st.toast("Eingaben gespeichert ✅", icon="✅")
    time.sleep(2)
    st.switch_page("pages/Auswertung.py")

