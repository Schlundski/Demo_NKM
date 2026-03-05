## Hier werden die Berechnungen in Funktionen geschrieben, welche dictionarys ausgeben, sodass man über den key
## immer genau abrufen kann, was man haben möchte
import numpy
from config.standards import Motorleistungen

# Allgemeine Berechnungen
def spielzeitenberechnung(geschwindigkeit_mmin, beschleunigung_mss, weg):

    """ Berechnung der Spielzeiten durch die gegebenen Argumente.

    Ausgegeben wird über ein Dictionary die values über folgende keys:

        "beschleunigungszeit"
        "beschleunigungsweg"
        "kontinuierliche_zeit"
        "kontinuierlicher_weg"
        "summe_der_zeit"

        """

    geschwindigkeit_ms = float(geschwindigkeit_mmin) / 60                   # [m/s] = [m/min] / 60
    beschleunigung_zeit = geschwindigkeit_ms / beschleunigung_mss           # [s]   = [m/s] / [m/s²]
    beschleunigung_weg = (beschleunigung_zeit**2) * (beschleunigung_mss / 2)# [m]   = [s²] * ([m/s²] / 2)
    kontinuierlich_weg = weg - (2* beschleunigung_weg)                      # [m]   = [m] - ( 2 * m )
    kontinuierlich_zeit = kontinuierlich_weg / geschwindigkeit_ms           # [s]   = [m] / [m/s]
    summe_zeit = kontinuierlich_zeit + (2* beschleunigung_zeit)             # [s]   = [s] + ( 2 * [s] )

    return {
        "beschleunigungszeit": beschleunigung_zeit, 
        "beschleunigungsweg": beschleunigung_weg,
        "kontinuierliche_zeit": kontinuierlich_zeit,
        "kontinuierlicher_weg": kontinuierlich_weg,
        "summe_der_zeit": summe_zeit
        }

def muellberechnung(
        anzahl_trichter, verbrennung_je_trichter_proh, anliefermenge_stunde, greifer_volumen,muell_dichte_beschickung, 
        muell_dichte_einlagerung, anlieferdauer
        ):
    
    """ Alle Berechnungen zum Thema Müll
    
    Ausgegeben wird ein Dictionary mit values zu folgenden keys:

        "gesamtbeschleunigungsleistung_voll"
        "muelleinlagerung_kg_pro_zyklus"
        "anzahl_zyklen_muelleinlagerung_pro_h"
        "anzahl_zyklen_muelleinlagerung_pro_d"
        "trichterbeschickungsmuell_kg_pro_zyklus"
        "anzahl_zyklen_trichterbeschickung_pro_h"
        "anzahl_zyklen_trichterbeschickung_pro_d"
        "anzahl_zyklen_trichterbeschickung_gesamt_pro_d"
    """

    muell_gesamt_proh = (anzahl_trichter * verbrennung_je_trichter_proh) + anliefermenge_stunde # [kg/h]    = ([1] * [kg]) + [kg/h]
    muell_einlagerung_prozyklus = greifer_volumen * muell_dichte_einlagerung                    # [kg/1]    = [m³] * [kg/m³]
    anzahl_zyklen_muelleinlagerung_proh = anliefermenge_stunde / muell_einlagerung_prozyklus    # [1/h]     = [kg/h] / [kg/1]
    anzahl_zyklen_muelleinlagerung_prod = anzahl_zyklen_muelleinlagerung_proh * anlieferdauer   # [1/d]     = [1/h] * [h/d]
    beschickung_prozyklus = muell_dichte_beschickung * greifer_volumen                          # [kg/1]    = [kg/m³] * [m³]
    anzahl_zyklen_beschickung_proh = verbrennung_je_trichter_proh / beschickung_prozyklus       # [1/h]     = [kg/h] / [kg/1]
    anzahl_zyklen_beschickung_prod = anzahl_zyklen_beschickung_proh * 24                        # [1/d]     = [1/h] * 24h
    anzahl_zyklen_beschickung_gesamt_prod = anzahl_zyklen_beschickung_prod * anzahl_trichter    # [1/d]     = [1/d] * [1]

    return {
        "gesamtbeschleunigungsleistung_voll": muell_gesamt_proh,
        "muelleinlagerung_kg_pro_zyklus": muell_einlagerung_prozyklus,
        "anzahl_zyklen_muelleinlagerung_pro_h": anzahl_zyklen_muelleinlagerung_proh,
        "anzahl_zyklen_muelleinlagerung_pro_d": anzahl_zyklen_muelleinlagerung_prod,
        "trichterbeschickungsmuell_kg_pro_zyklus": beschickung_prozyklus,
        "anzahl_zyklen_trichterbeschickung_pro_h": anzahl_zyklen_beschickung_proh,
        "anzahl_zyklen_trichterbeschickung_pro_d": anzahl_zyklen_beschickung_prod,
        "anzahl_zyklen_trichterbeschickung_gesamt_pro_d": anzahl_zyklen_beschickung_gesamt_prod
    }

# Mechanische Leistungsberechnungen
def mechleistungkatzfahrt(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, geschwindigkeit_mmin,
                          fahrwerkwiderstand=9.0, getriebestufen=3, wirkungsgrad_getriebestufe=0.980,  
                          motorzahl=1, beschleunigungszeit = 0, belastungsfaktor=1.55):
   
    """
    Funktion zur Berechnung der mech Leistung der Katzfahrt
    Ausgegeben wird ein Dict mit folgenden keys:
                motorauswahl
                beschleunigungsleistungen
                beharrungsleistung
                beschleunigungsleistungen_leer
                beharrungsleistung_leer
    """
 
    # Greifer voll
    gewicht_greifer_voll =      (greifer_volumen * muell_dichte) + gewicht_greifer_leer                                 # [kg]  = ( [m³] * [kg/m³] ) + [kg]
    geschwindigkeit_ms =        float(geschwindigkeit_mmin) / 60                                                        # [m/s] = [m/min] / 60
    wirkungsgrad_getriebe =     wirkungsgrad_getriebestufe ** getriebestufen                                            # [1]   = [1]^[1]
    gewicht_gesamt =            gewicht_greifer_voll + gewicht_katze + gewicht_seile                                    # [kg]  = [kg] + [kg] + [kg]
 
    motor_leistung_beharrung =  (fahrwerkwiderstand / 1000) * gewicht_gesamt * 9.81 * geschwindigkeit_ms \
                                    / wirkungsgrad_getriebe / 1000                                                      # [kW] = ([kg/t] / 1000 ) · [kg] · [m/s²] · [m/s] / [1] / 1000
   
    motor_leistung_beschl =     gewicht_gesamt * 0.5 * geschwindigkeit_ms ** 2 \
                                    / beschleunigungszeit / wirkungsgrad_getriebe / 1000                                # [kW] = [kg] * [1] * [(m/s)²] / ([m/s] / [m/s²]) * [1] / 1000
 
 
    motor_leistung_min =        motor_leistung_beharrung / motorzahl * belastungsfaktor       # [kW] = [kW] / [1] * [1]
   
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > motor_leistung_min:
            motor_auswahl = leistung
            break
 
    # Greifer leer                                 
    gewicht_gesamt_leer =           gewicht_greifer_leer + gewicht_katze + gewicht_seile                                # [kg] = [kg] + [kg] + [kg]
 
    motor_leistung_beharrung_leer = (fahrwerkwiderstand / 1000) * gewicht_gesamt_leer * 9.81 * geschwindigkeit_ms \
                                        / wirkungsgrad_getriebe / 1000                                                  # [kW] = ([kg/t] / 1000 ) · [kg] · [m/s²] · [m/s] / [1] / 1000
    motor_leistung_beschl_leer =    gewicht_gesamt_leer * 0.5 * geschwindigkeit_ms ** 2 \
                                        / beschleunigungszeit / wirkungsgrad_getriebe / 1000                            # [kW] = [kg] * [1] * [(m/s)²] / ([m/s] / [m/s²]) * [1] / 1000                                                                 # [kW] = ([kW] + [kW]) / [1]
 
    return {
                "motorauswahl": motor_auswahl,
                "beschleunigungsleistungen": motor_leistung_beschl,
                "beharrungsleistung": motor_leistung_beharrung,
                "beschleunigungsleistungen_leer": motor_leistung_beschl_leer,
                "beharrungsleistung_leer": motor_leistung_beharrung_leer
    }

def mechleistunghubwerk(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, geschwindigkeit_mmin, 
                         beschleunigung_zeit, wirkungsgrad_seiltrieb, wirkungsgrad_getriebestufe, 
                         getriebestufen, motor_anzahl, belastungsfaktor=1.55):
    
    """ Berechnen der mechanischen Leistungswerte des Hubwerkes. Ausgegeben wird ein Dict mit folgenden Keys:
        motorauswahl
        gesamtbeschleunigungsleistung_voll
        beharrungsleistung voll
        gesamtbeschleunigungsleistung_leer
        beharrungsleistung_leer
    """

    #  Grundlegende Berechnungen
    geschwindigkeit_ms = geschwindigkeit_mmin / 60                                              # [m/s] = [m/min] / 60
    wirkungsgrad_gesamt = wirkungsgrad_getriebestufe**getriebestufen * wirkungsgrad_seiltrieb   # [1]   = [1]^[1] * [1]

    # Berechnungen bei vollem Greifer (Hauptsächlich Heben)
    voll_gewicht_greifer = (greifer_volumen * muell_dichte) + gewicht_greifer_leer              # [kg]  = ( [m³] * [kg/m³] ) + [kg]
    voll_gewicht_gesamt = gewicht_seile + voll_gewicht_greifer                                  # [kg]  = [kg] + [kg]

    voll_motor_leistung_beharrung = voll_gewicht_gesamt * 9.81 * geschwindigkeit_ms \
        / wirkungsgrad_gesamt / 1000                                                            # [kW] = [kg] * [m/s²] * [m/s] / [1] / 1000
    voll_motor_leistung_beschleunigung_gesamt = (voll_gewicht_gesamt * 0.5 \
        * geschwindigkeit_ms**2) / (beschleunigung_zeit * wirkungsgrad_gesamt) / 1000           # [kW] = [kg] * 0.5 * [m²/s²] / [s] / [1] / 1000

    motor_leistung_min = voll_motor_leistung_beharrung / motor_anzahl * belastungsfaktor        # [kW] = [kW] / [1] * [1]
    
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > motor_leistung_min: 
            motor_auswahl = leistung
            break

    # Berechnung bei leerem Greifer (Hauptsächlich Senken)
    leer_gewicht_greifer = gewicht_greifer_leer                                                 # [kg]  = [kg]
    leer_gewicht_gesamt = gewicht_seile + leer_gewicht_greifer                                  # [kg]  = [kg] + [kg]

    leer_motor_leistung_beharrung = leer_gewicht_gesamt * 9.81 * geschwindigkeit_ms \
        / wirkungsgrad_gesamt / 1000                                                            # [kW] = [kg] * [m/s²] * [m/s] / [1] / 1000
    leer_motor_leistung_beschleunigung_gesamt = (leer_gewicht_gesamt * 0.5 * \
        geschwindigkeit_ms**2) / (beschleunigung_zeit * wirkungsgrad_gesamt) / 1000             # [kW] = [kg] * 0.5 * [m²/s²] / [s] / [1] / 1000

    return {
        "motorauswahl": motor_auswahl,
        "gesamtbeschleunigungsleistung_voll": voll_motor_leistung_beschleunigung_gesamt,
        "beharrungsleistung voll": voll_motor_leistung_beharrung,
        "gesamtbeschleunigungsleistung_leer": leer_motor_leistung_beschleunigung_gesamt,
        "beharrungsleistung_leer": leer_motor_leistung_beharrung,
    }

def greiferhydraulik(betriebsdruck=170, volumenstrom=66):

    """ Berechnung der benötigten mechanischen Leistung des Hydraulikgreifers
        Ausgegeben wird ein Dictionary mit folgenden Keys:
        
        leistung_beharrung"""
    
    leistung_hydraulisch_beharrung = betriebsdruck * volumenstrom / 600                          # [kW] = [bar] * [l/min] / 600

    return { 
        "leistung_beharrung": leistung_hydraulisch_beharrung,
            }

def kranfahrt(gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, gewicht_kran, gewicht_seile,
               geschwindigkeit_mmin, fahrwiderstand, motoranzahl, wirkungsgrad_getriebestufe,
               getriebestufen, beschleunigungszeit = 0, belastungsfaktor=1.55):
   
    """
        Funktion berechnet die mech Leistung der Kranfahrt und gibt die Mindestleistung und den nächstgrößeren Motor aus.
        Ebenfalls wird die Summe der beschleunigungsleistungen ausgegeben (Ohne weitere Berechnung, wie aufteilung auf Motoren etc.)
 
        Ausgegeben wird ein Dict mit folgenden Keys:
        motorauswahl
        beschleunigungsleistungen
        beharrungsleistung
        beschleunigungsleistungen_leer
        beharrungsleistung_leer
    """
   
    gewicht_greifer_voll = (greifer_volumen * muell_dichte) + gewicht_greifer_leer                      # [kg] = ([m³] * [kg/m³]) + [kg]
    gewicht_gesamt = gewicht_greifer_voll + gewicht_katze + gewicht_kran + gewicht_seile                # [kg] = [kg] + [kg] + [kg]
    geschwindigkeit_ms = geschwindigkeit_mmin / 60                                                      # [m/s] = [m/min] / 60
    wirkungsgrad_getriebe = wirkungsgrad_getriebestufe ** getriebestufen                                # [1] = [1] * [1]
 
 
    # Berechnungen bei vollem Greifer
    motor_leistung_beharrung =  (fahrwiderstand / 1000) * gewicht_gesamt * 9.81 * geschwindigkeit_ms \
                                    / wirkungsgrad_getriebe / 1000                                      # [kW] = ([kg/t] / 1000 ) · [kg] · [m/s²] · [m/s] / [1] / 1000
 
    motor_leistung_beschl =     gewicht_gesamt * 0.5 * geschwindigkeit_ms ** 2 \
                                    / beschleunigungszeit / wirkungsgrad_getriebe / 1000                # [kW] = [kg] * [1] * [(m/s)²] / ([m/s] / [m/s²]) * [1] / 1000
 
    motor_leistung_min = (motor_leistung_beharrung) / motoranzahl * belastungsfaktor                    # [kW] = [kW] / [1] * [1]
   
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > (motor_leistung_min):
            motor_auswahl = leistung
            break
 
    # Berechnungen bei leerem Greifer
    gewicht_gesamt_leer = gewicht_greifer_leer + gewicht_katze + gewicht_kran + gewicht_seile           # [kg] = [kg] + [kg] + [kg]
 
    motor_leistung_beharrung_leer =  (fahrwiderstand / 1000) * gewicht_gesamt_leer * 9.81 * geschwindigkeit_ms \
                                        / wirkungsgrad_getriebe / 1000                                  # [kW] = ([kg/t] / 1000 ) · [kg] · [m/s²] · [m/s] / [1] / 1000
    motor_leistung_beschl_leer =    gewicht_gesamt_leer * 0.5 * geschwindigkeit_ms ** 2 \
                                        / beschleunigungszeit / wirkungsgrad_getriebe / 1000            # [kW] = [kg] * [1] * [(m/s)²] / ([m/s] / [m/s²]) * [1] / 1000
 
   
    return {
        "motorauswahl" : motor_auswahl,
        "beschleunigungsleistungen": motor_leistung_beschl,
        "beharrungsleistung": motor_leistung_beharrung,
        "beschleunigungsleistungen_leer": motor_leistung_beschl_leer,
        "beharrungsleistung_leer": motor_leistung_beharrung_leer
    }
 
def mechleistunggreifervierseil(hubvorgang_beharrung_leistung, hubvorgang_beschl_leistung):
    """Die mechanische Leistungsberechnung des Greifers ergibt sich als Erfahrungswert aus einem Drittel des Hubvorganges
    Ausgegeben wird ein Dictionary mit den Key 'beharrungsleistung' und 'Beschleunigungsleistung'
    """

    beharrung_greifer = hubvorgang_beharrung_leistung / 3
    beschl_greifer = hubvorgang_beschl_leistung / 3

    return {"beharrungsleistung": beharrung_greifer,
            "Beschleunigungsleistung": beschl_greifer}

def berechnungen_pro_tag(dict):
    # region Variablen Deklarieren zum Abrufen der dict-Daten
    # Pfad-Variablen zur Vereinfachung einrichten
    dict_anlage = dict["anlage"]
    dict_greifer = dict["greifer"]
    dict_hub = dict["kran_mechanik"]["hubwerk"]
    dict_katz = dict["kran_mechanik"]["katze"]
    dict_kran = dict["kran_mechanik"]["kranfahrwerk"]
    dict_wege = dict["wege"]
    dict_rueckspeisung = dict["rueckspeisung"]

    ## Variablen deklarieren
    # Vordeklaration, damit "possibly unbound"-probleme vermieden werden

    # Mechanik Greifer
    df_mechleist_oeffnenschliessen_vierseil = {"beharrungsleistung": 0.0, "Beschleunigungsleistung": 0.0}
    df_mechleist_oeffnenschliessen_hydraulik = {"leistung_beharrung": 0.0}

    # Mechanische Energien Greifer
    df_mechenergie_greifer_oeffnenschliessen_vierseil = 0.0
    df_mechenergie_greifer_oeffnen_hydraulik = 0.0
    df_mechenergie_greifer_schliessen_hydraulik = 0.0
    df_mechenergie_greifer_oeffnenschliessen_hydraulik = 0.0

    # Elektrische Energien Greifer
    df_elenergie_greifer_vierseil_oeffnen = 0.0
    df_elenergie_greifer_vierseil_schliessen = 0.0
    df_elenergie_greifer_vierseil_oeffnen_rueckspeisung = 0.0
    df_elenergie_greifer_vierseil_schliessen_rueckspeisung = 0.0

    df_elenergie_greifer_oeffnen_hydraulik = 0.0
    df_elenergie_greifer_schliessen_hydraulik = 0.0
    df_elenergie_greifer_hydraulik_oeffnenschliessen = 0.0

    # Zyklusenergien
    df_elenergie_einlager_verbrauch_zyklus = 0.0
    df_elenergie_einlager_rueckspeisung_zyklus = 0.0
    df_elenergie_beschick_verbrauch_zyklus = 0.0
    df_elenergie_beschick_rueckspeisung_zyklus = 0.0

    ## Deklarationen für Short-Cuts, Übersicht, etc.
    # Anlage
    anlage_anzahl_trichter = dict_anlage["anzahl_trichter"]
    anlage_verbrennung_trichter_kg = dict_anlage["verbrennung_trichter_kg"]
    anlage_muell_anlieferung_h_kg = dict_anlage["muell_anlieferung_h_kg"]
    anlage_muell_dichte_beschickung_kg_pro_m3 = dict_anlage["muell_dichte_beschickung_kg_pro_m3"]
    anlage_muell_dichte_anlieferung_kg_pro_m3 = dict_anlage["muell_dichte_anlieferung_kg_pro_m3"]
    anlage_energie_kosten = dict_anlage["energie_kosten"]
    anlage_muell_anlieferdauer = dict_anlage["muell_anlieferdauer"]

    # Greifer
    greifer_parameter_typ = dict_greifer["auswahl_parameter"]
    greifer_leergewicht_kg = dict_greifer["leergewicht_kg"]
    greifer_volumen_m3 = dict_greifer["volumen_m3"]
    greifer_geschwindigkeit_m_pro_min = dict_greifer["geschwindigkeit_m_pro_min"]
    greifer_beschleunigung_m_pro_s2 = dict_greifer["beschleunigung_m_pro_s2"]
    greifer_typ = dict_greifer["typ"]
    greifer_volumenstrom_l_pro_min = dict_greifer["volumenstrom_l_pro_min"]
    greifer_betriebsdruck_bar = dict_greifer["betriebsdruck_bar"]
    greifer_schliesszeit_s = dict_greifer["schliesszeit_s"]
    greifer_oeffnungszeit_s = dict_greifer["oeffnungszeit_s"]

    # Kranmechanik
    # Hubwerk
    hubwerk_seilgewicht_kg = dict_hub["seilgewicht_kg"]
    hubwerk_hub_geschwindigkeit_m_pro_min = dict_hub["hub_geschwindigkeit_m_pro_min"]
    hubwerk_hub_beschleunigung_m_pro_s2 = dict_hub["hub_beschleunigung_m_pro_s2"]
    hubwerk_anzahl_motoren = dict_hub["anzahl_motoren"]
    hubwerk_wirkungsgrad_getriebe = dict_hub["wirkungsgrad_getriebe"]
    hubwerk_wirkungsgrad_seiltrieb = dict_hub["wirkungsgrad_seiltrieb"]
    hubwerk_getriebestufen = dict_hub["getriebestufen"]
    # Katzfahrwerk
    katze_gewicht_kg = dict_katz["gewicht_kg"]
    katze_geschwindigkeit_m_pro_min = dict_katz["geschwindigkeit_m_pro_min"]
    katze_beschleunigung_m_pro_s2 = dict_katz["beschleunigung_m_pro_s2"]
    katze_anzahl_motoren = dict_katz["anzahl_motoren"]
    katze_wirkungsgrad_getriebe = dict_katz["wirkungsgrad_getriebe"]
    katze_getriebestufen = dict_katz["getriebestufen"]
    katze_fahrwiderstand_kg_pro_t = dict_katz["fahrwiderstand_kg_pro_t"]
    # Kranfahrwerk
    kranfahrwerk_gewicht_kg = dict_kran["gewicht_kg"]
    kranfahrwerk_geschwindigkeit_m_pro_min = dict_kran["geschwindigkeit_m_pro_min"]
    kranfahrwerk_beschleunigung_m_pro_s2 = dict_kran["beschleunigung_m_pro_s2"]
    kranfahrwerk_anzahl_motoren = dict_kran["anzahl_motoren"]
    kranfahrwerk_wirkungsgrad_getriebe = dict_kran["wirkungsgrad_getriebe"]
    kranfahrwerk_getriebestufen = dict_kran["getriebestufen"]
    kranfahrwerk_fahrwiderstand_kg_pro_t = dict_kran["fahrwiderstand_kg_pro_t"]
    
    # Wege
    wege_weg_hebensenken_m = dict_wege["weg_hebensenken_m"]
    wege_weg_katzfahrt_m = dict_wege["weg_katzfahrt_m"]
    wege_weg_kranfahrt_einlagern_m = dict_wege["weg_kranfahrt_einlagern_m"]
    wege_weg_oeffnen_schliessen_m = dict_wege["weg_oeffnen_schliessen_m"]
    wege_weg_trichter_m = dict_wege["weg_trichter_m"]
    # endregion

    # region Grundfunktionen
    df_muell = muellberechnung(anlage_anzahl_trichter, anlage_verbrennung_trichter_kg, anlage_muell_anlieferung_h_kg, greifer_volumen_m3,
                   anlage_muell_dichte_beschickung_kg_pro_m3, anlage_muell_dichte_anlieferung_kg_pro_m3, anlage_muell_anlieferdauer)
    df_spielzeiten_hub = spielzeitenberechnung(hubwerk_hub_geschwindigkeit_m_pro_min, hubwerk_hub_beschleunigung_m_pro_s2, wege_weg_hebensenken_m)
    df_spielzeiten_katze = spielzeitenberechnung(katze_geschwindigkeit_m_pro_min, katze_beschleunigung_m_pro_s2, wege_weg_katzfahrt_m)
    df_spielzeiten_kran_einlager = spielzeitenberechnung(kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_beschleunigung_m_pro_s2, wege_weg_kranfahrt_einlagern_m)
    df_kran_beschick_wege_mittel = sum(wege_weg_trichter_m.values()) / len(wege_weg_trichter_m)
    df_spielzeiten_kran_beschick = spielzeitenberechnung(kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_beschleunigung_m_pro_s2, df_kran_beschick_wege_mittel)
    if greifer_typ == "Hydraulikgreifer":
        if greifer_parameter_typ == "Schließ/Öffnungszeit":
            df_spielzeiten_greifer = greifer_schliesszeit_s + greifer_oeffnungszeit_s
        else:
            df_spielzeiten_greifer = spielzeitenberechnung(greifer_geschwindigkeit_m_pro_min, greifer_beschleunigung_m_pro_s2, wege_weg_oeffnen_schliessen_m)
    else:
        df_spielzeiten_greifer = spielzeitenberechnung(greifer_geschwindigkeit_m_pro_min, greifer_beschleunigung_m_pro_s2, wege_weg_oeffnen_schliessen_m)
    # endregion

    # region grundlegende mechanische Leistungsberechnungen
    df_mechleist_katz_einlager = mechleistungkatzfahrt(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_anlieferung_kg_pro_m3, katze_gewicht_kg,
                                                       katze_geschwindigkeit_m_pro_min, katze_fahrwiderstand_kg_pro_t, katze_getriebestufen, katze_wirkungsgrad_getriebe, katze_anzahl_motoren,
                                                       df_spielzeiten_katze["beschleunigungszeit"])
    df_mechleist_katz_beschick = mechleistungkatzfahrt(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_beschickung_kg_pro_m3, katze_gewicht_kg,
                                                       katze_geschwindigkeit_m_pro_min, katze_fahrwiderstand_kg_pro_t, katze_getriebestufen, katze_wirkungsgrad_getriebe, katze_anzahl_motoren,
                                                       df_spielzeiten_katze["beschleunigungszeit"])
    df_mechleist_hub_einlager = mechleistunghubwerk(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_anlieferung_kg_pro_m3, hubwerk_hub_geschwindigkeit_m_pro_min, 
                                                    df_spielzeiten_hub["beschleunigungszeit"], hubwerk_wirkungsgrad_seiltrieb, hubwerk_wirkungsgrad_getriebe, hubwerk_getriebestufen, 
                                                    hubwerk_anzahl_motoren)
    df_mechleist_hub_beschick = mechleistunghubwerk(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_beschickung_kg_pro_m3, hubwerk_hub_geschwindigkeit_m_pro_min, 
                                                    df_spielzeiten_hub["beschleunigungszeit"], hubwerk_wirkungsgrad_seiltrieb, hubwerk_wirkungsgrad_getriebe, hubwerk_getriebestufen, 
                                                    hubwerk_anzahl_motoren)
    df_mechleist_kran_einlager = kranfahrt(greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_anlieferung_kg_pro_m3, katze_gewicht_kg, kranfahrwerk_gewicht_kg, hubwerk_seilgewicht_kg,
                                           kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_fahrwiderstand_kg_pro_t, kranfahrwerk_anzahl_motoren,
                                           kranfahrwerk_wirkungsgrad_getriebe, kranfahrwerk_getriebestufen, df_spielzeiten_kran_einlager["beschleunigungszeit"])
    df_mechleist_kran_beschick = kranfahrt(greifer_leergewicht_kg, greifer_volumen_m3, anlage_muell_dichte_beschickung_kg_pro_m3, katze_gewicht_kg, kranfahrwerk_gewicht_kg, hubwerk_seilgewicht_kg,
                                           kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_fahrwiderstand_kg_pro_t, kranfahrwerk_anzahl_motoren,
                                           kranfahrwerk_wirkungsgrad_getriebe, kranfahrwerk_getriebestufen, df_spielzeiten_kran_beschick["beschleunigungszeit"])
    if greifer_typ == "Vierseil-Greifer":
        df_mechleist_oeffnenschliessen_vierseil = mechleistunggreifervierseil(df_mechleist_hub_einlager["beharrungsleistung voll"], df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_voll"])
    elif greifer_typ == "Hydraulikgreifer":
        df_mechleist_oeffnenschliessen_hydraulik = greiferhydraulik(greifer_betriebsdruck_bar, greifer_volumenstrom_l_pro_min)
    # endregion

    # region mechanische Energieberechnungen einzelne Vorgänge

    # region Katze

    df_mechenergie_katz_einlager_voll = (
        df_mechleist_katz_einlager["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]
        + df_mechleist_katz_einlager["beharrungsleistung"] * df_spielzeiten_katze["kontinuierliche_zeit"]
    )
    df_mechenergie_katz_einlager_leer = (
        df_mechleist_katz_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]
        + df_mechleist_katz_einlager["beharrungsleistung_leer"] * df_spielzeiten_katze["kontinuierliche_zeit"] 
    )
    df_mechenergie_katz_beschick_voll = (
        df_mechleist_katz_beschick["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]
        + df_mechleist_katz_beschick["beharrungsleistung"] * df_spielzeiten_katze["kontinuierliche_zeit"]
    )
    df_mechenergie_katz_beschick_leer = (
        df_mechleist_katz_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]
        + df_mechleist_katz_beschick["beharrungsleistung_leer"] * df_spielzeiten_katze["kontinuierliche_zeit"] 
    )
    #endregion Katze

    # region Hub

    df_mechenergie_hub_einlager_voll = (
        df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]
        + df_mechleist_hub_einlager["beharrungsleistung voll"] * df_spielzeiten_hub["kontinuierliche_zeit"]
    )
    df_mechenergie_hub_einlager_leer = (
        df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]
        + df_mechleist_hub_einlager["beharrungsleistung_leer"] * df_spielzeiten_hub["kontinuierliche_zeit"]
    )
    df_mechenergie_hub_beschick_voll = (
        df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]
        + df_mechleist_hub_beschick["beharrungsleistung voll"] * df_spielzeiten_hub["kontinuierliche_zeit"]
    )
    df_mechenergie_hub_beschick_leer = (
        df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]
        + df_mechleist_hub_beschick["beharrungsleistung_leer"] * df_spielzeiten_hub["kontinuierliche_zeit"]
    )
    # endregion Hub

    # region Kran

    df_mechenergie_kran_einlager_voll = (
        df_mechleist_kran_einlager["beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]
        + df_mechleist_kran_einlager["beharrungsleistung"] * df_spielzeiten_kran_einlager["kontinuierliche_zeit"]
    )
    df_mechenergie_kran_einlager_leer = (
        df_mechleist_kran_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]
        + df_mechleist_kran_einlager["beharrungsleistung_leer"] * df_spielzeiten_kran_einlager["kontinuierliche_zeit"]
    )
    df_mechenergie_kran_beschick_voll = (
        df_mechleist_kran_beschick["beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]
        + df_mechleist_kran_beschick["beharrungsleistung"] * df_spielzeiten_kran_beschick["kontinuierliche_zeit"]
    )
    df_mechenergie_kran_beschick_leer = (
        df_mechleist_kran_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]
        + df_mechleist_kran_beschick["beharrungsleistung_leer"] * df_spielzeiten_kran_beschick["kontinuierliche_zeit"]
    )
    # endregion Kran

    # region Greifer
    if greifer_typ == "Vierseil-Greifer":
        df_mechenergie_greifer_oeffnenschliessen_vierseil = (
                df_mechleist_oeffnenschliessen_vierseil["Beschleunigungsleistung"] * df_spielzeiten_greifer["beschleunigungszeit"] 
                + df_mechleist_oeffnenschliessen_vierseil["beharrungsleistung"] * df_spielzeiten_greifer["kontinuierliche_zeit"] 
            )
        
    elif greifer_typ == "Hydraulikgreifer":
        if greifer_parameter_typ == "Schließ/Öffnungszeit":
            df_mechenergie_greifer_oeffnen_hydraulik = (
                df_mechleist_oeffnenschliessen_hydraulik["leistung_beharrung"] * greifer_oeffnungszeit_s 
            )
            df_mechenergie_greifer_schliessen_hydraulik = (
                df_mechleist_oeffnenschliessen_hydraulik["leistung_beharrung"] * greifer_schliesszeit_s
            )
        else:
            df_mechenergie_greifer_oeffnenschliessen_hydraulik = (
                df_mechleist_oeffnenschliessen_hydraulik["leistung_beharrung"] * df_spielzeiten_greifer["beschleunigungszeit"] 
                + df_mechleist_oeffnenschliessen_hydraulik["leistung_beharrung"] * df_spielzeiten_greifer["kontinuierliche_zeit"] 
            )
    # endregion Greifer
    # endregion mechanische Energieberechnung

    # region Elektrische Energieberechnung

    # region el Energie Katze
    df_elenergie_katz_einlager_voll = {
        "verbrauch": (
            df_mechenergie_katz_einlager_voll / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_einlager["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        ),
        "rueckspeisung": (
            (df_mechleist_katz_einlager["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        )
    }
    df_elenergie_katz_einlager_leer = {
        "verbrauch": (
            df_mechenergie_katz_einlager_leer / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        ),
        "rueckspeisung": (
            (df_mechleist_katz_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        )
    }
    df_elenergie_katz_beschick_voll = {
        "verbrauch": (
            df_mechenergie_katz_beschick_voll / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_beschick["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        ),
        "rueckspeisung": (
            (df_mechleist_katz_beschick["beschleunigungsleistungen"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        )
    }
    df_elenergie_katz_beschick_leer = {
        "verbrauch": (
            df_mechenergie_katz_beschick_leer / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        ),
        "rueckspeisung": (
            (df_mechleist_katz_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_katze["beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor_katze"] * dict_rueckspeisung["fu_wirkungsgrad_katze"]
        )
    }
    # endregion el Energie Katze

    # region el Energie Hub

    df_elenergie_hub_einlager_voll = {
        "verbrauch": (
            df_mechenergie_hub_einlager_voll / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        ),
        "rueckspeisung": (
            (df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        )
    }
    df_elenergie_hub_einlager_leer = {
        "verbrauch": (
            df_mechenergie_hub_einlager_leer / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        ),
        "rueckspeisung": (
            (df_mechleist_hub_einlager["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        )
    }
    df_elenergie_hub_beschick_voll = {
        "verbrauch": (
            df_mechenergie_hub_beschick_voll / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        ),
        "rueckspeisung": (
            (df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_voll"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        )
    }
    df_elenergie_hub_beschick_leer = {
        "verbrauch": (
            df_mechenergie_hub_beschick_leer / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        ),
        "rueckspeisung": (
            (df_mechleist_hub_beschick["gesamtbeschleunigungsleistung_leer"] * df_spielzeiten_hub["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_hub"] * dict_rueckspeisung["fu_wirkungsgrad_hub"]
        )
        }
    # endregion el Energie Hub

    # region el Energie Kran

    df_elenergie_kran_einlager_voll = {
        "verbrauch": (
            df_mechenergie_kran_einlager_voll / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_einlager["beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        ),
        "rueckspeisung": (
            (df_mechleist_kran_einlager["beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        )
    }
    df_elenergie_kran_einlager_leer = {
        "verbrauch": (
            df_mechenergie_kran_einlager_leer / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        ),
        "rueckspeisung": (
            (df_mechleist_kran_einlager["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        )
    }
    df_elenergie_kran_beschick_voll = {
        "verbrauch": (
            df_mechenergie_kran_beschick_voll / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_beschick["beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        ),
        "rueckspeisung": (
            (df_mechleist_kran_beschick["beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        )
    }
    df_elenergie_kran_beschick_leer = {
        "verbrauch": (
            df_mechenergie_kran_beschick_leer / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        ),
        "rueckspeisung": (
            (df_mechleist_kran_beschick["beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor_kran"] * dict_rueckspeisung["fu_wirkungsgrad_kran"]
        )
    }
    # endregion el Energie Kran

    # region el Energie Greifer

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_greifer_vierseil_oeffnen = (
            -1 * (df_mechenergie_greifer_oeffnenschliessen_vierseil) /dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_greifer"] * dict_rueckspeisung["fu_wirkungsgrad_greifer"]
        )
        df_elenergie_greifer_vierseil_schliessen = (
            df_mechenergie_greifer_oeffnenschliessen_vierseil / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_oeffnenschliessen_vierseil["Beschleunigungsleistung"] * df_spielzeiten_greifer["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_greifer"] * dict_rueckspeisung["fu_wirkungsgrad_greifer"]
        )
        df_elenergie_greifer_vierseil_oeffnen_rueckspeisung = (
            (df_mechenergie_greifer_oeffnenschliessen_vierseil) /dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_greifer"] * dict_rueckspeisung["fu_wirkungsgrad_greifer"]
        )
        df_elenergie_greifer_vierseil_schliessen_rueckspeisung = (
            (df_mechleist_oeffnenschliessen_vierseil["Beschleunigungsleistung"] * df_spielzeiten_greifer["beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor_greifer"] * dict_rueckspeisung["fu_wirkungsgrad_greifer"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        if greifer_parameter_typ == "Schließ/Öffnungszeit":
            df_elenergie_greifer_oeffnen_hydraulik = (
                (df_mechenergie_greifer_oeffnen_hydraulik) / dict_greifer["wirkungsgrad_hydraulik"]
            )
            df_elenergie_greifer_schliessen_hydraulik = (
                df_mechenergie_greifer_schliessen_hydraulik / dict_greifer["wirkungsgrad_hydraulik"]
            )
        else:
            df_elenergie_greifer_hydraulik_oeffnenschliessen = (
                df_mechenergie_greifer_oeffnenschliessen_hydraulik / dict_greifer["wirkungsgrad_hydraulik"]
            )
    # endregion el Energie Greifer
    
    # endregion Elektrische Energieberechnung

    # region Tagesberechnungen Einlagerung (Greifer schließen -> Heben -> Katzfahrt -> Kranfahrt -> Senken -> Greifer öffnen -> Heben -> Katzfahrt -> Kranfahrt -> Senken)
    
    df_zyklen_einlager_d = df_muell["anzahl_zyklen_muelleinlagerung_pro_d"]

    # Verbrauch

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_einlager_verbrauch_zyklus = (
            df_elenergie_greifer_vierseil_schliessen + 
            df_elenergie_hub_einlager_voll["verbrauch"] + 
            df_elenergie_katz_einlager_voll["verbrauch"] + 
            df_elenergie_kran_einlager_voll["verbrauch"] + 
            df_elenergie_hub_einlager_voll["verbrauch"] +
            df_elenergie_greifer_vierseil_oeffnen +
            df_elenergie_hub_einlager_leer["verbrauch"] +
            df_elenergie_kran_einlager_leer["verbrauch"] +
            df_elenergie_katz_einlager_leer["verbrauch"] +
            df_elenergie_hub_einlager_leer["verbrauch"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        if greifer_parameter_typ == "Schließ/Öffnungszeit":
            df_elenergie_einlager_verbrauch_zyklus = (
                df_elenergie_greifer_schliessen_hydraulik + 
                df_elenergie_hub_einlager_voll["verbrauch"] + 
                df_elenergie_katz_einlager_voll["verbrauch"] + 
                df_elenergie_kran_einlager_voll["verbrauch"] + 
                df_elenergie_hub_einlager_voll["verbrauch"] +
                df_elenergie_greifer_oeffnen_hydraulik +
                df_elenergie_hub_einlager_leer["verbrauch"] +
                df_elenergie_kran_einlager_leer["verbrauch"] +
                df_elenergie_katz_einlager_leer["verbrauch"] +
                df_elenergie_hub_einlager_leer["verbrauch"]
            )
        else:
            df_elenergie_einlager_verbrauch_zyklus = (
                df_elenergie_greifer_hydraulik_oeffnenschliessen + 
                df_elenergie_hub_einlager_voll["verbrauch"] + 
                df_elenergie_katz_einlager_voll["verbrauch"] + 
                df_elenergie_kran_einlager_voll["verbrauch"] + 
                df_elenergie_hub_einlager_voll["verbrauch"] +
                df_elenergie_greifer_hydraulik_oeffnenschliessen +
                df_elenergie_hub_einlager_leer["verbrauch"] +
                df_elenergie_kran_einlager_leer["verbrauch"] +
                df_elenergie_katz_einlager_leer["verbrauch"] +
                df_elenergie_hub_einlager_leer["verbrauch"]
            )
    df_elenergie_einlager_verbrauch_d = df_elenergie_einlager_verbrauch_zyklus * df_zyklen_einlager_d
    
    # Rückspeisung

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_einlager_rueckspeisung_zyklus = (
            df_elenergie_greifer_vierseil_schliessen_rueckspeisung +
            df_elenergie_hub_einlager_voll["rueckspeisung"] + 
            df_elenergie_katz_einlager_voll["rueckspeisung"] + 
            df_elenergie_kran_einlager_voll["rueckspeisung"] + 
            df_elenergie_hub_einlager_voll["rueckspeisung"] +
            df_elenergie_greifer_vierseil_oeffnen_rueckspeisung +
            df_elenergie_hub_einlager_leer["rueckspeisung"] +
            df_elenergie_kran_einlager_leer["rueckspeisung"] +
            df_elenergie_katz_einlager_leer["rueckspeisung"] +
            df_elenergie_hub_einlager_leer["rueckspeisung"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        df_elenergie_einlager_rueckspeisung_zyklus = (
            df_elenergie_hub_einlager_voll["rueckspeisung"] + 
            df_elenergie_katz_einlager_voll["rueckspeisung"] + 
            df_elenergie_kran_einlager_voll["rueckspeisung"] + 
            df_elenergie_hub_einlager_voll["rueckspeisung"] +
            df_elenergie_hub_einlager_leer["rueckspeisung"] +
            df_elenergie_kran_einlager_leer["rueckspeisung"] +
            df_elenergie_katz_einlager_leer["rueckspeisung"] +
            df_elenergie_hub_einlager_leer["rueckspeisung"]
        )
    df_elenergie_einlager_rueckspeisung_d = df_elenergie_einlager_rueckspeisung_zyklus * df_zyklen_einlager_d

    # endregion Tagesberechnung Einlagerung

    # region Tagesberechnungen Beschickung (Greifer schließen -> Heben -> Kranfahrt -> Katzfahrt -> Greifer öffnen -> Katzfahrt -> Kranfahrt -> Senken)

    df_zyklen_beschick_d = df_muell["anzahl_zyklen_trichterbeschickung_gesamt_pro_d"]

    # Verbrauch

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_beschick_verbrauch_zyklus = (
            df_elenergie_greifer_vierseil_schliessen + 
            df_elenergie_hub_beschick_voll["verbrauch"] +
            df_elenergie_kran_beschick_voll["verbrauch"] +
            df_elenergie_katz_beschick_voll["verbrauch"] +
            df_elenergie_greifer_vierseil_oeffnen +
            df_elenergie_katz_beschick_leer["verbrauch"] +
            df_elenergie_kran_beschick_leer["verbrauch"] +
            df_elenergie_hub_beschick_leer["verbrauch"]
        )
    if greifer_typ == "Hydraulikgreifer":
        if greifer_parameter_typ == "Schließ/Öffnungszeit":
            df_elenergie_beschick_verbrauch_zyklus = (
                df_elenergie_greifer_schliessen_hydraulik + 
                df_elenergie_hub_beschick_voll["verbrauch"] +
                df_elenergie_kran_beschick_voll["verbrauch"] +
                df_elenergie_katz_beschick_voll["verbrauch"] +
                df_elenergie_greifer_oeffnen_hydraulik +
                df_elenergie_katz_beschick_leer["verbrauch"] +
                df_elenergie_kran_beschick_leer["verbrauch"] +
                df_elenergie_hub_beschick_leer["verbrauch"]
            )
        else:
            df_elenergie_beschick_verbrauch_zyklus = (
                df_elenergie_greifer_hydraulik_oeffnenschliessen + 
                df_elenergie_hub_beschick_voll["verbrauch"] +
                df_elenergie_kran_beschick_voll["verbrauch"] +
                df_elenergie_katz_beschick_voll["verbrauch"] +
                df_elenergie_greifer_hydraulik_oeffnenschliessen +
                df_elenergie_katz_beschick_leer["verbrauch"] +
                df_elenergie_kran_beschick_leer["verbrauch"] +
                df_elenergie_hub_beschick_leer["verbrauch"]
            )
    df_elenergie_beschick_verbrauch_d = df_elenergie_beschick_verbrauch_zyklus * df_zyklen_beschick_d

    # Rückspeisung 

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_beschick_rueckspeisung_zyklus = (
            df_elenergie_greifer_vierseil_schliessen_rueckspeisung +
            df_elenergie_hub_beschick_voll["rueckspeisung"] +
            df_elenergie_kran_beschick_voll["rueckspeisung"] +
            df_elenergie_greifer_vierseil_oeffnen_rueckspeisung +
            df_elenergie_katz_beschick_leer["rueckspeisung"] +
            df_elenergie_kran_beschick_leer["rueckspeisung"] +
            df_elenergie_hub_beschick_leer["rueckspeisung"]
        )
    if greifer_typ == "Hydraulikgreifer":
        df_elenergie_beschick_rueckspeisung_zyklus = (
            df_elenergie_hub_beschick_voll["rueckspeisung"] +
            df_elenergie_kran_beschick_voll["rueckspeisung"] +
            df_elenergie_katz_beschick_voll["rueckspeisung"] +
            df_elenergie_katz_beschick_leer["rueckspeisung"] +
            df_elenergie_kran_beschick_leer["rueckspeisung"] +
            df_elenergie_hub_beschick_leer["rueckspeisung"]
        )
    df_elenergie_beschick_rueckspeisung_d = df_elenergie_beschick_rueckspeisung_zyklus * df_zyklen_beschick_d

    # endregion Tagesberechnung Beschickung

    # Gesamtenergie in kWh

    df_elenergie_verbrauch_kwh      = (df_elenergie_beschick_verbrauch_d + df_elenergie_einlager_verbrauch_d) / 3600
    df_elenergie_rueckspeisung_kwh  = (df_elenergie_beschick_rueckspeisung_d + df_elenergie_einlager_rueckspeisung_d) / 3600
    
    # region Tagesberechnungen Energiekosten nach Region

    df_elenergie_kosten_eur = df_elenergie_verbrauch_kwh * anlage_energie_kosten / 100  # Euro für gesamtverbrauch


    return {
        "verbrauch": df_elenergie_verbrauch_kwh,
        "rueckspeisung": df_elenergie_rueckspeisung_kwh,
        "kosten": df_elenergie_kosten_eur,
        #"CO2": pass,
    }

