import streamlit as st
import pandas as pd
from auth import check_login
from ui.components import number_standard, selectbox_standard, my_sidebar_nav
from config.standards import STANDARDWERTE
import time
from typing import cast
from ui.theme import set_background_auto_theme

my_sidebar_nav()

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)

st.set_page_config(layout = "centered")

check_login()

df_laender = pd.read_csv("tabellen/Stromländerpreise+CO2.csv", sep=';')

st.header("Allgemeinen Anlagendaten")

# Container für diese Seite im Session State
ist_state = st.session_state.setdefault("ist_anlage", {})
anlage_state = ist_state.setdefault("anlage", {})

# Allgemeine Daten
st.write("# :grey[Allgemeine Daten]")
anzahl_kraene = number_standard(
    "Anzahl der Kräne",
    STANDARDWERTE["Anlage"]["Anzahl Kräne"],
    1, 1, 10,
    "anzl_kraene",
    "Anzahl der Krane in der Anlage",
    0
)
anzahl_trichter = number_standard(
    "Anzahl der Trichter/Schuren",
    STANDARDWERTE["Anlage"]["Anzahl Trichter"],
    1, 1, 10,
    "anzl_trichter",
    "Anzahl der Trichter/Schuren zum Beschicken",
    0
)
verbrennung_trichter = number_standard(
    "Verbrennung je Trichter/Schure [kg]",
    STANDARDWERTE["Anlage"]["Verbrennung je Trichter"],
    0, 100, 100_000,
    "vbrng_trichter",
    "Verbrennung pro Trichter/Schure in kg"
)

# Mülldaten
st.write("# :grey[Eingabe der Mülldaten]")
müll_anlieferung_h = number_standard(
    "Durchschnittliche Müllanliefermenge pro Stunde [kg]",
    STANDARDWERTE["Müll"]["Müll Anliefermenge in der Stunde[kg]"],
    0, 100, 1_000_000,
    "ml_anlfrmg",
)
müll_dichte_beschickung = number_standard(
    "Müll Dichte bei Beschickung [kg/m³]",
    STANDARDWERTE["Müll"]["Müll Dichte Beschickung[kg/m³]"],
    0, 100, 2_000,
    "ml_dcht_beschickung",
)
müll_dichte_anlieferung = number_standard(
    "Müll Dichte bei Einlagerung [kg/m³]",
    STANDARDWERTE["Müll"]["Müll Dichte Einlagerung[kg/m³]"],
    0, 100, 2_000,
    "ml_dcht_anlieferung",
)
müll_anlieferdauer = number_standard(
    "Müll Anlieferdauer [h/d]",
    STANDARDWERTE["Müll"]["Müll Anlieferdauer Stunden[h]"],
    1, 1, 24,
    "ml_anlieferdr",
    "Durchschnittliche tägliche Anlieferdauer in Stunden",
    0
)

# Kosten etc.
anlage_standort = selectbox_standard(
    titel = "Standort der Anlage",
    standard = STANDARDWERTE["Anlage"]["Standort"],
    auswahl = df_laender["Land"].tolist(),
    key = "anl_standort",
    helptext = "In welchem Land befindet sich die Anlage?"
)
s = cast(pd.Series, df_laender.loc[df_laender["Land"] == anlage_standort, "Preis in c/kWh"]) 
preis = s.iloc[0] # Länderpreis direkt nach vorheriger Eingabe raussuchen
energie_kosten = number_standard(
    "Höhe der Tarifenergiekosten des Standortes [c/kWh]",
    preis,
    0,
    0.1,
    200,
    "enrgy_kostn",
    "Quelle zu automatischem Tarifvorschlag: https://de.statista.com/statistik/daten/studie/151260/umfrage//strompreise-fuer-industriekunden-in-europa/",
)

button = st.button("Speichern und weiter")

if button:
    # alles in den Session-State schreiben
    anlage_state.update(
        {
            "anzahl_kraene": anzahl_kraene,
            "anzahl_trichter": anzahl_trichter,
            "verbrennung_trichter_kg": verbrennung_trichter,
            "müll_anlieferung_h_kg": müll_anlieferung_h,
            "müll_dichte_beschickung_kg_pro_m3": müll_dichte_beschickung,
            "müll_dichte_anlieferung_kg_pro_m3": müll_dichte_anlieferung,
            "anlage_standort": anlage_standort,
            "energie_kosten": energie_kosten,
            "müll_anlieferdauer": müll_anlieferdauer
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Greifer.py")
