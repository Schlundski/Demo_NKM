# Seite zur Auswahl des Greifers, und Eingabe, bzw. Befüllung der Greiferparameter
import streamlit as st
from ui.components import number_standard, my_sidebar_nav
import config.standards as std
import time
from auth import check_login
from ui.theme import set_background_auto_theme

my_sidebar_nav()

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)

st.set_page_config(layout = "centered")

check_login()



standard_greifer_hydraulik = std.STANDARDWERTE["Greifer"]["Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1"]

st.title("Greiferkonfiguration")

# Container im Session State
ist_state = st.session_state["ist_anlage"]
greifer_state = ist_state.setdefault("greifer", {})

# Vorzeitige Deklaration, um theoretisch ungebundene Werte zu vermeiden
oeffnungszeit_greifen = std.hydr["Oeffnungszeit"]
schliesszeit_greifen = std.hydr["Schliesszeit"]
p_hydr_motor = std.hydr["Motorleistung"]
n_hydr_motor = std.hydr["Wirkungsgrad"]
volumenstrom = std.hydr["Volumenstrom"]
betriebsdruck = std.hydr["Betriebsdruck"]
gew_greifer_leer = std.hydr["Leergewicht"]
vol_greifer = std.hydr["Greifervolumen"]
ges_greifen = std.hydr["Greifgeschwindigkeit"]
bes_greifen = std.hydr["Greifbeschleunigung"]
auswahl_parameter = "Schließ/Öffnungszeit"

# Radio Buttons erstellen
greifer_Arten = [std.viers["Greiferart"], std.hydr["Greiferart"]]
auswahl_greifer = st.radio("Greiferart:", greifer_Arten, key="radio_greifer_Arten")
if auswahl_greifer not in greifer_Arten:
    auswahl_greifer = std.viers["Greiferart"]  # Standardwert setzen, falls ungültige Auswahl getroffen wird


# Vierseil-Greifer
if auswahl_greifer == std.viers["Greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [kg]",
        std.viers["Leergewicht"],
        0, 100, 20_000,
        "leergew",
    )
    vol_greifer = number_standard(
        "Greifervolumen [m³]",
        std.viers["Greifervolumen"],
        0, 0.1, 15,
        "volgreif",
    )
    ges_greifen = number_standard(
        "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
        std.viers["Greifgeschwindigkeit"],
        0, 1, 200,
        "gesgreif",
    )
    bes_greifen = number_standard(
        "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
        std.viers["Greifbeschleunigung"],
        0, 0.1, 10,
        "besgreif",
    )

# Hydraulikgreifer
elif auswahl_greifer == std.hydr["Greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [kg]",
        std.hydr["Leergewicht"],
        0, 100, 20_000,
        "leergew",
    )
    vol_greifer = number_standard(
        "Greifervolumen [m³]",
        std.hydr["Greifervolumen"],
        0, 0.1, 15,
        "volgreif",
    )
    # Die Auswahl, ob Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingegeben werden soll
    auswahl_parameter = st.radio("Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingeben?", 
             ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"], key="radio_greifer_oeffnen_schliessen")
    if auswahl_parameter not in ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"]:
        auswahl_parameter = "Schließ/Öffnungszeit"  # Standardwert setzen, falls ungültige Auswahl getroffen wird

    if auswahl_parameter == "Schließ/Öffnungszeit":
        oeffnungszeit_greifen = number_standard(
            "Öffnungszeit [s]",
            std.hydr["Oeffnungszeit"],
            0, 1, 30,
            "oeffnzeit",
        )
        schliesszeit_greifen = number_standard(
            "Schließzeit [s]",
            std.hydr["Schliesszeit"],
            0, 1, 30,
            "schliesszeit",
        )

    if auswahl_parameter == "Geschwindigkeit/Beschleunigung":
        ges_greifen = number_standard(
            "Greifergeschwindigkeit beim Öffnen/Schließen [m/s]",
            std.hydr["Greifgeschwindigkeit"],
            0, 1, 200,
            "gesgreif",
        )
        bes_greifen = number_standard(
            "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
            std.hydr["Greifbeschleunigung"],
            0, 0.1, 10,
            "besgreif",
        )
    
    p_hydr_motor = number_standard(
        "Motorleistung [kW]",
        std.hydr["Motorleistung"],
        0, 1, 250,
        "motorleist",
    )
    n_hydr_motor = number_standard(
        "Wirkungsgrad Hydraulik",
        std.hydr["Wirkungsgrad"],
        0, 0.01, 1,
        "wirkhyrd",
    )
    volumenstrom = number_standard(
        "Volumenstrom [l/min]",
        std.hydr["Volumenstrom"],
        0, 1, 150,
        "volstr",
    )
    betriebsdruck = number_standard(
        "Betriebsdruck [bar]",
        std.hydr["Betriebsdruck"],
        0, 1, 300,
        "betdruck",
    )
else:
    st.write("Bitte wählen Sie die Art des Greifers aus")

button = st.button("Speichern und weiter")

if button:
    # Basisdaten immer, egal welcher Typ
    greifer_state.update(
        {
            "auswahl_parameter": auswahl_parameter,
            "leergewicht_kg": gew_greifer_leer,
            "volumen_m3": vol_greifer,
            "geschwindigkeit_m_pro_min": ges_greifen,
            "beschleunigung_m_pro_s2": bes_greifen,
            "oeffnungszeit_s": oeffnungszeit_greifen,
            "schliesszeit_s": schliesszeit_greifen,
            "typ": auswahl_greifer,
            "motorleistung_kw": p_hydr_motor,
            "wirkungsgrad_hydraulik": n_hydr_motor,
            "volumenstrom_l_pro_min": volumenstrom,
            "betriebsdruck_bar": betriebsdruck,
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Krananlage.py")


