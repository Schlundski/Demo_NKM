# Bewegungseingaben
import streamlit as st
from ui.components import number_standard
import config.standards as std
import time
from auth import check_login
from core.computing import mechleistunghubwerk, mechleistungkatzfahrt, kranfahrt, spielzeitenberechnung
from ui.theme import set_background_auto_theme

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)

st.set_page_config(layout = "centered")

check_login()

st.title("Mechanische Krandaten")

# Eingaben bei Seitenaufruf ausklappen
if "expander_hubwerk_open" not in st.session_state:
        st.session_state.expander_hubwerk_open = True
if "expander_katze_open" not in st.session_state:
        st.session_state.expander_katze_open = True
if "expander_kran_open" not in st.session_state:
        st.session_state.expander_kran_open = True

# Container im Session State
ist_state = st.session_state["ist_anlage"]
kran_state = ist_state.setdefault("kran_mechanik", {})

# Hubwerk
with st.expander("Hubwerk", expanded = st.session_state.expander_hubwerk_open, width="stretch"):
    seilgewicht = number_standard(
        "Seilgewicht [kg]", std.hubw["Seilgewicht"], 0, 1, 500, "seilgew"
    )
    hub_geschwindigkeit = number_standard(
        "Hubgeschwindigkeit [m/min]",
        std.hubw["Geschwindigkeit"],
        0,
        1,
        100,
        "hubgeschw",
    )
    hub_beschleunigung = number_standard(
        "Hubbeschleunigung [m/s²]",
        std.hubw["Beschleunigung"],
        0,
        0.01,
        5,
        "hubbeschl",
    )
    motordrehzahl_hub = number_standard(
        "Motordrehzahl Hubwerk [1/min]",
        std.hubw["Motordrehzahl"],
        0,
        1,
        5000,
        "motdreh_hub",
    )
    massentraegheit_hub = number_standard(
        "Massenträgheit Hubwerk [kg·m²]",
        std.hubw["Massentraegheit"],
        0,
        0.001,
        100,
        "massentr_hub",
        nachkommastellen=3
    )
    anzahl_motoren_hub = number_standard(
        "Anzahl Motoren Hubwerk",
        std.hubw["AnzahlMotoren"],
        0,
        1,
        10,
        "anzmotor_hub",
        "Anzahl der Motoren, welche die Hubarbeit teilen",
        0
    )
    wirkungsgrad_getr_stufe_hub = number_standard(
        "Wirkungsgrad Getriebestufe Hubwerk",
        std.hubw["WirkungsgradGetrStufe"],
        0,
        0.01,
        1,
        "wirkgetr_hub",
    )
    wirkungsgrad_seiltrieb = number_standard(
        "Wirkungsgrad Seiltrieb",
        std.hubw["WirkungsgradSeiltrieb"],
        0,
        0.01,
        1,
        "wirkseil",
    )
    getriebestufen_hub = number_standard(
        "Getriebestufen Hubwerk",
        std.hubw["Getriebestufen"],
        0,
        1,
        10,
        "getrstuf_hub",
        "Anzahl der Getriebestufen des Hubwerkes",
        0
    )

    beschleunigung_zeit_hub = spielzeitenberechnung(
          hub_geschwindigkeit,
          hub_beschleunigung,
          0
    )["Beschleunigungszeit"]

    # Anzeigen des Ausgewählten Motors
    motor_hub = mechleistunghubwerk(
            gewicht_seile = seilgewicht,
           gewicht_greifer_leer = ist_state.get("greifer", {}).get("leergewicht_kg"),
           greifer_volumen = ist_state.get("greifer", {}).get("volumen_m3"),
           muell_dichte = ist_state.get("anlage", {}).get("müll_dichte_beschickung_kg_pro_m3"),
           geschwindigkeit_mmin = hub_geschwindigkeit,
           beschleunigung_m_ss = beschleunigung_zeit_hub,
           wirkungsgrad_seiltrieb = wirkungsgrad_seiltrieb,
           wirkungsgrad_getriebestufe = wirkungsgrad_getr_stufe_hub,
           drehzahl = motordrehzahl_hub,
           getriebestufen = getriebestufen_hub,
           motor_anzahl = anzahl_motoren_hub,
           massentraegheit= massentraegheit_hub
    )["Motorauswahl"]
    number_standard("Von uns gewählte Hubmotorleistung [kW]", 
                    motor_hub, 
                    0, 1, 200, 
                    "mtr_swhl_hb", 
                    "Der angezeigte Motor wird durch die vorherigen Eingaben intern berechnet"
                    )
    wirkungsgrad_motor_hub = number_standard("Wirkungsgrad des Hubmotors", 
                                             std.hubw["WirkungsgradMotor"], 
                                             0, 0.01, 1, 
                                             "wrkgd_mtr_hb", 
                                             "Der Standardwert des Wirkungsgrades beruht auf einem Erfahrungswert.")

    #Button zum Einklappen des Expanders
    button_hub_zuklappen = st.button(
        "Hubwerk Minimieren"
    )
    if button_hub_zuklappen:
          st.session_state.expander_hubwerk_open = False
          st.rerun()

# Katze
with st.expander("Katze", expanded = st.session_state.expander_katze_open, width="stretch"):
    gewicht_katze = number_standard(
        "Gewicht der Katze [kg]",
        std.katze["Gewicht"],
        0,
        1,
        100000,
        "gewkatze",
    )
    geschwindigkeit_katze = number_standard(
        "Fahrgeschwindigkeit Katze [m/min]",
        std.katze["Geschwindigkeit"],
        0,
        1,
        100,
        "geschwkatze",
    )
    beschleunigung_katze = number_standard(
        "Beschleunigung Katze [m/s²]",
        std.katze["Beschleunigung"],
        0,
        0.01,
        5,
        "beschlkatze",
    )
    motordrehzahl_katze = number_standard(
        "Motordrehzahl Katze [1/min]",
        std.katze["Motordrehzahl"],
        0,
        1,
        5000,
        "motdrehkatze",
    )
    massentraegheit_katze = number_standard(
        "Massenträgheit Katze [kg·m²]",
        std.katze["Massentraegheit"],
        0,
        0.001,
        100,
        "massentrkatze",
        nachkommastellen=3
    )
    anzahl_motoren_katze = number_standard(
        "Anzahl Motoren Katze",
        std.katze["AnzahlMotoren"],
        0,
        1,
        10,
        "anzmotkatze",
        "Anzahl der Motoren, welche die Katzfahrt teilen",
        0
    )
    wirkungsgrad_getr_stufe_katze = number_standard(
        "Wirkungsgrad Getriebestufe Katze",
        std.katze["WirkungsgradGetrStufe"],
        0,
        0.001,
        1,
        "wirkgetrkatze",
    )
    getriebestufen_katze = number_standard(
        "Getriebestufen Katze",
        std.katze["Getriebestufen"],
        0,
        1,
        10,
        "getrstufkatze",
        "Anzahl der Getriebestufen des Katzfahrwerkes",
        0
    )
    fahrwiderstand_katze = number_standard(
        "Fahrwiderstand Katze [kg/t]",
        std.katze["Fahrwiderstand"],
        0,
        0.1,
        100,
        "fahrwidkatze",
    )

    # Motor berechnen und anzeigen. User kann noch Werte ändern
    mot_katze=mechleistungkatzfahrt(
          gewicht_seile=seilgewicht,
          gewicht_greifer_leer=ist_state.get("greifer", {}).get("leergewicht_kg"),
          greifer_volumen=ist_state["greifer"]["volumen_m3"],
          muell_dichte=ist_state.get("anlage", {}).get("müll_dichte_beschickung_kg_pro_m3"),
          gewicht_katze=gewicht_katze,
          geschwindigkeit_mmin=geschwindigkeit_katze,
          beschleunigung_m_ss=geschwindigkeit_katze/60/beschleunigung_katze,
          drehzahl=int(motordrehzahl_katze),
          fahrwerkwiderstand=fahrwiderstand_katze,
          getriebestufen=int(getriebestufen_katze),
          wirkungsgrad_getriebestufe=wirkungsgrad_getr_stufe_katze,
          massentraegheit=massentraegheit_katze,
        )["Motorauswahl"]
    number_standard("Von uns gewählte Katzmotorleistung [kW]", 
                    mot_katze, 
                    0, 1, 200, 
                    "minmotorkatze"
                    )
    wirkungsgrad_motor_katze = number_standard("Wirkungsgrad des Katzmotors", 
                                               std.katze["WirkungsgradMotor"], 
                                               0, 0.01, 1,
                                               "wirkmotorkatze")

    #Button zum Einklappen des Expanders
    button_katze_zuklappen = st.button(
        "Katze Minimieren"
    )
    if button_katze_zuklappen:
          st.session_state.expander_katze_open = False
          st.rerun()

# Kran
with st.expander("Kranfahrwerk", expanded = st.session_state.expander_kran_open, width="stretch"):
    gewicht_kran = number_standard(
        "Kranfahrwerk Gewicht [kg]",
        std.kran["Gewicht"],
        0,
        1,
        500000,
        "gewkran",
    )
    geschwindigkeit_kran = number_standard(
        "Kranfahrgeschwindigkeit [m/min]",
        std.kran["Geschwindigkeit"],
        0,
        1,
        100,
        "geschwkran",
    )
    beschleunigung_kran = number_standard(
        "Kranfahrbeschleunigung [m/s²]",
        std.kran["Beschleunigung"],
        0,
        0.1,
        5,
        "beschlkran",
    )
    motordrehzahl_kran = number_standard(
        "Motordrehzahl Kran [1/min]",
        std.kran["Motordrehzahl"],
        0,
        1,
        5000,
        "motdrehkran",
    )
    massentraegheit_kran = number_standard(
        "Massenträgheit Kran [kg·m²]",
        std.kran["Massentraegheit"],
        0,
        0.001,
        100,
        "massentrkran",
        nachkommastellen=3
    )
    anzahl_motoren_kran = number_standard(
        "Anzahl Motoren Kran",
        std.kran["AnzahlMotoren"],
        0,
        1,
        10,
        "anzmotkran",
        "Anzahl der Motoren, welche die Kranfahrt teilen",
        0
    )
    wirkungsgrad_getr_stufe_kran = number_standard(
        "Wirkungsgrad Getriebestufe Kran",
        std.kran["WirkungsgradGetrStufe"],
        0,
        0.01,
        1,
        "wirkgetrkran",
    )
    wirkungsgrad_vorgelege = number_standard(
        "Wirkungsgrad Vorgelege",
        std.kran["WirkungsgradVorgelege"],
        0,
        0.01,
        1,
        "wirkvorgelege",
    )
    getriebestufen_kran = number_standard(
        "Getriebestufen Kran",
        std.kran["Getriebestufen"],
        0,
        1,
        10,
        "getrstufkran",
    )
    fahrwiderstand_kran = number_standard(
        "Fahrwiderstand Kran[kg/t]",
        std.kran["Fahrwiderstand"],
        0,
        0.1,
        100,
        "fahrwidkran",
    )

    # Motor berechnen und anzeigen. User kann noch die Werte verändern
    motor_kran = kranfahrt(
        gewicht_greifer_leer = ist_state.get("greifer", {}).get("leergewicht_kg"),
        greifer_volumen = ist_state.get("greifer", {}).get("volumen_m3"),
        muell_dichte = ist_state.get("anlage", {}).get("müll_dichte_beschickung_kg_pro_m3"),
        gewicht_katze = gewicht_katze,
        gewicht_kran = gewicht_kran,
        gewicht_seile = seilgewicht,
        beschleunigung_mss = beschleunigung_kran,
        geschwindigkeit_mmin = geschwindigkeit_kran,
        drehzahl = motordrehzahl_kran,
        massentraegheit = massentraegheit_kran,
        fahrwiderstand = fahrwiderstand_kran,
        motoranzahl = anzahl_motoren_kran,
        wirkungsgrad_getriebestufe = wirkungsgrad_getr_stufe_kran,
        getriebestufen = getriebestufen_kran
    )["Motorauswahl"]
    number_standard("Von uns gewählte Kranmotorleistung [kW]", 
                    motor_kran, 
                    0, 1, 200, 
                    "mtr_swhl_krn", 
                    "Der angezeigte Motor wird durch die vorherigen Eingaben intern berechnet"
                    )
    wirkungsgrad_motor_kran = number_standard("Wirkungsgrad des Kranmotors", 
                                              std.kran["WirkungsgradMotor"], 
                                              0, 0.01, 1, 
                                              "wrkgd_mtr_krn", 
                                              "Der Standardwert des Wirkungsgrades beruht auf einem Erfahrungswert.")

    #Button zum Einklappen des Expanders
    button_kran_zuklappen = st.button(
        "Kran Minimieren"
    )
    if button_kran_zuklappen:
          st.session_state.expander_kran_open = False
          st.rerun()

button = st.button("Speichern und weiter")

if button:
    # Expander wieder Ausklappen
    st.session_state.expander_hubwerk_open = True
    st.session_state.expander_katze_open = True
    st.session_state.expander_kran_open = True
    
    # Eingabewerte im session_state abspeichern
    kran_state.update(
        {
            "hubwerk": {
                "seilgewicht_kg": seilgewicht,
                "hub_geschwindigkeit_m_pro_min": hub_geschwindigkeit,
                "hub_beschleunigung_m_pro_s2": hub_beschleunigung,
                "motordrehzahl_1_pro_min": motordrehzahl_hub,
                "massenträgheit_kgm2": massentraegheit_hub,
                "anzahl_motoren": anzahl_motoren_hub,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_hub,
                "wirkungsgrad_seiltrieb": wirkungsgrad_seiltrieb,
                "getriebestufen": getriebestufen_hub,
                "wirkungsgrad_motor_hub": wirkungsgrad_motor_hub
            },
            "katze": {
                "gewicht_kg": gewicht_katze,
                "geschwindigkeit_m_pro_min": geschwindigkeit_katze,
                "beschleunigung_m_pro_s2": beschleunigung_katze,
                "motordrehzahl_1_pro_min": motordrehzahl_katze,
                "massenträgheit_kgm2": massentraegheit_katze,
                "anzahl_motoren": anzahl_motoren_katze,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_katze,
                "getriebestufen": getriebestufen_katze,
                "fahrwiderstand_kg_pro_t": fahrwiderstand_katze,
                "wirkungsgrad_motor_katze": wirkungsgrad_motor_katze
            },
            "kranfahrwerk": {
                "gewicht_kg": gewicht_kran,
                "geschwindigkeit_m_pro_min": geschwindigkeit_kran,
                "beschleunigung_m_pro_s2": beschleunigung_kran,
                "motordrehzahl_1_pro_min": motordrehzahl_kran,
                "massenträgheit_kgm2": massentraegheit_kran,
                "anzahl_motoren": anzahl_motoren_kran,
                "wirkungsgrad_getriebe": wirkungsgrad_getr_stufe_kran,
                "wirkungsgrad_vorgelege": wirkungsgrad_vorgelege,
                "getriebestufen": getriebestufen_kran,
                "fahrwiderstand_kg_pro_t": fahrwiderstand_kran,
                "wirkungsgrad_motor_kran": wirkungsgrad_motor_kran
            },
        }
    )

    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Wege.py")
