### Seite zur Konfiguration der Neu-Anlage und Auswertung und Visualisierung der Eingaben
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
import pandas as pd
from typing import cast
# Eigene Module mit Funktionen
from ui.components import number_standard, number_soll, selectbox_soll, plot_vergleich_ldaten_rdiagramm, rueckspeisung_standard, \
                          plot_vergleich_aufteilung_co2, plot_slider_global, plot_ldaten_rdiagramm, plot_aufteilung_co2
from core.computing import mechleistunghubwerk, kranfahrt, mechleistungkatzfahrt, berechnungen_pro_tag
from common.page_init import page_init
# Standardwerte
from config.standards import hydr, viers, wege, ruecksp

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
# Marker für Navigationsleiste aktivieren
st.session_state.setdefault("marker_navigation", True)
page_init("Auswertung", "📊", "wide")

## Container für diese Seite im Session State erstellen, sofern noch nicht vorhanden
# Bestandsanlagen #
ist_state = st.session_state.get("ist_anlage", {})
# Anlage
ist_anlage_state = ist_state.get("anlage", {})
# Krandaten
ist_kran_state = ist_state.get("kran_mechanik", {})
ist_kran_hub_state = ist_kran_state.get("hubwerk", {})
ist_kran_katz_state = ist_kran_state.get("katze", {})
ist_kran_kran_state = ist_kran_state.get("kranfahrwerk", {})
# Greiferdaten
ist_greifer_state = ist_state.get("greifer", {})
# Wegdaten
ist_wege_state = ist_state.get("wege", {})
# Rückspeisung
ist_rueckspeisung_state = ist_state.get("rueckspeisung", {})

# Neu-Anlage #
soll_state = st.session_state.setdefault("neu_anlage", {})
# Anlage
soll_anlage_state = soll_state.setdefault("anlage", {})
# Krandaten
soll_kran_state = soll_state.setdefault("kran_mechanik", {})
# Greiferdaten
soll_greifer_state = soll_state.setdefault("greifer", {})
# Wegdaten
soll_wege_state = soll_state.setdefault("wege", {})
soll_weg_trichter = {}
# Rückspeisung
soll_rueckspeisung_state = soll_state.setdefault("rueckspeisung", {})

## Länderpreise für automatischen Tarifvorschlag laden
df_laender = pd.read_csv("tabellen/Stromländerpreise+CO2.csv", sep=';')
df_laender = df_laender[df_laender["Land"].str.strip().str.lower() != "co2faktor"]

## UI-Inhalte der Auswertungsseite
st.title("📊 Auswertung")
st.info(
    "Auf dieser Seite erfolgt die energetische, wirtschaftliche und ökologische Auswertung der Anlage.\n\n"
    "Sie können zwischen zwei Analysearten wählen:\n"
    "• **Eigenanlage-Analyse**: Es wird ausschließlich der aktuelle IST-Zustand bewertet.\n"
    "• **Vergleich mit modernisierter Neu-Anlage**: Der IST-Zustand wird einer angepassten bzw. modernisierten Variante gegenübergestellt.\n\n"
    "Im Vergleichsmodus können einzelne Parameter gezielt verändert werden, "
    "um Auswirkungen auf Energieverbrauch, Rückspeisung, Betriebskosten und CO₂-Emissionen "
    "transparent darzustellen.\n\n"
    "Die Berechnungen basieren auf den zuvor eingegebenen mechanischen, betrieblichen und standortspezifischen Daten."
)

auswahl_auswertung = st.radio("Auswertungsart:",["Eigenanlage-Analyse","Vergleich mit modernisierter Neu-Anlage"], 
                              key="radio_auswertung")

if auswahl_auswertung == "Vergleich mit modernisierter Neu-Anlage":
    # Parameterauswahl
    with st.expander("Parameter für Modernisierung", True):
        with st.expander("Allgemeine Anlagendaten", False):
            st.header("Allgemeinen Anlagendaten")

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
            soll_verbrennung_trichter_kg = number_soll(
                "Verbrennung je Trichter [kg]",
                ist_anlage_state["verbrennung_trichter_kg"],
                0, 100, 100_000,
                "soll_vbrng_trichter",
                "Verbrennung pro Trichter in kg"
            )
            # Mülldaten
            st.write("# :grey[Mülldaten]")
            soll_muell_anlieferung_h_kg = number_soll(
                "Durchschnittliche Müllanliefermenge pro Stunde [kg]",
                ist_anlage_state["muell_anlieferung_h_kg"],
                0, 100, 1_000_000,
                "soll_ml_anlfrmg",
            )
            soll_muell_dichte_beschickung_kg_pro_m3 = number_soll(
                "Müll Dichte bei Beschickung [kg/m³]",
                ist_anlage_state["muell_dichte_beschickung_kg_pro_m3"],
                0, 100, 2000,
                "soll_ml_dcht_beschickung",
            )
            soll_muell_dichte_anlieferung_kg_pro_m3 = number_soll(
                "Müll Dichte bei Einlagerung [kg/m³]",
                ist_anlage_state["muell_dichte_anlieferung_kg_pro_m3"],
                0, 100, 2000,
                "soll_ml_dcht_anlieferung",
            )
            soll_muell_anlieferdauer = number_standard(
                "Müll Anlieferdauer [h/d]",
                ist_anlage_state["muell_anlieferdauer"],
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

            # Vorzeitige Deklaration, um theoretisch ungebundene Werte zu vermeiden
            soll_oeffnungszeit_greifen = ist_greifer_state["oeffnungszeit_s"]
            soll_schliesszeit_greifen = ist_greifer_state["schliesszeit_s"]
            soll_p_hydr_motor = ist_greifer_state["motorleistung_kw"]
            soll_n_hydr_motor = ist_greifer_state["wirkungsgrad_hydraulik"]
            soll_volumenstrom = ist_greifer_state["volumenstrom_l_pro_min"]
            soll_betriebsdruck = ist_greifer_state["betriebsdruck_bar"]
            soll_gew_greifer_leer = ist_greifer_state["leergewicht_kg"]
            soll_vol_greifer = ist_greifer_state["volumen_m3"]
            soll_ges_greifen = ist_greifer_state["geschwindigkeit_m_pro_min"]
            soll_bes_greifen = ist_greifer_state["beschleunigung_m_pro_s2"]
            soll_auswahl_parameter = ist_greifer_state["auswahl_parameter"]

            # beim ersten aufruf: soll = ist
            if "soll_radio_greifer_arten" not in st.session_state:
                st.session_state["soll_radio_greifer_arten"] = ist_greifer_state.get("typ", viers["greiferart"])

            # Radio Buttons erstellen
            soll_greifer_arten = [viers["greiferart"], hydr["greiferart"]]
            if ist_greifer_state["typ"] == "vierseil_greifer": 
                standard_index = 0 
            else: 
                standard_index = 1
            soll_auswahl_greifer = st.radio("Greiferart:", soll_greifer_arten, 
                                    key="soll_radio_greifer_arten", index=standard_index)
            if soll_auswahl_greifer not in soll_greifer_arten:
                soll_auswahl_greifer = viers["greiferart"]  # Standardwert setzen, falls ungültige Auswahl getroffen wird

            # Vierseil-Greifer
            if soll_auswahl_greifer == viers["greiferart"]:
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
            elif soll_auswahl_greifer == hydr["greiferart"]:
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

                # Die Auswahl, ob Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingegeben werden soll
                if soll_auswahl_parameter == "schliess_oeffnungszeit":
                    parameter_index = 0
                else:
                    parameter_index = 1
                soll_auswahl_parameter = st.radio("Schließ/Öffnungszeit oder Geschwindigkeit/Beschleunigung eingeben?", 
                        ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"], key="soll_radio_greifer_oeffnen_schliessen", index=parameter_index)
                if soll_auswahl_parameter not in ["Schließ/Öffnungszeit", "Geschwindigkeit/Beschleunigung"]:
                    soll_auswahl_parameter = "Schließ/Öffnungszeit"  # Standardwert setzen, falls ungültige Auswahl getroffen wird

                if soll_auswahl_parameter == "schliess_oeffnungszeit":
                    soll_oeffnungszeit_greifen = number_standard(
                        "Öffnungszeit [s]",
                        ist_greifer_state["oeffnungszeit_s"],
                        0, 1, 30,
                        "soll_oeffnzeit",
                    )
                    soll_schliesszeit_greifen = number_standard(
                        "Schließzeit [s]",
                        ist_greifer_state["schliesszeit_s"],
                        0, 1, 30,
                        "soll_schliesszeit",
                    )

                if soll_auswahl_parameter == "geschwindigkeit_beschleunigung":
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

        with st.expander("Krananlage", False):

            st.title("Mechanische Krandaten")

            # Hubwerk
            with st.expander("Hubwerk", False):
                soll_seilgewicht_kg = number_soll(
                    "Seilgewicht [kg]", 
                    ist_kran_hub_state["seilgewicht_kg"], 
                    0, 1, 500, 
                    "soll_seilgew"
                )
                soll_hub_geschwindigkeit_m_pro_min = number_soll(
                    "Hubgeschwindigkeit [m/min]",
                    ist_kran_hub_state["hub_geschwindigkeit_m_pro_min"],
                    0,
                    1,
                    100,
                    "soll_hubgeschw",
                )
                soll_hub_beschleunigung_m_pro_s2 = number_soll(
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
                    gewicht_seile = soll_seilgewicht_kg,
                    gewicht_greifer_leer = soll_gew_greifer_leer,
                    greifer_volumen = soll_vol_greifer,
                    muell_dichte = soll_muell_dichte_beschickung_kg_pro_m3,
                    geschwindigkeit_mmin = soll_hub_geschwindigkeit_m_pro_min,
                    beschleunigung_zeit = soll_hub_geschwindigkeit_m_pro_min / 60 / soll_hub_beschleunigung_m_pro_s2,
                    wirkungsgrad_seiltrieb = soll_wirkungsgrad_seiltrieb,
                    wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_hub,
                    getriebestufen = soll_getriebestufen_hub,
                    motor_anzahl = soll_anzahl_motoren_hub,
                    belastungsfaktor=1.55
                )["motorauswahl"]
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
                soll_gewicht_katze_kg = number_soll(
                    "Gewicht der Katze [kg]",
                    ist_kran_katz_state["gewicht_kg"],
                    0,
                    1,
                    100_000,
                    "soll_gewkatze",
                )
                soll_geschwindigkeit_katze_m_pro_min = number_soll(
                    "Fahrgeschwindigkeit Katze [m/min]",
                    ist_kran_katz_state["geschwindigkeit_m_pro_min"],
                    0,
                    1,
                    100,
                    "soll_geschwkatze",
                )
                soll_beschleunigung_katze_m_pro_s2 = number_soll(
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
                soll_mot_katze = mechleistungkatzfahrt(
                    gewicht_seile = soll_seilgewicht_kg,
                    gewicht_greifer_leer = soll_gew_greifer_leer,    
                    greifer_volumen = soll_vol_greifer,              
                    muell_dichte = soll_muell_dichte_beschickung_kg_pro_m3,
                    gewicht_katze = soll_gewicht_katze_kg,
                    geschwindigkeit_mmin = soll_geschwindigkeit_katze_m_pro_min,
                    fahrwerkwiderstand = soll_fahrwiderstand_katze,
                    getriebestufen = int(soll_getriebestufen_katze),
                    wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_katze,
                    motorzahl = int(soll_anzahl_motoren_katze),
                    beschleunigungszeit = int(soll_geschwindigkeit_katze_m_pro_min / 60.0 / soll_beschleunigung_katze_m_pro_s2),
                    belastungsfaktor=1.55
                    )["motorauswahl"]
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
                soll_gewicht_kran_kg = number_soll(
                    "Kranfahrwerk Gewicht [kg]",
                    ist_kran_kran_state["gewicht_kg"],
                    0,
                    1,
                    500_000,
                    "soll_gewkran",
                )
                soll_geschwindigkeit_kran_m_pro_min = number_soll(
                    "Kranfahrgeschwindigkeit [m/min]",
                    ist_kran_kran_state["geschwindigkeit_m_pro_min"],
                    0,
                    1,
                    100,
                    "soll_geschwkran",
                )
                soll_beschleunigung_kran_m_pro_s2 = number_soll(
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
                    gewicht_greifer_leer = soll_gew_greifer_leer,    
                    greifer_volumen = soll_vol_greifer,              
                    muell_dichte = soll_muell_dichte_beschickung_kg_pro_m3,
                    gewicht_katze = soll_gewicht_katze_kg,
                    gewicht_kran = soll_gewicht_kran_kg,
                    gewicht_seile = soll_seilgewicht_kg,
                    geschwindigkeit_mmin = soll_geschwindigkeit_kran_m_pro_min,
                    fahrwiderstand = soll_fahrwiderstand_kran,
                    motoranzahl = soll_anzahl_motoren_kran,
                    wirkungsgrad_getriebestufe = soll_wirkungsgrad_getr_stufe_kran,
                    getriebestufen = soll_getriebestufen_kran,
                    beschleunigungszeit=int(soll_geschwindigkeit_kran_m_pro_min / 60 / soll_beschleunigung_kran_m_pro_s2),
                    belastungsfaktor=1.55
                )["motorauswahl"]
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

            anzahl_trichter = int(soll_anzahl_trichter)

            if anzahl_trichter > 0:
                for zahl in range(anzahl_trichter):
                    default_value = ist_wege_state.get("weg_trichter_m", {}).get(zahl)

                    if default_value is None:
                        # Fallback auf Standardwerte, falls IST noch leer ist
                        key = f"trichterweg_{zahl + 1}_m"
                        default_value = wege[key]

                    soll_weg_trichter[zahl] = number_soll(
                        f"Referenzweg Trichter {zahl + 1}",
                        default_value,
                        0,
                        1,
                        200,
                        f"soll_wg_tr_{zahl + 1}",
                        nachkommastellen=0,
                    )
            else:
                st.warning('Bitte zuerst in der Seite "Anlage" die Anzahl der Trichter eingeben.')

        with st.expander("Rückspeisung", False):

            st.title("Rückspeisung")

            if (soll_auswahl_greifer == "Vierseil-Greifer"):
                soll_rueckspeisung_greifer = rueckspeisung_standard(
                    "Rückspeisung Greifer", 
                    ist_rueckspeisung_state["fu_wirkungsgrad_greifer"] or ruecksp["fu_wirkungsgrad_greifer"], 
                    0, 0.01, 1, 
                    "soll_rckspng_grfr", 
                    "Hat die Anlage eine Rückspeisung bei Greifer Öffnen/Schließen?", 
                    2
                )
            else:
                soll_rueckspeisung_greifer = [0,0]

            soll_rueckspeisung_hub = rueckspeisung_standard(
                "Rückspeisung Hubfahrt",
                ist_rueckspeisung_state["fu_wirkungsgrad_hub"] or ruecksp["fu_wirkungsgrad_hubfahrt"],
                0, 0.01, 1,
                "soll_rckspng_hb",
                "Hat die Anlage eine Rückspeisung bei der Hubfahrt?",
                2
            )

            soll_rueckspeisung_kran = rueckspeisung_standard(
                "Rückspeisung Kranfahrt",
                ist_rueckspeisung_state["fu_wirkungsgrad_kran"] or ruecksp["fu_wirkungsgrad_kranfahrt"],
                0, 0.01, 1,
                "soll_rckspng_krn",
                "Hat die Anlage eine Rückspeisung bei der Kranfahrt?",
                2
            )

            soll_rueckspeisung_katz = rueckspeisung_standard(
                "Rückspeisung Katzfahrt",
                ist_rueckspeisung_state["fu_wirkungsgrad_katze"] or ruecksp["fu_wirkungsgrad_katzfahrt"],
                0, 0.01, 1,
                "soll_rckspng_ktzfhrt",
                "Hat die Anlage eine Rückspeisung bei der Katzfahrt?",
                2
            )

        ## Session_State updaten usw.
        soll_anlage_state.update(
        {
            "anzahl_kraene": soll_anzahl_kraene,
            "anzahl_trichter": soll_anzahl_trichter,
            "verbrennung_trichter_kg": soll_verbrennung_trichter_kg,
            "muell_anlieferung_h_kg": soll_muell_anlieferung_h_kg,
            "muell_dichte_beschickung_kg_pro_m3": soll_muell_dichte_beschickung_kg_pro_m3,
            "muell_dichte_anlieferung_kg_pro_m3": soll_muell_dichte_anlieferung_kg_pro_m3,
            "anlage_standort": soll_anlage_standort,
            "energie_kosten": soll_energie_kosten,
            "muell_anlieferdauer": soll_muell_anlieferdauer
            }
        )    
        soll_greifer_state.update(
            {
                "auswahl_parameter": soll_auswahl_parameter,
                "leergewicht_kg": soll_gew_greifer_leer,
                "volumen_m3": soll_vol_greifer,
                "geschwindigkeit_m_pro_min": soll_ges_greifen,
                "beschleunigung_m_pro_s2": soll_bes_greifen,
                "oeffnungszeit_s": soll_oeffnungszeit_greifen,
                "schliesszeit_s": soll_schliesszeit_greifen,
                "typ": soll_auswahl_greifer,
                "motorleistung_kw": soll_p_hydr_motor,
                "wirkungsgrad_hydraulik": soll_n_hydr_motor,
                "volumenstrom_l_pro_min": soll_volumenstrom,
                "betriebsdruck_bar": soll_betriebsdruck,
            }
        )  
        soll_kran_state.update(
            {
                "hubwerk": {
                    "seilgewicht_kg": soll_seilgewicht_kg,
                    "hub_geschwindigkeit_m_pro_min": soll_hub_geschwindigkeit_m_pro_min,
                    "hub_beschleunigung_m_pro_s2": soll_hub_beschleunigung_m_pro_s2,
                    "anzahl_motoren": soll_anzahl_motoren_hub,
                    "wirkungsgrad_getriebe": soll_wirkungsgrad_getr_stufe_hub,
                    "wirkungsgrad_seiltrieb": soll_wirkungsgrad_seiltrieb,
                    "getriebestufen": soll_getriebestufen_hub,
                    "wirkungsgrad_motor_hub": soll_wirkungsgrad_motor_hub
                },
                "katze": {
                    "gewicht_kg": soll_gewicht_katze_kg,
                    "geschwindigkeit_m_pro_min": soll_geschwindigkeit_katze_m_pro_min,
                    "beschleunigung_m_pro_s2": soll_beschleunigung_katze_m_pro_s2,
                    "anzahl_motoren": soll_anzahl_motoren_katze,
                    "wirkungsgrad_getriebe": soll_wirkungsgrad_getr_stufe_katze,
                    "getriebestufen": soll_getriebestufen_katze,
                    "fahrwiderstand_kg_pro_t": soll_fahrwiderstand_katze,
                    "wirkungsgrad_motor_katze": soll_wirkungsgrad_motor_katze
                },
                "kranfahrwerk": {
                    "gewicht_kg": soll_gewicht_kran_kg,
                    "geschwindigkeit_m_pro_min": soll_geschwindigkeit_kran_m_pro_min,
                    "beschleunigung_m_pro_s2": soll_beschleunigung_kran_m_pro_s2,
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
                    "faktor_greifer": soll_rueckspeisung_greifer[1],
                    "fu_wirkungsgrad_greifer": soll_rueckspeisung_greifer[0],
                    "faktor_hub": soll_rueckspeisung_hub[1],
                    "fu_wirkungsgrad_hub": soll_rueckspeisung_hub[0],
                    "faktor_kran": soll_rueckspeisung_kran[1],
                    "fu_wirkungsgrad_kran": soll_rueckspeisung_kran[0],
                    "faktor_katze": soll_rueckspeisung_katz[1],
                    "fu_wirkungsgrad_katze": soll_rueckspeisung_katz[0]
            }
        )

    # Visualisierung der Berechnungen
    faktor = plot_slider_global()

    plot_vergleich_ldaten_rdiagramm("Energieverbrauch", "kWh",  
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["verbrauch"],
                        berechnungen_pro_tag(st.session_state["neu_anlage"])["verbrauch"],
                        faktor
                        )
    plot_vergleich_ldaten_rdiagramm("Energierückspeisung", "kWh",
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["rueckspeisung"],
                        berechnungen_pro_tag(st.session_state["neu_anlage"])["rueckspeisung"],
                        faktor, "normal"
                        )
    plot_vergleich_ldaten_rdiagramm(f"Approximierte Betriebskosten in {st.session_state['ist_anlage']['anlage']['anlage_standort']}", "EUR€",
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["kosten"],
                        berechnungen_pro_tag(st.session_state["neu_anlage"])["kosten"],
                        faktor
                        )
    plot_vergleich_aufteilung_co2(soll_anlage_standort,
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["verbrauch"],
                        berechnungen_pro_tag(st.session_state["neu_anlage"])["verbrauch"],
                        faktor
                        )
else:
    faktor = plot_slider_global()
    plot_ldaten_rdiagramm("Energieverbrauch", "kWh",  
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["verbrauch"],
                        faktor
                        )
    plot_ldaten_rdiagramm("Energierückspeisung", "kWh",
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["rueckspeisung"],
                        faktor
                        )
    plot_ldaten_rdiagramm(f"Approximierte Betriebskosten in {st.session_state['ist_anlage']['anlage']['anlage_standort']}", "EUR€",
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["kosten"],
                        faktor
                        )
    plot_aufteilung_co2(ist_anlage_state["anlage_standort"],
                        berechnungen_pro_tag(st.session_state["ist_anlage"])["verbrauch"],
                        faktor
                        )
    
button = st.button("Woher kommen die Werte?")
if button:
    st.switch_page("pages/modell_quellen.py")