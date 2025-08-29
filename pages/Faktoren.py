import streamlit as st
import pandas as pd
import time

# -----------------------------
# CSV laden und vorbereiten
avg_koeln_preset = pd.read_csv("tabellen/AVG Köln.csv", sep=";", decimal=",", encoding="utf-8")
avg_koeln_preset.columns = avg_koeln_preset.columns.str.strip()
avg_koeln_preset["Beschreibung"] = avg_koeln_preset["Beschreibung"].astype(str).str.strip()
avg_koeln_preset.set_index("Beschreibung", inplace=True)
avg_koeln_preset = avg_koeln_preset[~avg_koeln_preset.index.duplicated(keep="first")]

# (Komma/Punkt) in float wandeln
def to_float(x, default=None):
    try:
        return float(str(x).replace(",", "."))
    except Exception:
        return default

# ------------------------------------------------------------------
# Kundenspezifische Voreinstellung (Preset)
# Trichterwege fest vorgeben:
_trichterwege = [10.0, 25.0, 30.0, 55.0]

STD_AVG_KOELN = {
    "preset": "AVG Köln",
    "allgemein": {
        "anzahl_kraene": int(to_float(avg_koeln_preset.loc["Anzahl Kräne", "Wert"], 0)),
        # anzahl_trichter an die Liste koppeln:
        "anzahl_trichter": len(_trichterwege),
        "verbrennung_pro_trichter_Mg_h": to_float(avg_koeln_preset.loc["Verbrennung je Trichter", "Wert"], 0),
    },
    "greifer": {
        "auswahl": "Manuell eingeben",
        "greiferart": str(avg_koeln_preset.loc["Greiferart", "Wert"]),
        "leergewicht_Mg": to_float(avg_koeln_preset.loc["Greifer Leergewicht", "Wert"], 0),
        "motorleistung_kW": to_float(avg_koeln_preset.loc["Motorleistung Greifer in kW", "Wert"], 0),
        "volumen_m3": to_float(avg_koeln_preset.loc["Greifervolumen", "Wert"], 0),
    },
    "muell": {
        "modus": "Standard",
        "gesamtmenge_Mg_a": to_float(avg_koeln_preset.loc["Müllmenge im Jahr", "Wert"], 0),
        "anliefermenge_Mg_h": to_float(avg_koeln_preset.loc["Anliefermenge Stunde", "Wert"], 0),
        "anlieferdauer_h": to_float(avg_koeln_preset.loc["Anlieferdauer Stunden", "Wert"], 0),
        "dichte_einlagerung_Mg_m3": to_float(avg_koeln_preset.loc["Dichte Einlagerung", "Wert"], 0),
        "dichte_beschickung_Mg_m3": to_float(avg_koeln_preset.loc["Dichte Beschickung", "Wert"], 0),
    },
    "referenzwege": {
        "heben_senken_m": to_float(avg_koeln_preset.loc["Referenzweg Heben/Senken", "Wert"], 0),
        "katzfahrt_m": to_float(avg_koeln_preset.loc["Referenzweg Katzfahrt", "Wert"], 0),
        "kranfahrt_m": to_float(avg_koeln_preset.loc["Referenzweg Kranfahrt Einlagern", "Wert"], 0),
        "oeffnen_schliessen_m": to_float(avg_koeln_preset.loc["Referenzweg Öffnen/Schließen", "Wert"], 0),
        "trichterwege_m": _trichterwege,  # <- Liste aus vier Trichterwegen
    },
    "geschwindigkeiten": {
        "heben_senken_m_min": to_float(avg_koeln_preset.loc["Geschwindigkeit Heben/Senken", "Wert"], 0),
        "katzfahrt_m_min": to_float(avg_koeln_preset.loc["Geschwindigkeit Katzfahrt", "Wert"], 0),
        "kranfahrt_m_min": to_float(avg_koeln_preset.loc["Geschwindigkeit Kranfahrt", "Wert"], 0),
        "oeffnen_schliessen_einh": to_float(avg_koeln_preset.loc["Geschwindigkeit Öffnen/Schließen", "Wert"], 0),
    },
    "beschleunigungen": {
        "heben_senken_m_s2": to_float(avg_koeln_preset.loc["Beschleunigung Heben/Senken", "Wert"], 0),
        "katzfahrt_m_s2": to_float(avg_koeln_preset.loc["Beschleunigung Katzfahrt", "Wert"], 0),
        "kranfahrt_m_s2": to_float(avg_koeln_preset.loc["Beschleunigung Kranfahrt", "Wert"], 0),
        "oeffnen_schliessen_m_s2": to_float(avg_koeln_preset.loc["Beschleunigung Öffnen/Schließen", "Wert"], 0),
    },
    "motoren": {
        "hub_kW": to_float(avg_koeln_preset.loc["Nennleistung Hubmotor", "Wert"], 0),
        "hub_wirkungsgrad_pct": to_float(avg_koeln_preset.loc["Wirkungsgrad Hubmotor", "Wert"], 0),
        "katz_kW": to_float(avg_koeln_preset.loc["Nennleistung Katzfahrt", "Wert"], 0),
        "katz_wirkungsgrad_pct": to_float(avg_koeln_preset.loc["Wirkungsgrad Katzfahrt", "Wert"], 0),
        "kran_kW": to_float(avg_koeln_preset.loc["Nennleistung Kranfahrt", "Wert"], 0),
        "kran_wirkungsgrad_pct": to_float(avg_koeln_preset.loc["Wirkungsgrad Kranfahrt", "Wert"], 0),
    },
}
# ------------------------------------------------------------------

# -----------------------------------
# Ab hier beginnt die Seite
st.title("🔧 Faktoren eingeben")
st.write("\n\n\n\n\n\n")

## Faktorenuswahl
auswahl_standard = st.selectbox(
    "Daten manuell eingeben oder Bestandsanlagenvorlagen verwenden?",
    ["Manuell", "AVG Köln"],
    key="std_preset"
)

# Wenn AVG Köln gewählt ist, Preset per Button laden & direkt wechseln
if auswahl_standard == "AVG Köln":
    if st.button("AVG Köln – Voreinstellung laden & zur Auswertung"):
        st.session_state["faktoren"] = STD_AVG_KOELN
        st.session_state["ready_for_analysis"] = True
        st.toast("Voreinstellung ‚AVG Köln‘ geladen ✅", icon="✅")
        time.sleep(2)
        st.switch_page("pages/Auswertung.py")

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
    auswahl_greifer_art     = "Hydraulikgreifer"
    auswahl_greifer_gewicht = 3.050
    auswahl_greifer_motor   = 18.8
    auswahl_greifer_inhalt  = 2.75
elif auswahl_greifer_select == "Vierseil_Mehrschalen Müllgreifer Mrs Greifer 1-26-6315-6316":
    auswahl_greifer_art     = "Vierseil-Greifer"
    auswahl_greifer_gewicht = 3.800
    auswahl_greifer_motor   = st.number_input("Hubmotorleistung Greifer Öffnen/Schließen in kW", key="greifer_motor_kW")
    auswahl_greifer_inhalt  = 4
elif auswahl_greifer_select == "Manuell eingeben":
    auswahl_greifer_art     = st.selectbox("Greiferart", ["Vierseil-Greifer","Hydraulikgreifer"])
    auswahl_greifer_gewicht = st.number_input("Leergewicht Greifer in Mg", key="greifer_leergewicht_Mg")
    auswahl_greifer_motor   = st.number_input("Motorleistung Greifer für Öffnen/Schließen in kW (Hubmotor oder Hydraulikmotor)", key="greifer_motor_kW")
    auswahl_greifer_inhalt  = st.number_input("Greifervolumen in m³", key="greifer_volumen_m3")

st.write(":grey[Müllmengen]")
auswahl_muell = st.selectbox(
    " Bei Müllmengen mit Standard rechnen oder eigene Werte eingeben?",
    ["Standard", "Werte eingeben"],
    key="muell_modus"
)
if auswahl_muell == "Werte eingeben":
    auswahl_muell_gesamtmenge_jahr = st.number_input("Müllmenge in Mg pro Jahr", key="muell_gesamt_Mg_a")
    auswahl_muell_anliefermenge_h  = st.number_input("Anliefermenge in Mg pro Stunde", key="muell_anliefer_Mg_h")
    auswahl_muell_anlieferdauer    = st.number_input("Anlieferdauer in Stunden", key="muell_anlieferdauer_h")
    auswahl_muell_dichte_einlagern = st.number_input("Abfalldichte im Greifer bei Einlagerung in Mg/m³", key="muell_dichte_einlagerung_Mg_m3")
    auswahl_muell_dichte_trichter  = st.number_input("Abfalldichte im Greifer bei Trichterbeschickung in Mg/m³", key="muell_dichte_trichter_Mg_m3")
if auswahl_muell == "Standard":
    pass  # (Lastplan-Standard bleibt hier; Preset-Button ist oben bei auswahl_standard)

# Referenzwege
st.write("\n\n")
st.write("# :blue[Angaben zu Referenzwegen und Bewegungen]")
st.write(":grey[Referenzwege]")
auswahl_referenzweg_hebensenken       = st.number_input("Referenzweg Heben/Senken in m", key="weg_heben_m")
auswahl_referenzweg_katzfahrt         = st.number_input("Referenzweg Katzfahrt in m", key="weg_katz_m")
auswahl_referenzweg_kranfahrt         = st.number_input("Referenzweg Kranfahrt in m", key="weg_kran_m")
auswahl_referenzweg_oeffnenschliessen = st.number_input("Referenzweg Greifer Öffnen/Schließen in m", key="weg_oeffnen_m")

# --- Referenzwege je Trichter (dynamisch bis 10) ---
n_tr = int(auswahl_trichterzahl or 0)  # min/max am Widget gesetzt (1..10)
if n_tr > 0:
    st.write("Referenzwege je Trichter [m]")
    cols = st.columns(5)  # hübsch in bis zu 5 Spalten
    for i in range(1, n_tr + 1):
        col = cols[(i - 1) % len(cols)]
        with col:
            st.number_input(
                f"Trichter {i} in m",
                key=f"weg_trichter_{i}_m",
                min_value=0.0,
                step=0.1,
            )

st.write(":grey[Bewegungen]")
auswahl_bewegung_hebensenken       = st.number_input("Geschwindigkeit Heben/Senken in m/min", key="v_heben_m_min")
auswahl_bewegung_katzfahrt         = st.number_input ("Geschwindigkeit Katzfahrt in m/min", key="v_katz_m_min")
auswahl_bewegung_kranfahrt         = st.number_input("Geschwindigkeit Kranfahrt in m/min", key="v_kran_m_min")
auswahl_bewegung_oeffnenschliessen = st.number_input("Geschwindigkeit Greifer Öffnen/Schließen", key="v_oeffnen_einh")

st.write(":grey[Beschleunigungen]")
auswahl_beschleunigung_hebensenken       = st.number_input("Beschleuigung Heben/Senken in m/s²", key="a_heben_m_s2")
auswahl_beschleunigung_katzfahrt         = st.number_input("Beschleunigung Katzfahrt in m/s²", key="a_katz_m_s2")
auswahl_beschleunigung_kranfahrt         = st.number_input("Beschleunigung Kranfahrt in m/s²", key="a_kran_m_s2")
auswahl_beschleunigung_oeffnenschliessen = st.number_input("Beschleunigung Greifer Öffnen/Schließen in m/s²", key="a_oeffnen_m_s2")

# Motorenleistungen
st.write("\n\n")
st.write("# :blue[Angaben zur Leistung verwendeter Motoren]")
auswahl_motorleistung_hub  = st.number_input("Nennleistung des Hubmotors des Greifers in kW", key="motor_hub_kW")
auswahl_wirkungsgrad_hub   = st.number_input("Wirkungsgrad des Hubmotors des Greifers in %", key="wirkungsgrad_hub_pct")
auswahl_motorleistung_katz = st.number_input("Nennleistung des Katzfahrmotors in kW", key="motor_katz_kW")
auswahl_wirkungsgrad_katz  = st.number_input("Wirkungsgrad des Katzfahrmotors in %", key="wirkungsgrad_katz_pct")
auswahl_motorleistung_kran = st.number_input("Nennleistung des Kranfahrmotors in kW", key="motor_kran_kW")
auswahl_wirkungsgrad_kran  = st.number_input("Wirkungsgrad des Kranfahrmotors in %", key="wirkungsgrad_kran_pct")

##-----------------------------------------------------------------
# Speichern & Wechseln (manuelle Eingaben übernehmen)
if st.button("Auswahl speichern & zur Auswertung"):
    # Greiferwerte aus Auswahl ableiten (Konstanten oder Eingaben)
    gaus = st.session_state.get("greifer_auswahl")
    if gaus == "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        g_gewicht_Mg = 3.05
        g_motor_kW   = 18.8
        g_vol_m3     = 2.75
        auswahl_greifer_art = "Hydraulikgreifer"
    elif gaus == "Vierseil_Mehrschalen Müllgreifer Mrs Greifer 1-26-6315-6316":
        g_gewicht_Mg = 3.8
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))
        g_vol_m3     = 4.0
        auswahl_greifer_art = "Vierseil-Greifer"
    else:  # Manuell eingeben
        g_gewicht_Mg = to_float(st.session_state.get("greifer_leergewicht_Mg"))
        g_motor_kW   = to_float(st.session_state.get("greifer_motor_kW"))
        g_vol_m3     = to_float(st.session_state.get("greifer_volumen_m3"))
        # auswahl_greifer_art kommt aus dem Selectbox oben

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
    st.switch_page("pages/Auswertung.py")
