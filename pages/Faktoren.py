## Faktorenseite

from auth import check_login
import streamlit as st
from config.standards import STANDARDWERTE
import time


# NEU: Preset-Config & Loader
from config.presets import PRESET_SOURCES
from core.io import load_preset, to_float

# Konfiguration

TARGET_PAGE = "pages/Bewegungen.py"

st.set_page_config(page_title="Meine App", page_icon="🔒")
check_login()

# Preset-Lader

@st.cache_data(show_spinner=False)
def get_preset(name: str) -> dict:
    path = PRESET_SOURCES[name]
    return load_preset(path, name)

# Seite-UI

st.title("🔧 Faktoren eingeben")
st.write("\n")

# Faktoren-Auswahl
preset_options = ["Manuell"] + list(PRESET_SOURCES.keys())
auswahl_standard = st.selectbox(
    "Daten manuell eingeben oder Bestandsanlagenvorlagen verwenden?",
    preset_options,
    index=0,
    key="std_preset"
)

# Preset laden & direkt zur Auswertung
if auswahl_standard in PRESET_SOURCES:
    if st.button(f"{auswahl_standard} – Voreinstellung laden & zur Auswertung"):
        preset_dict = get_preset(auswahl_standard)
        st.session_state["faktoren"] = preset_dict
        st.session_state["ready_for_analysis"] = True
        st.toast(f"Voreinstellung ‚{auswahl_standard}‘ geladen ✅", icon="✅")
        time.sleep(2)
        st.switch_page(TARGET_PAGE)

# Manuelle Eingaben

# Allgemeines & Müllmengen
st.write("# :blue[Allgemeines & Müllmengen]")
st.write(":grey[Allgemeines]")

auswahl_kranzahl            = st.number_input("Anzahl der Krane", key="anzahl_kraene")
auswahl_trichterzahl        = st.number_input("Anzahl der Trichter", min_value=1, max_value=10, key="anzahl_trichter")
auswahl_trichterverbrennung = st.number_input("Verbrennung je Trichter in Mg/h", key="trichter_verbrennung_Mg_h")

# Greifer-Auswahl
auswahl_greifer_select = st.selectbox(
    "Greifer auswählen oder Daten  manuell eingeben?",
    [
        "Manuell eingeben",
        "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1",
        "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316"
    ],
    key="greifer_auswahl"
)

# Nur bei manueller Eingabe die Felder anzeigen
match auswahl_greifer_select:
    case "Manuell eingeben":  # Manuell
        auswahl_greifer_art     = st.selectbox("Greiferart", ["Vierseil-Greifer", "Hydraulikgreifer"], key="greiferart")
        auswahl_greifer_gewicht = st.number_input("Leergewicht Greifer in Mg", key="greifer_leergewicht_Mg")
        auswahl_greifer_inhalt  = st.number_input("Greifervolumen in m³", key="greifer_volumen_m3")
        # Motorleistung nur abfragen, wenn es ein Motorgreifer/Hydraulikgreifer ist
        if st.session_state.get("greiferart") == "Hydraulikgreifer":
                st.number_input("Motorleistung Greifer Öffnen/Schließen in kW", key="greifer_motor_kW")
    case "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        greifer_dict = STANDARDWERTE["Greifer"]["Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1"]
        for key, value in greifer_dict.items():
            st.write(f"**{key}:** {value}")
    case "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316":
        greifer_dict = STANDARDWERTE["Greifer"]["Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316"]
        for key, value in greifer_dict.items():
            st.write(f"**{key}:** {value}")

# Müllmengen
st.write(":grey[Müllmengen]")
auswahl_muell = st.selectbox(
    "Bei Müllmengen mit Standardwerten rechnen oder eigene Werte eingeben?",
    ["Werte eingeben", "Standard"],
    key="muell_modus"
)

if auswahl_muell == "Werte eingeben":
    auswahl_muell_gesamtmenge_jahr = st.number_input("Müllmenge in Mg pro Jahr", key="muell_gesamt_Mg_a")
    auswahl_muell_anliefermenge_h  = st.number_input("Anliefermenge in Mg pro Stunde", key="muell_anliefer_Mg_h")
    auswahl_muell_anlieferdauer    = st.number_input("Anlieferdauer in Stunden", key="muell_anlieferdauer_h")
    auswahl_muell_dichte_einlagern = st.number_input("Abfalldichte im Greifer bei Einlagerung in Mg/m³", key="muell_dichte_einlagerung_Mg_m3")
    auswahl_muell_dichte_trichter  = st.number_input("Abfalldichte im Greifer bei Trichterbeschickung in Mg/m³", key="muell_dichte_trichter_Mg_m3")

# Bewegungen und Geschwindigkeit

st.write("\n")
st.write("# :blue[Angaben zu Bewegungen und Referenzwege]")

auswahl_bewegungen = st.selectbox(
    "Bei Geschwindigkeiten und Beschleunigungen mit Standardwerten rechnen oder eigene Werte eingeben?",
    ["Werte eingeben", "Standard"],
    key="bewegung_modus"
)

if auswahl_bewegungen == "Werte eingeben":
    # Bewegungen (Geschwindigkeiten)
    st.write(":grey[Bewegungen]")
    auswahl_bewegung_hebensenken       = st.number_input("Geschwindigkeit Heben/Senken in m/min", key="v_heben_m_min")
    auswahl_bewegung_katzfahrt         = st.number_input("Geschwindigkeit Katzfahrt in m/min", key="v_katz_m_min")
    auswahl_bewegung_kranfahrt         = st.number_input("Geschwindigkeit Kranfahrt in m/min", key="v_kran_m_min")
    auswahl_bewegung_oeffnenschliessen = st.number_input("Geschwindigkeit Greifer Öffnen/Schließen", key="v_oeffnen_einh")

    # Beschleunigungen
    st.write(":grey[Beschleunigungen]")
    auswahl_beschleunigung_hebensenken       = st.number_input("Beschleuigung Heben/Senken in m/s²", key="a_heben_m_s2")
    auswahl_beschleunigung_katzfahrt         = st.number_input("Beschleunigung Katzfahrt in m/s²", key="a_katz_m_s2")
    auswahl_beschleunigung_kranfahrt         = st.number_input("Beschleunigung Kranfahrt in m/s²", key="a_kran_m_s2")
    auswahl_beschleunigung_oeffnenschliessen = st.number_input("Beschleunigung Greifer Öffnen/Schließen in m/s²", key="a_oeffnen_m_s2")


# Referenzwege
st.write(":grey[Referenzwege]")
auswahl_referenzweg_hebensenken       = st.number_input("Referenzweg Heben/Senken in m", key="weg_heben_m")
auswahl_referenzweg_katzfahrt         = st.number_input("Referenzweg Katzfahrt in m", key="weg_katz_m")
auswahl_referenzweg_kranfahrt         = st.number_input("Referenzweg Kranfahrt in m", key="weg_kran_m")
auswahl_referenzweg_oeffnenschliessen = st.number_input("Referenzweg Greifer Öffnen/Schließen in m", key="weg_oeffnen_m")

# Dynamische Trichter-Referenzwege
n_tr = int(auswahl_trichterzahl or 0)  # min/max 1..10
if n_tr > 0:
    st.write("Referenzwege je Trichter [m]")
    cols = st.columns(5)
    for i in range(1, n_tr + 1):
        col = cols[(i - 1) % len(cols)]
        with col:
            st.number_input(
                f"Trichter {i} in m",
                key=f"weg_trichter_{i}_m",
                min_value=0.0,
                step=0.1,
            )


############################################
#Hier darf ich nicht vergessen, dass ich bei manueller Eingabe noch die Motorleistungen ausrechnen muss
#für den session_state zum speichern dann
############################################



# Speichern & Wechseln (manuelle Eingaben übernehmen)
# Hier geht es vorallem um die Standard-Werte-Übernahme
if st.button("Auswahl speichern & zur Auswertung"):
    # Greiferwerte aus Auswahl ableiten (Konstanten oder Eingaben)
    gaus = st.session_state.get("greifer_auswahl")
    if gaus == "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        g_std = STANDARDWERTE["Greifer"]["Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1"]
        g_gewicht_Mg = to_float(g_std.get("Leergewicht in Mg"))
        g_motor_kW   = to_float(g_std.get("Motorleistung in kW"))
        g_vol_m3     = to_float(g_std.get("Greifervolumen in m³"))
        auswahl_greifer_art = g_std.get("Greiferart")
    elif gaus == "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316":
        g_std = STANDARDWERTE["Greifer"]["Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316"]
        g_gewicht_Mg = to_float(g_std.get("Leergewicht in Mg"))
        # g_motor_kW   = !! dieser Wert ist noch zu berechnen (abhängig vom Vierseil-Hubsystem)
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))  # Platzhalter bis Berechnung implementiert
        g_vol_m3     = to_float(g_std.get("Greifervolumen"))
        auswahl_greifer_art = g_std.get("Greiferart")
    elif gaus == "Manuell eingeben":
        # auswahl_greifer_art stammt aus Selectbox oben (nur bei manuell vorhanden)
        auswahl_greifer_art = st.session_state.get("greiferart")
        g_gewicht_Mg = to_float(st.session_state.get("greifer_leergewicht_Mg"))
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))
        g_vol_m3     = to_float(st.session_state.get("greifer_volumen_m3"))
    else:
        # Fallback (sollte nicht auftreten)
        auswahl_greifer_art = None
        g_gewicht_Mg = None
        g_motor_kW   = None
        g_vol_m3     = None

    # Müllwerte aus Auswahl ableiten (Konstanten oder Eingaben)
    gaus2 = st.session_state.get("muell_modus")
    if gaus2 == "Standard":
        m_std = STANDARDWERTE["Müll"]
        muell_dict = {
            "modus": "Standard",
            "gesamtmenge_Mg_a":          to_float(m_std.get("Müll Gesamtmenge im Jahr in Mg")),
            "anliefermenge_Mg_h":        to_float(m_std.get("Müll Anliefermenge in der Stunde")),
            "anlieferdauer_h":           to_float(m_std.get("Müll Anlieferdauer in Stunden")),
            "dichte_einlagerung_Mg_m3":  to_float(m_std.get("Müll Dichte Einlagerung in Mg/m³")),
            "dichte_beschickung_Mg_m3":  to_float(m_std.get("Müll Dichte Beschickung in Mg/m³")),
        }
    else:  # "Werte eingeben"
        muell_dict = {
            "modus": "Werte eingeben",
            "gesamtmenge_Mg_a":          to_float(st.session_state.get("muell_gesamt_Mg_a")),
            "anliefermenge_Mg_h":        to_float(st.session_state.get("muell_anliefer_Mg_h")),
            "anlieferdauer_h":           to_float(st.session_state.get("muell_anlieferdauer_h")),
            "dichte_einlagerung_Mg_m3":  to_float(st.session_state.get("muell_dichte_einlagerung_Mg_m3")),
            "dichte_beschickung_Mg_m3":  to_float(st.session_state.get("muell_dichte_trichter_Mg_m3")),
        }

    # Bewegungen & Beschleunigungen je nach Modus übernehmen
    beweg_modus = st.session_state.get("bewegung_modus")
    if beweg_modus == "Standard":
        g_std = STANDARDWERTE["Geschwindigkeiten"]
        b_std = STANDARDWERTE["Beschleunigungen"]
        geschw_dict = {
            "heben_senken_m_min":      to_float(g_std.get("heben_senken_m_min")),
            "katzfahrt_m_min":         to_float(g_std.get("katzfahrt_m_min")),
            "kranfahrt_m_min":         to_float(g_std.get("kranfahrt_m_min")),
            "oeffnen_schliessen_einh": to_float(g_std.get("oeffnen_schliessen_einh")),
        }
        beschl_dict = {
            "heben_senken_m_s2":       to_float(b_std.get("heben_senken_m_s2")),
            "katzfahrt_m_s2":          to_float(b_std.get("katzfahrt_m_s2")),
            "kranfahrt_m_s2":          to_float(b_std.get("kranfahrt_m_s2")),
            "oeffnen_schliessen_m_s2": to_float(b_std.get("oeffnen_schliessen_m_s2")),
        }
    else:
        geschw_dict = {
            "heben_senken_m_min":      to_float(st.session_state.get("v_heben_m_min")),
            "katzfahrt_m_min":         to_float(st.session_state.get("v_katz_m_min")),
            "kranfahrt_m_min":         to_float(st.session_state.get("v_kran_m_min")),
            "oeffnen_schliessen_einh": to_float(st.session_state.get("v_oeffnen_einh")),
        }
        beschl_dict = {
            "heben_senken_m_s2":       to_float(st.session_state.get("a_heben_m_s2")),
            "katzfahrt_m_s2":          to_float(st.session_state.get("a_katz_m_s2")),
            "kranfahrt_m_s2":          to_float(st.session_state.get("a_kran_m_s2")),
            "oeffnen_schliessen_m_s2": to_float(st.session_state.get("a_oeffnen_m_s2")),
        }

    # Trichter-Referenzwege als Liste
    n_tr_save = int(st.session_state.get("anzahl_trichter", 0) or 0)
    trichter_refwege = [
        to_float(st.session_state.get(f"weg_trichter_{i}_m"))
        for i in range(1, n_tr_save + 1)
    ]

    # Faktoren-Dict zusammenstellen
    st.session_state["faktoren"] = {
        "preset": st.session_state.get("std_preset"),
        "allgemein": {
            "anzahl_kraene": int(st.session_state.get("anzahl_kraene", 0) or 0),
            "anzahl_trichter": n_tr_save,
            "verbrennung_pro_trichter_Mg_h": to_float(st.session_state.get("trichter_verbrennung_Mg_h")),
        },
        "greifer": {
            "auswahl": gaus,
            "greiferart": auswahl_greifer_art,
            "leergewicht_Mg": g_gewicht_Mg,
            "motorleistung_kW": g_motor_kW,
            "volumen_m3": g_vol_m3,
        },
        "muell": muell_dict,
        "referenzwege": {
            "heben_senken_m": to_float(st.session_state.get("weg_heben_m")),
            "katzfahrt_m": to_float(st.session_state.get("weg_katz_m")),
            "kranfahrt_m": to_float(st.session_state.get("weg_kran_m")),
            "oeffnen_schliessen_m": to_float(st.session_state.get("weg_oeffnen_m")),
            "trichterwege_m": trichter_refwege,  # Index 0 = Trichter 1
        },
        "geschwindigkeiten": geschw_dict,
        "beschleunigungen":  beschl_dict,
        "motoren": {
            "hub_kW":  to_float(st.session_state.get("motor_hub_kW")),
            "hub_wirkungsgrad_pct":  to_float(st.session_state.get("wirkungsgrad_hub_pct")),
            "katz_kW": to_float(st.session_state.get("motor_katz_kW")),
            "katz_wirkungsgrad_pct": to_float(st.session_state.get("wirkungsgrad_katz_pct")),
            "kran_kW": to_float(st.session_state.get("motor_kran_kW")),
            "kran_wirkungsgrad_pct": to_float(st.session_state.get("wirkungsgrad_kran_pct")),
        },
    }

    st.session_state["ready_for_analysis"] = True
    st.toast("Eingaben gespeichert ✅", icon="✅")
    time.sleep(2)
    st.switch_page(TARGET_PAGE) #Zum Testen abgeändert um auf Bewegungen.py weiterzugehen.

