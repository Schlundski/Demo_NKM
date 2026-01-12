# Seite zur Auswahl des Greifers, und Eingabe, bzw. Befüllung der Greiferparameter
import streamlit as st
from ui.components import number_standard
import config.standards as std
import time
from auth import check_login

check_login()

standard_greifer_hydraulik = std.STANDARDWERTE["Greifer"]["Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1"]

st.title("Greiferkonfiguration")

# Container im Session State
ist_state = st.session_state["ist_anlage"]
greifer_state = ist_state.setdefault("greifer", {})

# Radio Buttons erstellen
greifer_Arten = [std.viers["Greiferart"], std.hydr["Greiferart"]]
auswahl = st.radio("Greiferart:", greifer_Arten, key="radio_greifer_Arten")

# Platzhalter für gemeinsame Variablen
gew_greifer_leer = None
vol_greifer = None
ges_greifen = None
bes_greifen = None

# Vierseil-Greifer
if auswahl == std.viers["Greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [t]",
        std.viers["Leergewicht"],
        0, 0.1, 15,
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
elif auswahl == std.hydr["Greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [t]",
        std.hydr["Leergewicht"],
        0, 0.1, 15,
        "leergew",
    )
    vol_greifer = number_standard(
        "Greifervolumen [m³]",
        std.hydr["Greifervolumen"],
        0, 0.1, 15,
        "volgreif",
    )
    ges_greifen = number_standard(
        "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
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
            "leergewicht_t": gew_greifer_leer,
            "volumen_m3": vol_greifer,
            "geschwindigkeit_m_pro_min": ges_greifen,
            "beschleunigung_m_pro_s2": bes_greifen,
        }
    )
    if auswahl == std.viers["Greiferart"]:
        greifer_state.update(
            {
                "typ": "Vierseil-Greifer",
                "motorleistung_kw": standard_greifer_hydraulik["Motorleistung"],
                "wirkungsgrad_hydraulik": standard_greifer_hydraulik["Wirkungsgrad"],
                "volumenstrom_l_pro_min": standard_greifer_hydraulik["Volumenstrom"],
                "betriebsdruck_bar": standard_greifer_hydraulik["Betriebsdruck"]
            }
        )
    elif auswahl == std.hydr["Greiferart"]:
        greifer_state.update(
            {
                "typ": "Hydraulikgreifer",
                "motorleistung_kw": p_hydr_motor,
                "wirkungsgrad_hydraulik": n_hydr_motor,
                "volumenstrom_l_pro_min": volumenstrom,
                "betriebsdruck_bar": betriebsdruck,
            }
        )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Krananlage.py")


