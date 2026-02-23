### Seite Wege: Hier werden die Referenzwege für die verschiedenen Fahrten abgefragt. Alle Werte werden im Session-State gespeichert, damit sie auf den folgenden Seiten verfügbar sind.
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
# Eigene Module mit Funktionen
from ui.components import number_standard
from common.page_init import page_init
from common.flow import success_feedback
# Standardwerte
from config.standards import wege

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Wege", "📐", "centered")

## Container im Session State für die Wegedaten erstellen, sofern noch nicht vorhanden
ist_state = st.session_state.setdefault("ist_anlage", {})
wege_state = ist_state.setdefault("wege", {})
# Dynamischer Variablen für die Trichterwege, da die Anzahl der Trichter variabel ist
weg_trichter = {}
anlage = ist_state.get("anlage", {})
anzahl_trichter = int(anlage.get("anzahl_trichter", 0))

## UI-Inhalte der Wegeseite
st.title("📐 Referenzwege")
st.info("Auf dieser Seite erfassen Sie Referenzwege für die einzelnen Bewegungen des Krans.\n\n"
        "Die Wege werden zusammen mit Geschwindigkeit und Beschleunigung zur Berechnung von Spielzeiten, "
        "Energiebedarf und Vergleich IST/NEU verwendet.")

weg_hebensenken_m = number_standard(
    "Referenzweg Heben senken [m]",
    wege["heben_senken_m"],
    0,
    1,
    200,
    "wg_hs_m",
    "Typischer Hubweg pro Zyklus. Bestimmt die Dauer und den Energiebedarf der Hubbewegung.",
    0
)
weg_katzfahrt_m = number_standard(
    "Referenzweg Katzfahrt [m]",
    wege["katzfahrt_m"],
    0,
    1,
    200,
    "wg_ktzfhrt_m",
    "Typische Fahrstrecke der Katze pro Zyklus. Beeinflusst Spielzeit und Energiebedarf der Katzfahrt.",
    0
)
weg_kranfahrt_m = number_standard(
    "Referenzweg Kranfahrt Einlagern [m]",
    wege["kranfahrt_einlagern_m"],
    0,
    1,
    200,
    "wg_krnfhrt_m",
    "Typische Fahrstrecke des Krans beim Einlagern pro Zyklus. Beeinflusst Spielzeit und Energiebedarf der Kranfahrt.",
    0
)
if ist_state.get("greifer", {}).get("typ") == "vierseil_greifer":
    weg_oeffnenschliessn_m = number_standard(
        "Referenzweg Greifer Öffnen/Schließen",
        wege["oeffnen_schliessen_m"],
        0,
        1,
        200,
        "wg_ofnschl_m",
        "Typischer Bewegungsweg beim Öffnen/Schließen. Wird zur Abschätzung der Zeit-/Energieanteile dieser Bewegung verwendet.",
        0
    )
else: 
    weg_oeffnenschliessn_m = 0 # Bei Hydraulikgreifer wird der Öffnen/Schließen-Weg nicht berücksichtigt, da die Bewegung nicht direkt mechanisch über Rollen erfolgt

if anzahl_trichter > 0:
    for zahl in range(anzahl_trichter):
        key = f"trichterweg_{zahl + 1}_m"
        weg_trichter[zahl] = number_standard(
            f"Referenzweg Trichter {zahl + 1}",
            wege[key],
            0,
            1,
            200,
            f"wg_tr_{zahl + 1}",
            f"Typische Fahrstrecke zu Trichter/Schure {zahl + 1}. Bestimmt die Fahranteile je Trichter und beeinflusst die Gesamtspielzeit.",
            0,
        )
else:
    st.warning("Bitte zuerst in der Seite \"Anlage\" die Anzahl der Trichter eingeben.")

button = st.button("Speichern", "speichern_wege")

if button:
    wege_state.update(
        # alles in den Session-State speichern, damit sie auf den folgenden Seiten verfügbar ist
        {
            "weg_hebensenken_m": weg_hebensenken_m,
            "weg_katzfahrt_m": weg_katzfahrt_m,
            "weg_kranfahrt_einlagern_m": weg_kranfahrt_m,
            "weg_oeffnen_schliessen_m": weg_oeffnenschliessn_m,
            "weg_trichter_m": weg_trichter,
        }
    )
    st.session_state["wege_saved"] = True # Flag setzen, dass diese Seite gespeichert wurde

# Feedback und Weiterleitung zur nächsten Seite, wenn gespeichert wurde
success_feedback("wege", "rueckspeisung")