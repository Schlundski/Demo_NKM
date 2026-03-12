### Seite für die Eingabe der allgemeinen Anlagendaten
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
import pandas as pd
# Eigene Module mit Funktionen
from ui.components import number_standard, selectbox_standard
from typing import cast
from common.page_init import page_init
from common.flow import success_feedback
# Standardwerte
from config.standards import anlage, muell

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Anlagendaten", "🏭", "centered")

## Länderpreise für automatischen Tarifvorschlag laden
df_laender = pd.read_csv("tabellen/Stromländerpreise+CO2.csv", sep=';')
df_laender = df_laender[df_laender["Land"].str.strip().str.lower() != "co2faktor"] # Zeile CO2-Faktoren rausnehmen

## Container für diese Seite im Session State erstellen, sofern noch nicht vorhanden
ist_state = st.session_state.setdefault("ist_anlage", {})
anlage_state = ist_state.setdefault("anlage", {})

## UI-Inhalte der Anlagenseite
st.title("🏭Allgemeinen Anlagendaten")
st.info("Auf dieser Seite erfassen Sie die grundlegenden technischen und betrieblichen Kenndaten der bestehenden Anlage.\n\n"
        "Diese Werte bilden die Grundlage für die anschließende Energie-, Kosten- und CO₂-Berechnung.")

# Allgemeine Daten
st.subheader(":grey[Allgemeine Daten]")
anzahl_kraene = number_standard(
    "Anzahl der Kräne",
    anlage["anzahl_kraene"],
    anlage_state.get("anzahl_kraene", anlage["anzahl_kraene"]),
    1, 1, 10,
    "anzl_kraene",
    "Wie viele Krananlagen gleichzeitig zur Beschickung/Handhabung genutzt werden. Wird zur Skalierung von Energie, Kosten und CO₂ verwendet",
    0
)
anzahl_trichter = number_standard(
    "Anzahl der Trichter/Schuren",
    anlage["anzahl_trichter"],
    anlage_state.get("anzahl_trichter", anlage["anzahl_trichter"]),
    1, 1, 10,
    "anzl_trichter",
    "Wie viele Beschickungsstellen (Trichter/Schuren) die Anlage besitzt. Relevant für die Abschätzung von Spielzyklen und Materialumschlag.",
    0
)
verbrennung_trichter = number_standard(
    "Verbrennung je Trichter/Schure in der Stunde [kg/h]",
    anlage["verbrennung_je_trichter_kg"],
    anlage_state.get("verbrennung_trichter_kg", anlage["verbrennung_je_trichter_kg"]),
    0, 100, 100_000,
    "vbrng_trichter",
    "Masse, die je Trichter/Schure pro Stunde umgesetzt wird. Bestimmt die erforderliche Umschlagmenge und damit Betriebszeiten."
)

# Mülldaten
st.subheader(":grey[Eingabe der Mülldaten]")
muell_anlieferung_h = number_standard(
    "Durchschnittliche Müllanliefermenge pro Stunde [kg]",
    muell["anliefermenge_kg_pro_stunde"],
    anlage_state.get("muell_anlieferung_h_kg", muell["anliefermenge_kg_pro_stunde"]),
    0, 100, 1_000_000,
    "ml_anlfrmg",
    "„Durchschnittlicher Massenstrom der Anlieferung. Grundlage für die tägliche Umschlagmenge und die Auslastung."
)
muell_dichte_beschickung = number_standard(
    "Müll Dichte bei Beschickung [kg/m³]",
    muell["dichte_beschickung_kg_m3"],
    anlage_state.get("muell_dichte_beschickung_kg_pro_m3", muell["dichte_beschickung_kg_m3"]),
    0, 100, 2_000,
    "ml_dcht_beschickung",
    "Schüttdichte im Greifer bei der Beschickung. Einfluss auf Greifervolumen, Zyklenanzahl und Spielzeit."
)
muell_dichte_anlieferung = number_standard(
    "Müll Dichte bei Einlagerung [kg/m³]",
    muell["dichte_einlagerung_kg_m3"],
    anlage_state.get("muell_dichte_anlieferung_kg_pro_m3", muell["dichte_einlagerung_kg_m3"]),
    0, 100, 2_000,
    "ml_dcht_anlieferung",
    "Schüttdichte im Bunker/bei Einlagerung. Wird genutzt, um Volumen- und Weg-/Zeitanteile realistisch zu bewerten."
)
muell_anlieferdauer = number_standard(
    "Müll Anlieferdauer [h/d]",
    muell["anlieferdauer_stunden_pro_tag"],
    anlage_state.get("muell_anlieferdauer", muell["anlieferdauer_stunden_pro_tag"]),
    1, 1, 24,
    "ml_anlieferdr",
    "Wie viele Stunden pro Tag Müll angeliefert wird. Bestimmt die tägliche Gesamtmenge (Massenstrom * Zeit).",
    0
)

# Kosten etc.
st.subheader(":grey[Standort und Kosten]")
anlage_standort = selectbox_standard(
    titel="Standort der Anlage",
    standard=anlage["standort"],
    wert=anlage_state.get("anlage_standort"),
    auswahl=df_laender["Land"].tolist(),
    key="anl_standort",
    helptext="Land/Region der Anlage. Daraus werden Strompreis und CO₂-Faktoren abgeleitet."
)

# Automatischer Tarifvorschlag basierend auf Standort
auswahl_land = cast(pd.Series, df_laender.loc[df_laender["Land"] == anlage_standort, "Preis in c/kWh"]) 
preis = auswahl_land.iloc[0]

energie_kosten = number_standard(
    "Höhe der Tarifenergiekosten des Standortes [c/kWh]",
    preis,
    preis,
    0,
    0.1,
    200,
    "enrgy_kostn",
    "Strompreis für die Berechnung der Betriebskosten. Vorschlag wird aus der Ländertabelle übernommen, kann aber manuell angepasst werden.",
)

success_feedback("anlage", "greifer")

if st.session_state.get("speichern_anlage"):
    anlage_state.update(
        # alles in den Session-State speichern, damit es auf den folgenden Seiten verfügbar ist
        {
            "anzahl_kraene": anzahl_kraene,
            "anzahl_trichter": anzahl_trichter,
            "verbrennung_trichter_kg": verbrennung_trichter,
            "muell_anlieferung_h_kg": muell_anlieferung_h,
            "muell_dichte_beschickung_kg_pro_m3": muell_dichte_beschickung,
            "muell_dichte_anlieferung_kg_pro_m3": muell_dichte_anlieferung,
            "anlage_standort": anlage_standort,
            "energie_kosten": energie_kosten,
            "muell_anlieferdauer": muell_anlieferdauer
        }
    )
    st.session_state["anlage_saved"] = True
    st.rerun() # Rerun, damit der Weiter-Button erscheint