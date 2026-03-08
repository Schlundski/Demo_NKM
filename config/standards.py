STANDARDWERTE = {

    "anlage": {
        "anzahl_kraene": 2,                       # stk
        "anzahl_trichter": 4,                     # stk
        "verbrennung_je_trichter_kg": 21200,      # kg
        "standort": "Deutschland",
    },

    "greifer": {

        "motor-mehrschalengreifer_mrs_greifer_2-12-31667-1": {
            "leergewicht_kg": 3050,
            "motorleistung_kw": 18.8,
            "greifervolumen_m3": 2.75,
            "wirkungsgrad": 0.9,
            "volumenstrom_l_min": 66.0,
            "betriebsdruck_bar": 170,
            "greifgeschwindigkeit_m_min": 100.0,
            "greifbeschleunigung_m_s2": 2.0,
            "greiferart": "Hydraulikgreifer",
            "oeffnungszeit_s": 6,
            "schliesszeit_s": 10.5,
            "anteil_bewegte_masse": 0.15
        },

        "vierseil-mehrschalen_muellgreifer_mrs_greifer_1-26-6315-6316": {
            "leergewicht_kg": 3800,
            "greifervolumen_m3": 4.0,
            "greifgeschwindigkeit_m_min": 100.0,
            "greifbeschleunigung_m_s2": 0.5,
            "greiferart": "Vierseil-Greifer",
            "oeffnungszeit_s": 6,
            "schliesszeit_s": 10.5,
        }
    },

    "muell": {
        "gesamtmenge_kg_pro_jahr": 760_000_000,
        "anliefermenge_kg_pro_stunde": 235_000,
        "anlieferdauer_stunden_pro_tag": 12,
        "dichte_einlagerung_kg_m3": 700,
        "dichte_beschickung_kg_m3": 800
    },

    "geschwindigkeiten": {
        "heben_senken_m_min": 100.0,
        "katzfahrt_m_min": 85.0,
        "kranfahrt_m_min": 85.0,
        "oeffnen_schliessen_m_min": 100.0,
    },

    "beschleunigungen": {
        "heben_senken_m_s2": 0.5,
        "katzfahrt_m_s2": 0.22,
        "kranfahrt_m_s2": 0.22,
        "oeffnen_schliessen_m_s2": 0.5,
    },

    "referenzwege": {
        "heben_senken_m": 25,
        "katzfahrt_m": 10,
        "kranfahrt_einlagern_m": 35,
        "oeffnen_schliessen_m_vierseil": 11,
        "oeffnen_schliessen_m_hydraulik": 2,
        "trichterweg_1_m": 10,
        "trichterweg_2_m": 25,
        "trichterweg_3_m": 40,
        "trichterweg_4_m": 55,
        "trichterweg_5_m": 70,
        "trichterweg_6_m": 85,
        "trichterweg_7_m": 100,
        "trichterweg_8_m": 115,
        "trichterweg_9_m": 130,
        "trichterweg_10_m": 145,
    },

    "hubwerk": {  # werte aus 831022m.010000-8_motorgreifer
        "seilgewicht_kg": 200.0,
        "geschwindigkeit_m_min": 80.0,
        "beschleunigung_m_s2": 0.67,
        "motordrehzahl_1_min": 1488,
        "massentraegheit_kg_m2": 5.3,
        "anzahl_motoren": 1,
        "wirkungsgrad_getr_stufe": 0.98,
        "wirkungsgrad_seiltrieb": 0.99,
        "getriebestufen": 3,
        "wirkungsgrad_motor": 0.967
    },

    "katze": {  # werte aus 831022m.010000-8_motorgreifer
        "gewicht_kg": 12300.0,
        "geschwindigkeit_m_min": 60.0,
        "beschleunigung_m_s2": 0.25,
        "motordrehzahl_1_min": 1456,
        "massentraegheit_kg_m2": 0.008,
        "anzahl_motoren": 2,
        "wirkungsgrad_getr_stufe": 0.98,
        "wirkungsgrad_motor": 0.896,
        "getriebestufen": 2,
        "fahrwiderstand_kg_t": 8.5,
    },

    "kran": {  # werte aus 831022m.010000-8_motorgreifer
        "gewicht_kg": 30200.0,
        "geschwindigkeit_m_min": 80.0,
        "beschleunigung_m_s2": 0.3,
        "motordrehzahl_1_min": 1461,
        "massentraegheit_kg_m2": 0.098,
        "anzahl_motoren": 2,
        "wirkungsgrad_getr_stufe": 0.98,
        "wirkungsgrad_vorgelege": 1.0,
        "getriebestufen": 3,
        "fahrwiderstand_kg_t": 7,
        "wirkungsgrad_motor": 0.904
    },

    "rueckspeisung": {
        "fu_wirkungsgrad_greifer": 0.98,
        "faktor_greifer": 0,
        "fu_wirkungsgrad_hubfahrt": 0.98,
        "faktor_hubfahrt": 0,
        "fu_wirkungsgrad_kranfahrt": 0.98,
        "faktor_kranfahrt": 0,
        "fu_wirkungsgrad_katzfahrt": 0.98,
        "faktor_katzfahrt": 0
    }
}


Motorleistungen = [
    0.06, 0.09, 0.12, 0.18, 0.25, 0.37, 0.55, 0.75,
    1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5,
    22, 30, 37, 45, 55, 75, 90, 110, 132, 160,
    200, 250, 315, 335, 400, 450, 560
]
# daten aus iec 60072-1 table 6 preferred rated output values


# aliase

anlage = STANDARDWERTE["anlage"]
hydr = STANDARDWERTE["greifer"]["motor-mehrschalengreifer_mrs_greifer_2-12-31667-1"]
viers = STANDARDWERTE["greifer"]["vierseil-mehrschalen_muellgreifer_mrs_greifer_1-26-6315-6316"]
hubw = STANDARDWERTE["hubwerk"]
katze = STANDARDWERTE["katze"]
kran = STANDARDWERTE["kran"]
wege = STANDARDWERTE["referenzwege"]
muell = STANDARDWERTE["muell"]
ruecksp = STANDARDWERTE["rueckspeisung"]