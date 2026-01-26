import streamlit as st
from ui.components import number_standard, number_soll, selectbox_soll, plot_ldaten_rdiagramm, rueckspeisung_standard, plot_aufteilung_CO2, plot_slider_global
from auth import check_login
from core.computing import mechleistunghubwerk, kranfahrt, mechleistungkatzfahrt, berechnungen_pro_tag
import pandas as pd
from config.standards import STANDARDWERTE
import config.standards as std
from typing import cast
from ui.theme import set_background_auto_theme

set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)

st.set_page_config(layout = "wide")
check_login()

df_laender = pd.read_csv("tabellen/Stromländerpreise+CO2.csv", sep=';')

ist_state = st.session_state["ist_anlage"]

st.title("📊 Auswertung")

with st.expander("Parameter für Modernisierung", False):
    with st.expander("Allgemeine Anlagendaten", False):
        st.header("Allgemeinen Anlagendaten")
        # Neuen session states container initialisieren
        st.session_state["neu_anlage"] = {}
        st.session_state["neu_anlage"]["anlage"] = {}
        soll_anlage_state = st.session_state["neu_anlage"]["anlage"]
        ist_anlage_state = ist_state["anlage"]
        # Allgemeine Daten
        st.write("# :grey[Allgemeine Daten]")
        soll_anzahl_kraene = number_soll(
            "Anzahl der Kräne",
            ist_anlage_state["anzahl_kraene"],
            1, 1, 10,
            "soll_anzl_kraene",
            "Anzahl der Krane in der Anlage",
            0
        )
        soll_anzahl_trichter = number_soll(
            "Anzahl der Trichter",
            ist_anlage_state["anzahl_trichter"],
            1, 1, 10,
            "soll_anzl_trichter",
            "Anzahl der Trichter zum Beschicken",
            0
        )
        soll_verbrennung_trichter = number_soll(
            "Verbrennung je Trichter [kg]",
            ist_anlage_state["verbrennung_trichter_kg"],
            0, 100, 100_000,
            "soll_vbrng_trichter",
            "Verbrennung pro Trichter in kg"
        )
        # Mülldaten
        st.write("# :grey[Mülldaten]")
        soll_müll_anlieferung_h = number_soll(
            "Durchschnittliche Müllanliefermenge pro Stunde [kg]",
            ist_anlage_state["müll_anlieferung_h_kg"],
            0, 100, 1_000_000,
            "soll_ml_anlfrmg",
        )
        soll_müll_dichte_beschickung = number_soll(
            "Müll Dichte bei Beschickung [kg/m³]",
            ist_anlage_state["müll_dichte_beschickung_kg_pro_m3"],
            0, 100, 2000,
            "soll_ml_dcht_beschickung",
        )
        soll_müll_dichte_anlieferung = number_soll(
            "Müll Dichte bei Einlagerung [kg/m³]",
            ist_anlage_state["müll_dichte_anlieferung_kg_pro_m3"],
            0, 100, 2000,
            "soll_ml_dcht_anlieferung",
        )
        soll_müll_anlieferdauer = number_standard(
            "Müll Anlieferdauer [h/d]",
            ist_anlage_state["müll_anlieferdauer"],
            1, 1, 24,
            "soll_ml_anlieferdr",
            "Durchschnittliche tägliche Anlieferdauer in Stunden",
            0
        )

        # Kosten etc.
        soll_anlage_standort = selectbox_soll(
            titel = "Standort der Anlage",
            ist = ist_anlage_state["anlage_standort"],
            auswahl = df_laender["Land"].tolist(),
            key = "soll_anl_standort",
            helptext = "In welchem Land befindet sich die Anlage?"
        )
        s = cast(pd.Series, df_laender.loc[df_laender["Land"] == soll_anlage_standort, "Preis in c/kWh"]) 
        preis = s.iloc[0] # Länderpreis direkt nach vorheriger Eingabe raussuchen
        soll_energie_kosten = number_soll(
            "Höhe der Tarifenergiekosten des Standortes [c/kWh]",
            preis,
            0,
            0.1,
            200,
            "soll_enrgy_kostn",
            "Die Energiekosten von c/kWh für die Anlage",
        )

    with st.expander("Greiferdaten", False):
        # Neuen session_state container initialisieren
        st.session_state["neu_anlage"]["greifer"] = {}
        soll_greifer_state = st.session_state["neu_anlage"]["greifer"]
        ist_greifer_state = ist_state["greifer"]

        # Radio Buttons erstellen
        soll_greifer_Arten = [std.viers["Greiferart"], std.hydr["Greiferart"]]
        if ist_greifer_state["typ"] == "Vierseil-Greifer": 
            standard_index=0 
        else: 
            standard_index=1
        soll_auswahl = st.radio("Greiferart:", soll_greifer_Arten, key="soll_radio_greifer_Arten", index=standard_index)

        # Vierseil-Greifer
        if soll_auswahl == std.viers["Greiferart"]:
            soll_gew_greifer_leer = number_soll(
                "Leergewicht des Greifers [kg]",
                ist_greifer_state["leergewicht_kg"],
                0, 100, 15_000,
                "soll_leergew",
            )
            soll_vol_greifer = number_soll(
                "Greifervolumen [m³]",
                ist_greifer_state["volumen_m3"],
                0, 0.1, 15,
                "soll_volgreif",
            )
            soll_ges_greifen = number_soll(
                "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
                ist_greifer_state["geschwindigkeit_m_pro_min"],
                0, 1, 200,
                "soll_gesgreif",
            )
            soll_bes_greifen = number_soll(
                "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
                ist_greifer_state["beschleunigung_m_pro_s2"],
                0, 0.1, 10,
                "soll_besgreif",
            )

        # Hydraulikgreifer
        elif soll_auswahl == std.hydr["Greiferart"]:
            soll_gew_greifer_leer = number_soll(
                "Leergewicht des Greifers [kg]",
                ist_greifer_state["leergewicht_kg"],
                0, 100, 15_000,
                "soll_leergew",
            )
            soll_vol_greifer = number_soll(
                "Greifervolumen [m³]",
                ist_greifer_state["volumen_m3"],
                0, 0.1, 15,
                "soll_volgreif",
            )
            soll_ges_greifen = number_soll(
                "Greifergeschwindigkeit beim Öffnen/Schließen [m/min]",
                ist_greifer_state["geschwindigkeit_m_pro_min"],
                0, 1, 200,
                "soll_gesgreif",
            )
            soll_bes_greifen = number_soll(
                "Greiferbeschleunigung beim Öffnen/Schließen [m/s²]",
                ist_greifer_state["beschleunigung_m_pro_s2"],
                0, 0.1, 10,
                "soll_besgreif",
            )
            soll_p_hydr_motor = number_soll(
                "Motorleistung [kW]",
                ist_greifer_state["motorleistung_kw"],
                0, 1, 250,
                "soll_motorleist",
            )
            soll_n_hydr_motor = number_soll(
                "Wirkungsgrad Hydraulik",
                ist_greifer_state["wirkungsgrad_hydraulik"],
                0, 0.01, 1,
                "soll_wirkhyrd",
            )
            soll_volumenstrom = number_soll(
                "Volumenstrom [l/min]",
                ist_greifer_state["volumenstrom_l_pro_min"],
                0, 1, 150,
                "soll_volstr",
            )
            soll_betriebsdruck = number_soll(
                "Betriebsdruck [bar]",
                ist_greifer_state["betriebsdruck_bar"],
                0, 1, 300,
                "soll_betdruck",
            )
            soll_ant_bew_masse = number_standard(
                "Anteil der bewegten Masse am Greifer [%]",
                ist_greifer_state["anteil_bew_masse"],
                0,0.1,1,
                "soll_antbewma"
            )
        else:
            st.write("Bitte wählen Sie die Art des Greifers aus")

    with st.expander("Krananlage", False):
        st.title("Mechanische Krandaten")
        # Container im Session State initialisieren
        st.session_state["neu_anlage"]["kran_mechanik"]={}
        soll_kran_state = st.session_state["neu_anlage"]["kran_mechanik"]
        soll_kran_state["hubwerk"] = {}
        soll_kran_state["katze"] = {}
        soll_kran_state["kranfahrwerk"] = {}
        soll_kran_hub_state = soll_kran_state["hubwerk"]
        soll_kran_katz_state = soll_kran_state["katze"]
        soll_kran_kran_state = soll_kran_state["kranfahrwerk"]
        ist_kran_state = ist_state["kran_mechanik"]
        ist_kran_hub_state = ist_kran_state["hubwerk"]
        ist_kran_katz_state = ist_kran_state["katze"]
        ist_kran_kran_state = ist_kran_state["kranfahrwerk"]

        # Hubwerk
        with st.expander("Hubwerk", False):
            soll_seilgewicht = number_soll(
                "Seilgewicht [kg]", 
                ist_kran_hub_state["seilgewicht_kg"], 
                0, 1, 500, 
                "soll_soll_seilgew"
            )
            soll_hub_geschwindigkeit = number_soll(
                "Hubgeschwindigkeit [m/min]",
                ist_kran_hub_state["hub_geschwindigkeit_m_pro_min"],
                0,
                1,
                100,
                "soll_hubgeschw",
            )
            soll_hub_beschleunigung = number_soll(
                "Hubbeschleunigung [m/s²]",
                ist_kran_hub_state["hub_beschleunigung_m_pro_s2"],
                0,
                0.01,
                5,
                "soll_hubbeschl",
            )
            soll_anzahl_motoren_hub = number_soll(
                "Anzahl Motoren Hubwerk",
                ist_kran_hub_state["anzahl_motoren"],
                0,
                1,
                10,
                "soll_anzmotor_hub",
                "Anzahl der Motoren, welche die Hubarbeit teilen",
                0
            )
            soll_wirkungsgrad_getr_stufe_hub = number_soll(
                "Wirkungsgrad Getriebestufe Hubwerk",
                ist_kran_hub_state["wirkungsgrad_getriebe"],
                0,
                0.01,
                1,
                "soll_wirkgetr_hub",
            )
            soll_wirkungsgrad_seiltrieb = number_soll(
                "Wirkungsgrad Seiltrieb",
                ist_kran_hub_state["wirkungsgrad_seiltrieb"],
                0,
                0.01,
                1,
                "soll_wirkseil",
            )
            soll_getriebestufen_hub = number_soll(
                "Getriebestufen Hubwerk",
                ist_kran_hub_state["getriebestufen"],
                0,
                1,
                10,
                "soll_getrstuf_hub",
                "Anzahl der Getriebestufen des Hubwerkes",
                0
            )

            # Anzeigen des Ausgewählten Motors
            soll_motor_hub = mechleistunghubwerk(
                gewicht_seile = soll_seilgewicht,
                gewicht_greifer_leer = soll_gew_greifer_leer,   # type: ignore[possibly-unbound]
                greifer_volumen = soll_vol_greifer,             # type: ignore[possibly-unbound]
                muell_dichte = soll_müll_dichte_beschickung,
                geschwindigkeit_mmin = soll_hub_geschwindigkeit,
                beschleunigung_zeit = soll_hub_geschwindigkeit / 60 / soll_hub_beschleunigung,
                wirkungsgrad_seiltrieb = soll_wirkungsgrad_seiltrieb,
                wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_hub,
                getriebestufen = soll_getriebestufen_hub,
                motor_anzahl = soll_anzahl_motoren_hub,
                belastungsfaktor=1.55
            )["Motorauswahl"]
            number_soll("Von uns gewählte Hubmotorleistung [kW]", 
                            soll_motor_hub, 
                            0, 1, 200, 
                            "mtr_swhl_hb", 
                            "Der angezeigte Motor wird durch die vorherigen Eingaben intern berechnet"
                            )
            soll_wirkungsgrad_motor_hub = number_soll("Wirkungsgrad des Hubmotors", 
                                                    ist_kran_hub_state["wirkungsgrad_motor_hub"], 
                                                    0, 0.01, 1, 
                                                    "wrkgd_mtr_hb", 
                                                    "Der Standardwert des Wirkungsgrades beruht auf einem Erfahrungswert.")

        # Katze
        with st.expander("Katze", expanded = False):
            soll_gewicht_katze = number_soll(
                "Gewicht der Katze [kg]",
                ist_kran_katz_state["gewicht_kg"],
                0,
                1,
                100_000,
                "soll_gewkatze",
            )
            soll_geschwindigkeit_katze = number_soll(
                "Fahrgeschwindigkeit Katze [m/min]",
                ist_kran_katz_state["geschwindigkeit_m_pro_min"],
                0,
                1,
                100,
                "soll_geschwkatze",
            )
            soll_beschleunigung_katze = number_soll(
                "Beschleunigung Katze [m/s²]",
                ist_kran_katz_state["beschleunigung_m_pro_s2"],
                0,
                0.01,
                5,
                "soll_beschlkatze",
            )
            soll_anzahl_motoren_katze = number_soll(
                "Anzahl Motoren Katze",
                ist_kran_katz_state["anzahl_motoren"],
                0,
                1,
                10,
                "soll_anzmotkatze",
                "Anzahl der Motoren, welche die Katzfahrt teilen",
                0
            )
            soll_wirkungsgrad_getr_stufe_katze = number_soll(
                "Wirkungsgrad Getriebestufe Katze",
                ist_kran_katz_state["wirkungsgrad_getriebe"],
                0,
                0.001,
                1,
                "soll_wirkgetrkatze",
            )
            soll_getriebestufen_katze = number_soll(
                "Getriebestufen Katze",
                ist_kran_katz_state["getriebestufen"],
                0,
                1,
                10,
                "soll_getrstufkatze",
                "Anzahl der Getriebestufen des Katzfahrwerkes",
                0
            )
            soll_fahrwiderstand_katze = number_soll(
                "Fahrwiderstand Katze [kg/t]",
                ist_kran_katz_state["fahrwiderstand_kg_pro_t"],
                0,
                0.1,
                100,
                "soll_fahrwidkatze",
            )

            # Motor berechnen und anzeigen. User kann noch Werte ändern
            soll_mot_katze=mechleistungkatzfahrt(
                gewicht_seile = soll_seilgewicht,
                gewicht_greifer_leer = soll_gew_greifer_leer,   # type: ignore[possibly-unbound]
                greifer_volumen = soll_vol_greifer,             # type: ignore[possibly-unbound]
                muell_dichte = soll_müll_dichte_beschickung,
                gewicht_katze = soll_gewicht_katze,
                geschwindigkeit_mmin = soll_geschwindigkeit_katze,
                fahrwerkwiderstand = soll_fahrwiderstand_katze,
                getriebestufen = int(soll_getriebestufen_katze),
                wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_katze,
                motorzahl = int(soll_anzahl_motoren_katze),
                beschleunigungszeit = int(soll_geschwindigkeit_katze / 60.0 / soll_beschleunigung_katze),
                belastungsfaktor=1.55
                )["Motorauswahl"]
            number_soll("Von uns gewählte Katzmotorleistung [kW]", 
                            soll_mot_katze, 
                            0, 1, 200, 
                            "soll_minmotorkatze"
                            )
            soll_wirkungsgrad_motor_katze = number_soll("Wirkungsgrad des Katzmotors", 
                                                    ist_kran_katz_state["wirkungsgrad_motor_katze"], 
                                                    0, 0.01, 1,
                                                    "soll_wirkmotorkatze")

        # Kran
        with st.expander("Kranfahrwerk", expanded = False):
            soll_gewicht_kran = number_soll(
                "Kranfahrwerk Gewicht [kg]",
                ist_kran_kran_state["gewicht_kg"],
                0,
                1,
                500_000,
                "soll_gewkran",
            )
            soll_geschwindigkeit_kran = number_soll(
                "Kranfahrgeschwindigkeit [m/min]",
                ist_kran_kran_state["geschwindigkeit_m_pro_min"],
                0,
                1,
                100,
                "soll_geschwkran",
            )
            soll_beschleunigung_kran = number_soll(
                "Kranfahrbeschleunigung [m/s²]",
                ist_kran_kran_state["beschleunigung_m_pro_s2"],
                0,
                0.1,
                5,
                "soll_beschlkran",
            )
            soll_anzahl_motoren_kran = number_soll(
                "Anzahl Motoren Kran",
                ist_kran_kran_state["anzahl_motoren"],
                0,
                1,
                10,
                "soll_anzmotkran",
                "Anzahl der Motoren, welche die Kranfahrt teilen",
                0
            )
            soll_wirkungsgrad_getr_stufe_kran = number_soll(
                "Wirkungsgrad Getriebestufe Kran",
                ist_kran_kran_state["wirkungsgrad_getriebe"],
                0,
                0.01,
                1,
                "soll_wirkgetrkran",
            )
            soll_wirkungsgrad_vorgelege = number_soll(
                "Wirkungsgrad Vorgelege",
                ist_kran_kran_state["wirkungsgrad_vorgelege"],
                0,
                0.01,
                1,
                "soll_wirkvorgelege",
            )
            soll_getriebestufen_kran = number_soll(
                "Getriebestufen Kran",
                ist_kran_kran_state["getriebestufen"],
                0,
                1,
                10,
                "soll_getrstufkran",
            )
            soll_fahrwiderstand_kran = number_soll(
                "Fahrwiderstand Kran[kg/t]",
                ist_kran_kran_state["fahrwiderstand_kg_pro_t"],
                0,
                0.1,
                100,
                "soll_fahrwidkran",
            )

            # Motor berechnen und anzeigen. User kann noch die Werte verändern
            soll_motor_kran = kranfahrt(
                gewicht_greifer_leer = soll_gew_greifer_leer,   # type: ignore[possibly-unbound]
                greifer_volumen = soll_vol_greifer,             # type: ignore[possibly-unbound]
                muell_dichte = soll_müll_dichte_beschickung,
                gewicht_katze = soll_gewicht_katze,
                gewicht_kran = soll_gewicht_kran,
                gewicht_seile = soll_seilgewicht,
                geschwindigkeit_mmin = soll_geschwindigkeit_kran,
                fahrwiderstand = soll_fahrwiderstand_kran,
                motoranzahl = soll_anzahl_motoren_kran,
                wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_kran,
                getriebestufen = soll_getriebestufen_kran,
                beschleunigungszeit=int(soll_geschwindigkeit_kran / 60 / soll_beschleunigung_kran),
                belastungsfaktor=1.55
            )["Motorauswahl"]
            number_soll("Von uns gewählte Kranmotorleistung [kW]", 
                            soll_motor_kran, 
                            0, 1, 200, 
                            "soll_mtr_swhl_krn", 
                            "Der angezeigte Motor wird durch die vorherigen Eingaben intern berechnet"
                            )
            soll_wirkungsgrad_motor_kran = number_soll("Wirkungsgrad des Kranmotors", 
                                                    ist_kran_kran_state["wirkungsgrad_motor_kran"], 
                                                    0, 0.01, 1, 
                                                    "wrkgd_mtr_krn", 
                                                    "Der Standardwert des Wirkungsgrades beruht auf einem Erfahrungswert.")
            
    with st.expander("Referenzwege", False):

        st.title("Wege")

        # Container im Session State
        st.session_state["neu_anlage"]["wege"] = {}
        soll_wege_state = st.session_state["neu_anlage"]["wege"]
        ist_wege_state = ist_state["wege"]

        soll_weg_hebensenken_m = number_soll(
            "Referenzweg Heben senken [m]",
            ist_wege_state["weg_hebensenken_m"],
            0,
            1,
            200,
            "soll_wg_hs_m",
            nachkommastellen=0
        )
        soll_weg_katzfahrt_m = number_soll(
            "Referenzweg Katzfahrt [m]",
            ist_wege_state["weg_katzfahrt_m"],
            0,
            1,
            200,
            "soll_wg_ktzfhrt_m",
            nachkommastellen=0
        )
        soll_weg_kranfahrt_m = number_soll(
            "Referenzweg Kranfahrt Einlagern [m]",
            ist_wege_state["weg_kranfahrt_einlagern_m"],
            0,
            1,
            200,
            "soll_wg_krnfhrt_m",
            nachkommastellen=0
        )
        soll_weg_oeffnenschliessn_m = number_soll(
            "Referenzweg Greifer Öffnen/Schließen",
            ist_wege_state["weg_oeffnen_schliessen_m"],
            0,
            1,
            200,
            "soll_wg_ofnschl_m",
            nachkommastellen=0
        )

        soll_weg_trichter = {}
        for zahl in range(int(soll_anzahl_trichter)):
            key = f"soll_Trichterweg {zahl + 1}"
            try: 
                value = ist_state["wege"]["weg_trichter_m"][zahl]
            except: 
                value = STANDARDWERTE["Referenzwege"][f"Trichterweg {zahl +1}"]
                
            soll_weg_trichter[zahl] = number_soll(
                f"Referenzweg Trichter {zahl + 1}",
                value,
                0,
                1,
                200,
                f"soll_wg_tr_{zahl + 1}",
                nachkommastellen=0,
            )

    with st.expander("Rückspeisung", False):

        st.title("Rückspeisung")

        # Container im Session State
        st.session_state["neu_anlage"]["rueckspeisung"] = {}
        soll_rueckspeisung_state = st.session_state["neu_anlage"]["rueckspeisung"]
        ist_rueckspeisung_state = ist_state["rueckspeisung"]

        if (soll_auswahl=="Vierseil-Greifer"):
            soll_rueckspeisung_greifer = rueckspeisung_standard(
                "Rückspeisung Greifer", 
                ist_rueckspeisung_state["FU-Wirkungsgrad greifer"] or STANDARDWERTE["Rückspeisung"]["FU-Wirkungsgrad Greifer"], 
                0, 0.01, 1, 
                "soll_rckspng_grfr", 
                "Hat die Anlage eine Rückspeisung bei Greifer Öffnen/Schließen?", 
                2
            )
        else:
            soll_rueckspeisung_greifer = [0,0]

        soll_rueckspeisung_hub = rueckspeisung_standard(
            "Rückspeisung Hubfahrt",
            ist_rueckspeisung_state["FU-Wirkungsgrad hub"] or STANDARDWERTE["Rückspeisung"]["FU-Wirkungsgrad Hubfahrt"],
            0, 0.01, 1,
            "soll_rckspng_hb",
            "Hat die Anlage eine Rückspeisung bei der Hubfahrt?",
            2
        )

        soll_rueckspeisung_kran = rueckspeisung_standard(
            "Rückspeisung Kranfahrt",
            ist_rueckspeisung_state["FU-Wirkungsgrad kran"] or STANDARDWERTE["Rückspeisung"]["FU-Wirkungsgrad Kranfahrt"],
            0, 0.01, 1,
            "soll_rckspng_krn",
            "Hat die Anlage eine Rückspeisung bei der Kranfahrt?",
            2
        )

        soll_rueckspeisung_katz = rueckspeisung_standard(
            "Rückspeisung Katzfahrt",
            ist_rueckspeisung_state["FU-Wirkungsgrad katze"] or STANDARDWERTE["Rückspeisung"]["FU-Wirkungsgrad Katzfahrt"],
            0, 0.01, 1,
            "soll_rckspng_ktzfhrt",
            "Hat die Anlage eine Rückspeisung bei der Katzfahrt?",
            2
        )

soll_anlage_state.update(
{
    "anzahl_trichter": soll_anzahl_trichter,
    "verbrennung_trichter_kg": soll_verbrennung_trichter,
    "müll_anlieferung_h_kg": soll_müll_anlieferung_h,
    "müll_dichte_beschickung_kg_pro_m3": soll_müll_dichte_beschickung,
    "müll_dichte_anlieferung_kg_pro_m3": soll_müll_dichte_anlieferung,
    "anlage_standort": soll_anlage_standort,
    "energie_kosten": soll_energie_kosten,
    "müll_anlieferdauer": soll_müll_anlieferdauer
    }
)    
soll_greifer_state.update(
    {
        "leergewicht_kg": soll_gew_greifer_leer,        # type: ignore[possibly-unbound]
        "volumen_m3": soll_vol_greifer,                 # type: ignore[possibly-unbound]
        "geschwindigkeit_m_pro_min": soll_ges_greifen,  # type: ignore[possibly-unbound]
        "beschleunigung_m_pro_s2": soll_bes_greifen,    # type: ignore[possibly-unbound]
    }
)
if soll_auswahl == std.viers["Greiferart"]:
    soll_greifer_state.update(
    {
        "typ": "Vierseil-Greifer",
    }
)
elif soll_auswahl == std.hydr["Greiferart"]:
        soll_greifer_state.update(
        {
            "typ": "Hydraulikgreifer",
            "motorleistung_kw": soll_p_hydr_motor,      # type: ignore[possibly-unbound]
            "wirkungsgrad_hydraulik": soll_n_hydr_motor,# type: ignore[possibly-unbound]
            "volumenstrom_l_pro_min": soll_volumenstrom,# type: ignore[possibly-unbound]
            "betriebsdruck_bar": soll_betriebsdruck,    # type: ignore[possibly-unbound]
            "anteil_bew_masse": soll_ant_bew_masse,      # type: ignore[possibly-unbound]
        }
        )   
soll_kran_state.update(
    {
        "hubwerk": {
            "seilgewicht_kg": soll_seilgewicht,
            "hub_geschwindigkeit_m_pro_min": soll_hub_geschwindigkeit,
            "hub_beschleunigung_m_pro_s2": soll_hub_beschleunigung,
            "anzahl_motoren": soll_anzahl_motoren_hub,
            "wirkungsgrad_getriebe": soll_wirkungsgrad_getr_stufe_hub,
            "wirkungsgrad_seiltrieb": soll_wirkungsgrad_seiltrieb,
            "getriebestufen": soll_getriebestufen_hub,
            "wirkungsgrad_motor_hub": soll_wirkungsgrad_motor_hub
        },
        "katze": {
            "gewicht_kg": soll_gewicht_katze,
            "geschwindigkeit_m_pro_min": soll_geschwindigkeit_katze,
            "beschleunigung_m_pro_s2": soll_beschleunigung_katze,
            "anzahl_motoren": soll_anzahl_motoren_katze,
            "wirkungsgrad_getriebe": soll_wirkungsgrad_getr_stufe_katze,
            "getriebestufen": soll_getriebestufen_katze,
            "fahrwiderstand_kg_pro_t": soll_fahrwiderstand_katze,
            "wirkungsgrad_motor_katze": soll_wirkungsgrad_motor_katze
        },
        "kranfahrwerk": {
            "gewicht_kg": soll_gewicht_kran,
            "geschwindigkeit_m_pro_min": soll_geschwindigkeit_kran,
            "beschleunigung_m_pro_s2": soll_beschleunigung_kran,
            "anzahl_motoren": soll_anzahl_motoren_kran,
            "wirkungsgrad_getriebe": soll_wirkungsgrad_getr_stufe_kran,
            "wirkungsgrad_vorgelege": soll_wirkungsgrad_vorgelege,
            "getriebestufen": soll_getriebestufen_kran,
            "fahrwiderstand_kg_pro_t": soll_fahrwiderstand_kran,
            "wirkungsgrad_motor_kran": soll_wirkungsgrad_motor_kran
        },
    }
)
soll_wege_state.update(
    {
        "weg_hebensenken_m": soll_weg_hebensenken_m,
        "weg_katzfahrt_m": soll_weg_katzfahrt_m,
        "weg_kranfahrt_einlagern_m": soll_weg_kranfahrt_m,
        "weg_oeffnen_schliessen_m": soll_weg_oeffnenschliessn_m,
        "weg_trichter_m": soll_weg_trichter,
    }
)
soll_rueckspeisung_state.update(
    {
            "faktor greifer": soll_rueckspeisung_greifer[1],
            "FU-Wirkungsgrad greifer": soll_rueckspeisung_greifer[0],
            "faktor hub": soll_rueckspeisung_hub[1],
            "FU-Wirkungsgrad hub": soll_rueckspeisung_hub[0],
            "faktor kran": soll_rueckspeisung_kran[1],
            "FU-Wirkungsgrad kran": soll_rueckspeisung_kran[0],
            "faktor katze": soll_rueckspeisung_katz[1],
            "FU-Wirkungsgrad katze": soll_rueckspeisung_katz[0]
    }
)


# Visualisierung der Berechnungen

with st.expander("Debug session state", False):
    st.write(st.session_state)

st.write("Visualisierungen:")
faktor = plot_slider_global()
plot_ldaten_rdiagramm("Energieverbrauch", "kWh",  
                      berechnungen_pro_tag(st.session_state["ist_anlage"])["Verbrauch"],
                      berechnungen_pro_tag(st.session_state["neu_anlage"])["Verbrauch"],
                      faktor
                      )
plot_ldaten_rdiagramm("Energierückspeisung", "kWh",
                      berechnungen_pro_tag(st.session_state["ist_anlage"])["Rückspeisung"],
                      berechnungen_pro_tag(st.session_state["neu_anlage"])["Rückspeisung"],
                      faktor, "normal"
                      )
plot_ldaten_rdiagramm(f"Approximierte Betriebskosten in {st.session_state["ist_anlage"]["anlage"]["anlage_standort"]}", "EUR€",
                      berechnungen_pro_tag(st.session_state["ist_anlage"])["Kosten"],
                      berechnungen_pro_tag(st.session_state["neu_anlage"])["Kosten"],
                      faktor
                      )
plot_aufteilung_CO2(soll_anlage_standort,
                    berechnungen_pro_tag(st.session_state["ist_anlage"])["Verbrauch"],
                    berechnungen_pro_tag(st.session_state["neu_anlage"])["Verbrauch"],
                    faktor
                    )

button = st.button("Woher kommen die Werte?")
if button:
    st.switch_page("pages/ModellQuellen.py")