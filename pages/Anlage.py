import streamlit as st
import pandas as pd
from auth import check_login
from ui.components import number_standard, text_standard, selectbox_standard, checkbox_standard
from config.standards import STANDARDWERTE
import time

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
    "Anzahl der Trichter",
    STANDARDWERTE["Anlage"]["Anzahl Trichter"],
    1, 1, 10,
    "anzl_trichter",
    "Anzahl der Trichter zum Beschicken",
    0
)
verbrennung_trichter = number_standard(
    "Verbrennung je Trichter [t]",
    STANDARDWERTE["Anlage"]["Verbrennung je Trichter"],
    0, 0.1, 100,
    "vbrng_trichter",
    "Verbrennung pro Trichter in Tonnen"
)

# Mülldaten
st.write("# :grey[Eingabe der Mülldaten]")
müll_anlieferung_h = number_standard(
    "Durchschnittliche Müllanliefermenge pro Stunde [t]",
    STANDARDWERTE["Müll"]["Müll Anliefermenge in der Stunde[t]"],
    0, 1, 1000,
    "ml_anlfrmg",
)
müll_dichte_beschickung = number_standard(
    "Müll Dichte bei Beschickung [t/m³]",
    STANDARDWERTE["Müll"]["Müll Dichte Beschickung[t/m³]"],
    0, 0.1, 2,
    "ml_dcht_beschickung",
)
müll_dichte_anlieferung = number_standard(
    "Müll Dichte bei Einlagerung [t/m³]",
    STANDARDWERTE["Müll"]["Müll Dichte Einlagerung[t/m³]"],
    0, 0.1, 2,
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
energie_kosten = number_standard(
    "Höhe der Tarifenergiekosten des Standortes [c/kWh]",
    df_laender.loc[df_laender["Land"]==anlage_standort, "Preis in c/kWh"].iloc[0],
    0,
    0.1,
    200,
    "enrgy_kostn",
    "Die Energiekosten von c/kWh für die Anlage",
)

button = st.button("Speichern und weiter")

if button:
    # alles in den Session-State schreiben
    anlage_state.update(
        {
            "anzahl_kraene": anzahl_kraene,
            "anzahl_trichter": anzahl_trichter,
            "verbrennung_trichter_t": verbrennung_trichter,
            "müll_anlieferung_h_t": müll_anlieferung_h,
            "müll_dichte_beschickung_t_pro_m3": müll_dichte_beschickung,
            "müll_dichte_anlieferung_t_pro_m3": müll_dichte_anlieferung,
            "anlage_standort": anlage_standort,
            "energie_kosten": energie_kosten,
            "müll_anlieferdauer": müll_anlieferdauer
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Greifer.py")
