### Seite Rückspeisung: Hier werden die Rückspeisungsfaktoren für die verschiedenen Fahrten abgefragt. Je nach Auswahl des Greifertyps auf der vorherigen Seite wird auch die Rückspeisung bei Greifer Öffnen/Schließen abgefragt oder nicht. Alle Werte werden im Session-State gespeichert, damit sie auf den folgenden Seiten verfügbar sind.
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
# Eigene Module mit Funktionen
from ui.components import rueckspeisung_standard
from common.page_init import page_init
from common.flow import success_feedback
# Standardwerte
from config.standards import ruecksp

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Rückspeisung", "♻️", "centered")

## Container im Session State für die Rückspeisungsdaten erstellen, sofern noch nicht vorhanden
ist_state =st.session_state.setdefault("ist_anlage", {})
rueckspeisung_state = ist_state.setdefault("rueckspeisung", {})

## UI-Inhalte der Rückspeisungsseite
st.title("Rückspeisungen")
st.info("Auf dieser Seite legen Sie fest, ob und in welchem Umfang beim Abbremsen Energie in das Netz zurückgespeist wird.\n"
        "Die Rückspeisung reduziert den berechneten Energieverbrauch und damit auch Kosten und CO₂.\n\n"
        "Je nach Greifertyp wird zusätzlich die Rückspeisung beim Öffnen/Schließen berücksichtigt.")

# Abfrage des Greifertyps: Hydraulikgreifer -> keine Greiferrückspeisung
greifer_typ = ist_state.get("greifer", {}).get("typ")
if (greifer_typ=="Vierseil-Greifer"):
    rueckspeisung_greifer = rueckspeisung_standard(
        "Rückspeisung Greifer", 
        ruecksp["fu_wirkungsgrad_greifer"], 
        0, 0.01, 1, 
        "rckspng_grfr", 
        "Gibt an, ob und in welchem Umfang beim Öffnen/Schließen des Greifers Energie in das Netz zurückgespeist wird. \n"
        "Reduziert den berechneten Energieverbrauch dieser Bewegung.", 
        2
    )
else:
    rueckspeisung_greifer = [0,0]

rueckspeisung_hub = rueckspeisung_standard(
    "Rückspeisung Hubfahrt",
    ruecksp["fu_wirkungsgrad_hubfahrt"],
    0,
    0.01,
    1,
    "rckspng_hb",
    "Gibt an, ob beim Absenken oder Abbremsen der Hubbewegung Energie zurückgewonnen wird. \n \
    Beeinflusst direkt den Energiebedarf der Hubfahrt.",
    2
)

rueckspeisung_kran = rueckspeisung_standard(
    "Rückspeisung Kranfahrt",
    ruecksp["fu_wirkungsgrad_kranfahrt"],
    0,
    0.01,
    1,
    "rckspng_krn",
    "Gibt an, ob beim Abbremsen der Kranbewegung Energie in das Netz zurückgespeist wird. \n \
    Reduziert den Energieverbrauch der horizontalen Fahrbewegung.",
    2
)

rueckspeisung_katz = rueckspeisung_standard(
    "Rückspeisung Katzfahrt",
    ruecksp["fu_wirkungsgrad_katzfahrt"],
    0,
    0.01,
    1,
    "rckspng_ktzfhrt",
    "Gibt an, ob beim Abbremsen der Katzfahrt Energie zurückgewonnen wird. \n \
    Beeinflusst den berechneten Energiebedarf der Querbewegung.",
    2
)

button = st.button("Speichern", "speichern_rueckspeisung")

if button:
    rueckspeisung_state.update(
        # alles in den Session-State speichern, damit es auf den folgenden Seiten verfügbar ist
        {
            "faktor_greifer": rueckspeisung_greifer[1],
            "fu_wirkungsgrad_greifer": rueckspeisung_greifer[0],
            "faktor_hub": rueckspeisung_hub[1],
            "fu_wirkungsgrad_hub": rueckspeisung_hub[0],
            "faktor_kran": rueckspeisung_kran[1],
            "fu_wirkungsgrad_kran": rueckspeisung_kran[0],
            "faktor_katze": rueckspeisung_katz[1],
            "fu_wirkungsgrad_katze": rueckspeisung_katz[0]
        }
    )
    st.session_state["rueckspeisung_saved"] = True # Flag setzen, dass diese Seite gespeichert wurde

# Feedback und Weiterleitung zur nächsten Seite, wenn gespeichert wurde
success_feedback("rueckspeisung", "auswertung")