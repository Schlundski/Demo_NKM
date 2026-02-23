### Seite zur Auswahl des Greifers, und Eingabe, bzw. Befüllung der Greiferparameter
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
# Eigene Module mit Funktionen
from ui.components import number_standard
from common.page_init import page_init
from common.flow import success_feedback
# Standardwerte
from config.standards import hydr, viers

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Greiferdaten", "🪝", "centered")

## Vorzeitige Deklaration, um theoretisch ungebundene Werte zu vermeiden
oeffnungszeit_greifen = hydr["oeffnungszeit_s"]
schliesszeit_greifen = hydr["schliesszeit_s"]
p_hydr_motor = hydr["motorleistung_kw"]
n_hydr_motor = hydr["wirkungsgrad"]
volumenstrom = hydr["volumenstrom_l_min"]
betriebsdruck = hydr["betriebsdruck_bar"]
gew_greifer_leer = hydr["leergewicht_kg"]
vol_greifer = hydr["greifervolumen_m3"]
ges_greifen = hydr["greifgeschwindigkeit_m_min"]
bes_greifen = hydr["greifbeschleunigung_m_s2"]
auswahl_parameter = "Schließ/Öffnungszeit"

## Container im Session State 
ist_state = st.session_state.setdefault("ist_anlage", {})
greifer_state = ist_state.setdefault("greifer", {})

## UI-Inhalte der Greiferseite
st.title("🪝Greiferdaten")
st.info("Auf dieser Seite wählen Sie den Greifertyp und erfassen die wichtigsten technischen Kenndaten.\n\n"
        "Die Angaben bestimmen die Greifer-Spielzeiten und (bei Hydraulik) den Energiebedarf der Hydraulik - "
        "und fließen direkt in die Energie-, Kosten- und CO₂-Berechnung ein.")

# Radio Buttons erstellen für Greiferauswahl

greifer_Arten = [viers["greiferart"], hydr["greiferart"]]
auswahl_greifer = st.radio("Greiferart:", greifer_Arten, key="radio_greifer_Arten",
                           help="Wählen Sie den verwendeten Greifertyp. \
                            Je nach Typ unterscheiden sich die relevanten Eingabeparameter \
                            und die Energieberechnung.")

# Vierseil-Greifer
if auswahl_greifer == viers["greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [kg]",
        viers["leergewicht_kg"],
        0, 100, 20_000,
        "leergew",
        "Eigengewicht des Greifers ohne Last. Relevant für Bewegungsenergie und mechanische Belastung"
    )
    vol_greifer = number_standard(
        "Greifervolumen [m³]",
        viers["greifervolumen_m3"],
        0, 0.1, 15,
        "volgreif",
        "Volumen, das der Greifer pro Zyklus aufnehmen kann. Bestimmt die Zyklenanzahl und damit Spielzeit/Energie."
    )
    ges_greifen = number_standard(
        "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
        viers["greifgeschwindigkeit_m_min"],
        0, 1, 200,
        "gesgreif",
        "Mittlere Öffnungs-/Schließgeschwindigkeit des Greifers. Beeinflusst die Zeit pro Zyklus."
    )
    bes_greifen = number_standard(
        "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
        viers["greifbeschleunigung_m_s2"],
        0, 0.1, 10,
        "besgreif",
        "Beschleunigung beim Öffnen/Schließen. Wirkt sich auf die realistische Zykluszeit aus."
    )

# Hydraulikgreifer
elif auswahl_greifer == hydr["greiferart"]:
    gew_greifer_leer = number_standard(
        "Leergewicht des Greifers [kg]",
        hydr["leergewicht_kg"],
        0, 100, 20_000,
        "leergew",
        "Eigengewicht des Greifers ohne Last. Relevant für Bewegungsenergie und mechanische Belastung"
    )
    vol_greifer = number_standard(
        "Greifervolumen [m³]",
        hydr["greifervolumen_m3"],
        0, 0.1, 15,
        "volgreif",
        "Volumen, das der Greifer pro Zyklus aufnehmen kann. Bestimmt die Zyklenanzahl und damit Spielzeit/Energie."
    )

    # Auswahl, ob Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingegeben werden soll
    auswahl_parameter = st.radio("Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingeben?", 
             ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"], 0, key="radio_greifer_oeffnen_schliessen",
             help="Wählen Sie, ob Sie Zeiten direkt angeben oder aus Geschwindigkeit/Beschleunigung ableiten möchten.")
    
    if auswahl_parameter not in ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"]:
        auswahl_parameter = "Schließ/Öffnungszeit"  # Standardwert setzen, falls ungültige Auswahl getroffen wird

    if auswahl_parameter == "Schließ/Öffnungszeit":
        oeffnungszeit_greifen = number_standard(
            "Öffnungszeit [s]",
            hydr["oeffnungszeit_s"],
            0, 1, 30,
            "oeffnzeit",
            "Zeit für das vollständige Öffnen des Greifers. Bestimmt die Zykluszeit und damit den Energiebedarf."
        )
        schliesszeit_greifen = number_standard(
            "Schließzeit [s]",
            hydr["schliesszeit_s"],
            0, 1, 30,
            "schliesszeit",
            "Zeit für das vollständige Schließen des Greifers. Bestimmt die Zykluszeit und damit den Energiebedarf."
        )

    if auswahl_parameter == "Geschwindigkeit/Beschleunigung":
        ges_greifen = number_standard(
            "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
            hydr["greifgeschwindigkeit_m_min"],
            0, 1, 200,
            "gesgreif",
            "Mittlere Öffnungs-/Schließgeschwindigkeit des Greifers. Beeinflusst die Zeit pro Zyklus."
        )
        bes_greifen = number_standard(
            "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
            hydr["greifbeschleunigung_m_s2"],
            0, 0.1, 10,
            "besgreif",
            "Beschleunigung beim Öffnen/Schließen. Wirkt sich auf die realistische Zykluszeit aus."
        )
    
    p_hydr_motor = number_standard(
        "Motorleistung [kW]",
        hydr["motorleistung_kw"],
        0, 1, 250,
        "motorleist",
        "Elektrische Leistung des Hydraulikmotors/Aggregats. Grundlage für die Energieabschätzung."
    )
    n_hydr_motor = number_standard(
        "Wirkungsgrad Hydraulik",
        hydr["wirkungsgrad"],
        0, 0.01, 1,
        "wirkhyrd",
        "Gesamtwirkungsgrad (0-1) des hydraulischen Systems. Berücksichtigt Verluste im Aggregat."
    )
    volumenstrom = number_standard(
        "Volumenstrom [l/min]",
        hydr["volumenstrom_l_min"],
        0, 1, 150,
        "volstr",
        "Förderstrom der Hydraulikpumpe. Beeinflusst die erreichbare Geschwindigkeit und Leistung."
    )
    betriebsdruck = number_standard(
        "Betriebsdruck [bar]",
        hydr["betriebsdruck_bar"],
        0, 1, 300,
        "betdruck",
        "Typischer Arbeitsdruck im Hydrauliksystem. Grundlage für Leistungs-/Energieabschätzung."
    )

button = st.button("Speichern", "speichern_greifer")

if button:
    greifer_state.update(
        # alles in den Session-State speichern, damit es auf den folgenden Seiten verfügbar ist
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
    st.session_state["greifer_saved"] = True # Flag setzen, dass diese Seite gespeichert wurde

# Feedback und Weiterleitung zur nächsten Seite, wenn gespeichert wurde
success_feedback("greifer", "krananlage")