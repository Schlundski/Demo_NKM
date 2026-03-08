### Seite zur Eingabe der mechanischen Daten der Krananlage. Berechnung der Motorleistungen für Hubwerk, Katze und Kranfahrwerk. Alle Werte werden im Session State unter "ist_anlage" -> "kran_mechanik" gespeichert.
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
# Eigene Module mit Funktionen
from ui.components import number_standard
from core.computing import mechleistunghubwerk, mechleistungkatzfahrt, kranfahrt, spielzeitenberechnung
from common.page_init import page_init
from common.flow import success_feedback
# Standardwerte
from config.standards import hubw, katze, kran

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Krananlage", "🏗️", "centered")

# Eingaben bei erstem Seitenaufruf ausklappen
for key in ("expander_hubwerk_open", "expander_katze_open", "expander_kran_open"):
    st.session_state.setdefault(key, True)

## Container für diese Seite im Session State erstellen, sofern noch nicht vorhanden
ist_state = st.session_state.setdefault("ist_anlage", {})
kran_state = ist_state.setdefault("kran_mechanik", {})
greifer_state = ist_state.setdefault("greifer", {})
anlage_state = ist_state.setdefault("anlage", {})
hub_state = kran_state.setdefault("hubwerk", {})
katze_state = kran_state.setdefault("katze", {})
kranfahr_state = kran_state.setdefault("kranfahrwerk", {})

## UI-Inhalte der Krananlagenseite
st.title("🏗️ Mechanische Krandaten")
st.info("Auf dieser Seite erfassen Sie die mechanischen Kenndaten der Kranbewegungen (Hubwerk, Katze und Kranfahrwerk).\n\n"
        "Die Angaben werden genutzt, um Spielzeiten und Leistungsbedarfe abzuschätzen und fließen in die Energie-, Kosten- und CO₂-Auswertung ein.")

# Hubwerk
with st.expander("Hubwerk", expanded = st.session_state["expander_hubwerk_open"]):
    seilgewicht_kg = number_standard(
        "Seilgewicht [kg]", 
        hubw["seilgewicht_kg"], 
        hub_state.get("seilgewicht_kg", hubw["seilgewicht_kg"]),
        0, 1, 500, 
        "seilgew", 
        "Eigengewicht der Hubseile. Beeinflusst die zu bewegende Masse und damit die erforderliche Motorleistung des Hubwerks."
    )
    hub_geschwindigkeit_m_min = number_standard(
        "Hubgeschwindigkeit [m/min]",
        hubw["geschwindigkeit_m_min"],
        hub_state.get("hub_geschwindigkeit_m_pro_min", hubw["geschwindigkeit_m_min"]),
        0,
        1,
        100,
        "hubgeschw",
        "Typische Hubgeschwindigkeit beim Heben oder Senken. Bestimmt zusammen mit dem Hubweg die Spielzeit und den Leistungsbedarf."
    )
    hub_beschleunigung_m_s2 = number_standard(
        "Hubbeschleunigung [m/s²]",
        hubw["beschleunigung_m_s2"],
        hub_state.get("hub_beschleunigung_m_pro_s2", hubw["beschleunigung_m_s2"]),
        0,
        0.01,
        5,
        "hubbeschl",
        "Beschleunigung des Hubvorgangs. Beeinflusst die Beschleunigungszeit und damit die erforderliche Spitzenleistung."
    )
    anzahl_motoren_hub = number_standard(
        "Anzahl Motoren Hubwerk",
        hubw["anzahl_motoren"],
        hub_state.get("anzahl_motoren", hubw["anzahl_motoren"]),
        1,
        1,
        10,
        "anzmotor_hub",
        "Anzahl der Motoren, welche die Hubarbeit gemeinsam leisten. Beeinflusst die auf einen Motor entfallende Leistung.",
        0
    )
    wirkungsgrad_getr_stufe_hub = number_standard(
        "Wirkungsgrad Getriebestufe Hubwerk",
        hubw["wirkungsgrad_getr_stufe"],
        hub_state.get("wirkungsgrad_getriebe", hubw["wirkungsgrad_getr_stufe"]),
        0,
        0.01,
        1,
        "wirkgetr_hub",
        "Wirkungsgrad einer einzelnen Getriebestufe im Hubwerk. Geht in die Gesamtwirkungsgradberechnung ein."
    )
    wirkungsgrad_seiltrieb = number_standard(
        "Wirkungsgrad Seiltrieb",
        hubw["wirkungsgrad_seiltrieb"],
        hub_state.get("wirkungsgrad_seiltrieb", hubw["wirkungsgrad_seiltrieb"]),
        0,
        0.01,
        1,
        "wirkseil",
        "Wirkungsgrad des Seiltriebsystems. Berücksichtigt mechanische Verluste im Hubmechanismus."
    )
    getriebestufen_hub = number_standard(
        "Getriebestufen Hubwerk",
        hubw["getriebestufen"],
        hub_state.get("getriebestufen", hubw["getriebestufen"]),
        1,
        1,
        10,
        "getrstuf_hub",
        "Anzahl der Getriebestufen im Hubwerk. Beeinflusst den Gesamtwirkungsgrad des Antriebsstrangs.",
        0
    )

    # Berechnung der Beschleunigungszeit für die Hubbewegung, um die Spitzenleistung abschätzen zu können
    beschleunigungszeit_hub = spielzeitenberechnung(
          hub_geschwindigkeit_m_min,
          hub_beschleunigung_m_s2,
          0
    )["beschleunigungszeit"]

    # Anzeigen des Ausgewählten Motors
    motor_hub = mechleistunghubwerk(
            gewicht_seile=              seilgewicht_kg,
            gewicht_greifer_leer=       greifer_state.get("leergewicht_kg", 0),
            greifer_volumen=            greifer_state.get("volumen_m3", 0),
            muell_dichte=               anlage_state.get("muell_dichte_beschickung_kg_pro_m3", 0),
            geschwindigkeit_mmin=       hub_geschwindigkeit_m_min,
            beschleunigung_zeit=        beschleunigungszeit_hub,
            wirkungsgrad_seiltrieb=     wirkungsgrad_seiltrieb,
            wirkungsgrad_getriebestufe= wirkungsgrad_getr_stufe_hub,
            getriebestufen=             getriebestufen_hub,
            motor_anzahl=               anzahl_motoren_hub,
            belastungsfaktor=           1.55
            )["motorauswahl"]
    
    st.info(f"Intern berechnete Motorleistung für das Hubwerk zur Orientierung: **{motor_hub:.2f} kW**")

    wirkungsgrad_motor_hub = number_standard("Wirkungsgrad des Hubmotors", 
                                             hubw["wirkungsgrad_motor"], 
                                             hub_state.get("wirkungsgrad_motor_hub", hubw["wirkungsgrad_motor"]),
                                             0, 0.01, 1, 
                                             "wrkgd_mtr_hb", 
                                             "Wirkungsgrad des eingesetzten Hubmotors. Wird zur Berechnung des elektrischen Leistungsbedarfs verwendet.")

    # #Button zum Einklappen des Expanders
    # button_hub_zuklappen = st.button(
    #     "Hubwerk Minimieren", "hubwerk_zuklappen"
    # )
    # if button_hub_zuklappen:
    #       st.session_state["expander_hubwerk_open"] = False
    #       st.rerun()

# Katze
with st.expander("Katze", expanded = st.session_state["expander_katze_open"]):
    gewicht_katze_kg = number_standard(
        "Gewicht der Katze [kg]",
        katze["gewicht_kg"],
        katze_state.get("gewicht_kg", katze["gewicht_kg"]),
        0,
        1,
        100000,
        "gewkatze",
        "Eigengewicht der Katze ohne Last. Beeinflusst die zu bewegende Gesamtmasse der Katzfahrt."
    )
    geschwindigkeit_katze_m_min = number_standard(
        "Fahrgeschwindigkeit Katze [m/min]",
        katze["geschwindigkeit_m_min"],
        katze_state.get("geschwindigkeit_m_pro_min", katze["geschwindigkeit_m_min"]),
        0,
        1,
        100,
        "geschwkatze",
        "Typische Fahrgeschwindigkeit der Katze. Bestimmt die Spielzeit und den Leistungsbedarf der Bewegung."
    )
    beschleunigung_katze_m_s2 = number_standard(
        "Beschleunigung Katze [m/s²]",
        katze["beschleunigung_m_s2"],
        katze_state.get("beschleunigung_m_pro_s2", katze["beschleunigung_m_s2"]),
        0,
        0.01,
        5,
        "beschlkatze",
        "Beschleunigung beim Anfahren der Katze. Beeinflusst die erforderliche Motorleistung.",
    )
    anzahl_motoren_katze = number_standard(
        "Anzahl Motoren Katze",
        katze["anzahl_motoren"],
        katze_state.get("anzahl_motoren", katze["anzahl_motoren"]),
        1,
        1,
        10,
        "anzmotkatze",
        "Anzahl der Motoren, welche die Katzfahrt antreiben. Beeinflusst die Leistungsaufteilung.",
        0
    )
    wirkungsgrad_getr_stufe_katze = number_standard(
        "Wirkungsgrad Getriebestufe Katze",
        katze["wirkungsgrad_getr_stufe"],
        katze_state.get("wirkungsgrad_getriebe", katze["wirkungsgrad_getr_stufe"]),
        0,
        0.001,
        1,
        "wirkgetrkatze",
        "Wirkungsgrad einer einzelnen Getriebestufe der Katzfahrt. Geht in die Gesamtwirkungsgradberechnung ein."
    )
    getriebestufen_katze = number_standard(
        "Getriebestufen Katze",
        katze["getriebestufen"],
        katze_state.get("getriebestufen", katze["getriebestufen"]),
        1,
        1,
        10,
        "getrstufkatze",
        "Anzahl der Getriebestufen im Katzfahrwerk. Beeinflusst den Gesamtwirkungsgrad des Antriebs.",
        0
    )
    fahrwiderstand_katze_kg_t = number_standard(
        "Fahrwiderstand Katze [kg/t]",
        katze["fahrwiderstand_kg_t"],
        katze_state.get("fahrwiderstand_kg_pro_t", katze["fahrwiderstand_kg_t"]),
        0,
        0.1,
        100,
        "fahrwidkatze",
        "Spezifischer Fahrwiderstand der Katzfahrt. Berücksichtigt Roll- und Reibungsverluste."
    )

    # Motor berechnen und anzeigen. User kann noch Werte ändern
    motor_katze = mechleistungkatzfahrt(
          gewicht_seile=                seilgewicht_kg,
          gewicht_greifer_leer=         greifer_state.get("leergewicht_kg", 0),
          greifer_volumen=              greifer_state.get("volumen_m3", 0),
          muell_dichte=                 anlage_state.get("muell_dichte_beschickung_kg_pro_m3", 0),
          gewicht_katze=                gewicht_katze_kg,
          geschwindigkeit_mmin=         geschwindigkeit_katze_m_min,
          fahrwerkwiderstand=           fahrwiderstand_katze_kg_t,
          getriebestufen=               int(getriebestufen_katze),
          wirkungsgrad_getriebestufe=   wirkungsgrad_getr_stufe_katze,
          motorzahl=                    int(anzahl_motoren_katze),
          beschleunigungszeit=          int(geschwindigkeit_katze_m_min / 60.0 / beschleunigung_katze_m_s2),
          belastungsfaktor=             1.55
        )["motorauswahl"]
    st.info(f"Intern berechnete Motorleistung für die Katze zur Orientierung: **{motor_katze:.2f} kW**")

    wirkungsgrad_motor_katze = number_standard("Wirkungsgrad des Katzmotors", 
                                            katze["wirkungsgrad_motor"], 
                                            katze_state.get("wirkungsgrad_motor_katze", katze["wirkungsgrad_motor"]),
                                            0, 0.01, 1,
                                            "wirkmotorkatze")

    # #Button zum Einklappen des Expanders
    # button_katze_zuklappen = st.button(
    #     "Katze Minimieren", "katze_zuklappen"
    # )
    # if button_katze_zuklappen:
    #       st.session_state["expander_katze_open"] = False
    #       st.rerun()

# Kran
with st.expander("Kranfahrwerk", expanded = st.session_state["expander_kran_open"]):
    gewicht_kran_kg = number_standard(
        "Kranfahrwerk Gewicht [kg]",
        kran["gewicht_kg"],
        kranfahr_state.get("gewicht_kg", kran["gewicht_kg"]),
        0,
        1,
        500000,
        "gewkran",
        "Eigengewicht des Kranfahrwerks ohne Last. Beeinflusst die zu bewegende Gesamtmasse."
    )
    geschwindigkeit_kran_m_min = number_standard(
        "Kranfahrgeschwindigkeit [m/min]",
        kran["geschwindigkeit_m_min"],
        kranfahr_state.get("geschwindigkeit_m_pro_min", kran["geschwindigkeit_m_min"]),
        0,
        1,
        100,
        "geschwkran",
        "Typische Fahrgeschwindigkeit des Krans. Bestimmt Spielzeit und Leistungsbedarf."
    )
    beschleunigung_kran_m_s2 = number_standard(
        "Kranfahrbeschleunigung [m/s²]",
        kran["beschleunigung_m_s2"],
        kranfahr_state.get("beschleunigung_m_pro_s2", kran["beschleunigung_m_s2"]),
        0,
        0.1,
        5,
        "beschlkran",
        "Beschleunigung beim Anfahren des Krans. Beeinflusst die erforderliche Motorleistung."
    )
    anzahl_motoren_kran = number_standard(
        "Anzahl Motoren Kran",
        kran["anzahl_motoren"],
        kranfahr_state.get("anzahl_motoren", kran["anzahl_motoren"]),
        1,
        1,
        10,
        "anzmotkran",
        "Anzahl der Motoren des Kranfahrwerks. Beeinflusst die Leistungsaufteilung.",
        0
    )
    wirkungsgrad_getr_stufe_kran = number_standard(
        "Wirkungsgrad Getriebestufe Kran",
        kran["wirkungsgrad_getr_stufe"],
        kranfahr_state.get("wirkungsgrad_getriebe", kran["wirkungsgrad_getr_stufe"]),
        0,
        0.01,
        1,
        "wirkgetrkran",
        "Wirkungsgrad einer einzelnen Getriebestufe im Kranfahrwerk."
    )
    wirkungsgrad_vorgelege = number_standard(
        "Wirkungsgrad Vorgelege",
        kran["wirkungsgrad_vorgelege"],
        kranfahr_state.get("wirkungsgrad_vorgelege", kran["wirkungsgrad_vorgelege"]),
        0,
        0.01,
        1,
        "wirkvorgelege",
        "Wirkungsgrad des Vorgeleges. Berücksichtigt zusätzliche mechanische Verluste."
    )
    getriebestufen_kran = number_standard(
        "Anzahl Getriebestufen Kran",
        kran["getriebestufen"],
        kranfahr_state.get("getriebestufen", kran["getriebestufen"]),
        1,
        1,
        10,
        "getrstufkran",
        "Anzahl der Getriebestufen im Kranfahrwerk. Beeinflusst den Gesamtwirkungsgrad.",
        0
    )
    fahrwiderstand_kran_kg_t = number_standard(
        "Fahrwiderstand Kran[kg/t]",
        kran["fahrwiderstand_kg_t"],
        kranfahr_state.get("fahrwiderstand_kg_pro_t", kran["fahrwiderstand_kg_t"]),
        0,
        0.1,
        100,
        "fahrwidkran",
        "Spezifischer Fahrwiderstand der Kranfahrt. Berücksichtigt Roll- und Reibungsverluste."
    )

    # Motor berechnen und anzeigen. User kann noch die Werte verändern
    motor_kran = kranfahrt(
        gewicht_greifer_leer=       greifer_state.get("leergewicht_kg", 0),
        greifer_volumen=            greifer_state.get("volumen_m3", 0),
        muell_dichte=               anlage_state.get("muell_dichte_beschickung_kg_pro_m3", 0),
        gewicht_katze=              gewicht_katze_kg,
        gewicht_kran=               gewicht_kran_kg,
        gewicht_seile=              seilgewicht_kg,
        geschwindigkeit_mmin=       geschwindigkeit_kran_m_min,
        fahrwiderstand=             fahrwiderstand_kran_kg_t,
        motoranzahl=                anzahl_motoren_kran,
        wirkungsgrad_getriebestufe= wirkungsgrad_getr_stufe_kran,
        getriebestufen=             getriebestufen_kran,
        beschleunigungszeit=        int(geschwindigkeit_kran_m_min / 60.0 / beschleunigung_kran_m_s2),
        belastungsfaktor=           1.55
    )["motorauswahl"]

    st.info(f"Intern berechnete Motorleistung für das Kranfahrwerk zur Orientierung: **{motor_kran:.2f} kW**")

    wirkungsgrad_motor_kran = number_standard("Wirkungsgrad des Kranmotors", 
        kran["wirkungsgrad_motor"], 
        kranfahr_state.get("wirkungsgrad_motor_kran", kran["wirkungsgrad_motor"]),
        0, 0.01, 1, 
        "wrkgd_mtr_krn", 
        "Wirkungsgrad des eingesetzten Kranmotors. Wird zur Berechnung des elektrischen Leistungsbedarfs verwendet.")

    # #Button zum Einklappen des Expanders
    # button_kran_zuklappen = st.button(
    #     "Kran Minimieren", "kran_zuklappen"
    # )
    # if button_kran_zuklappen:
    #       st.session_state["expander_kran_open"] = False
    #       st.rerun()

success_feedback("krananlage", "wege")

if st.session_state.get("speichern_krananlage"):
# Alle eingegebenen Werte in den Session State speichern, damit sie auf den folgenden Seiten verfügbar sind
    kran_state.update(
        {
            "hubwerk": {
                "seilgewicht_kg": seilgewicht_kg,
                "hub_geschwindigkeit_m_pro_min": hub_geschwindigkeit_m_min,
                "hub_beschleunigung_m_pro_s2": hub_beschleunigung_m_s2,
                "anzahl_motoren": anzahl_motoren_hub,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_hub,
                "wirkungsgrad_seiltrieb": wirkungsgrad_seiltrieb,
                "getriebestufen": getriebestufen_hub,
                "wirkungsgrad_motor_hub": wirkungsgrad_motor_hub
            },
            "katze": {
                "gewicht_kg": gewicht_katze_kg,
                "geschwindigkeit_m_pro_min": geschwindigkeit_katze_m_min,
                "beschleunigung_m_pro_s2": beschleunigung_katze_m_s2,
                "anzahl_motoren": anzahl_motoren_katze,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_katze,
                "getriebestufen": getriebestufen_katze,
                "fahrwiderstand_kg_pro_t": fahrwiderstand_katze_kg_t,
                "wirkungsgrad_motor_katze": wirkungsgrad_motor_katze
            },
            "kranfahrwerk": {
                "gewicht_kg": gewicht_kran_kg,
                "geschwindigkeit_m_pro_min": geschwindigkeit_kran_m_min,
                "beschleunigung_m_pro_s2": beschleunigung_kran_m_s2,
                "anzahl_motoren": anzahl_motoren_kran,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_kran,
                "wirkungsgrad_vorgelege": wirkungsgrad_vorgelege,
                "getriebestufen": getriebestufen_kran,
                "fahrwiderstand_kg_pro_t": fahrwiderstand_kran_kg_t,
                "wirkungsgrad_motor_kran": wirkungsgrad_motor_kran
            },
        }
    )
    st.session_state["krananlage_saved"] = True # Flag setzen, dass diese Seite gespeichert wurde
    st.rerun() # Rerun, damit der Weiter-Button erscheint
    
