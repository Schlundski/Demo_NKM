
## Hier werden die Berechnungen in Funktionen geschrieben, welche dictionarys ausgeben, sodass man über den key
## immer genau abrufen kann, was man haben möchte
import numpy
from config.standards import Motorleistungen

# Fehlermeldung "Variable is possibly unbound" ignorieren, da zwingend einer der zwei Greiferfälle ist
# pyright: reportPossiblyUnboundVariable=false

# Allgemeine Berechnungen
def spielzeitenberechnung(geschwindigkeit_mmin, beschleunigung_mss, weg):

    """ Berechnung der Spielzeiten durch die gegebenen Argumente.

    Ausgegeben wird über ein Dictionary die values über folgende keys:

        "Beschleunigungszeit"
        "Beschleunigungsweg"
        "Kontinuierliche Zeit"
        "Kontinuierlicher Weg"
        "Summe der Zeit"

        """

    geschwindigkeit_ms = float(geschwindigkeit_mmin) / 60                   # [m/s] = [m/min] / 60
    beschleunigung_zeit = geschwindigkeit_ms / beschleunigung_mss           # [s]   = [m/s] / [m/s²]
    beschleunigung_weg = (beschleunigung_zeit**2) * (beschleunigung_mss / 2)# [m]   = [s²] * ([m/s²] / 2)
    kontinuierlich_weg = weg - (2* beschleunigung_weg)                      # [m]   = [m] - ( 2 * m )
    kontinuierlich_zeit = kontinuierlich_weg / geschwindigkeit_ms           # [s]   = [m] / [m/s]
    summe_zeit = kontinuierlich_zeit + (2* beschleunigung_zeit)             # [s]   = [s] + ( 2 * [s] )

    return {
        "Beschleunigungszeit": beschleunigung_zeit, 
        "Beschleunigungsweg": beschleunigung_weg,
        "Kontinuierliche Zeit": kontinuierlich_zeit,
        "Kontinuierlicher Weg": kontinuierlich_weg,
        "Summe der Zeit": summe_zeit
        }

def muellberechnung(
        anzahl_trichter, verbrennung_je_trichter_proh, anliefermenge_stunde, greifer_volumen,muell_dichte_beschickung, 
        muell_dichte_einlagerung, anlieferdauer
        ):
    
    """ Alle Berechnungen zum Thema Müll
    
    Ausgegeben wird ein Dictionary mit values zu folgenden keys:

        "Gesamter zu transportierender Müll kg / h"
        "Mülleinlagerung kg / Zyklus"
        "Anzahl Zyklen Mülleinlagerung / h"
        "Anzahl Zyklen Mülleinlagerung / d"
        "Trichterbeschickungsmüll kg / Zyklus"
        "Anzahl Zyklen Trichterbeschickung / h"
        "Anzahl Zyklen Trichterbeschickung / d"
        "Anzahl Zyklen Trichterbeschickung gesamt / d"
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
        "Gesamter zu transportierender Müll kg / h": muell_gesamt_proh,
        "Mülleinlagerung kg / Zyklus": muell_einlagerung_prozyklus,
        "Anzahl Zyklen Mülleinlagerung / h": anzahl_zyklen_muelleinlagerung_proh,
        "Anzahl Zyklen Mülleinlagerung / d": anzahl_zyklen_muelleinlagerung_prod,
        "Trichterbeschickungsmüll kg / Zyklus": beschickung_prozyklus,
        "Anzahl Zyklen Trichterbeschickung / h": anzahl_zyklen_beschickung_proh,
        "Anzahl Zyklen Trichterbeschickung / d": anzahl_zyklen_beschickung_prod,
        "Anzahl Zyklen Trichterbeschickung gesamt / d": anzahl_zyklen_beschickung_gesamt_prod
    }

# Mechanische Leistungsberechnungen
def mechleistungkatzfahrt(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, geschwindigkeit_mmin, beschleunigung_m_ss, drehzahl=0, 
                          fahrwerkwiderstand=9.0, getriebestufen=3, wirkungsgrad_getriebestufe=0.980, massentraegheit=0.01, 
                          belastungsfaktor=1.55, motorzahl=1):
    
    """ 
    Funktion zur Berechnung der mech Leistung der Katzfahrt
    Ausgegeben wird ein Dict mit folgenden keys:
    Mindestmotorleistung kW
    Motorauswahl
    Beschleunigungsleistungen kW
    """

    # Greifer voll
    gewicht_greifer_voll = (greifer_volumen * muell_dichte) + gewicht_greifer_leer  # [kg]  = ( [m³] * [kg/m³] ) + [kg]
    geschwindigkeit_ms = float(geschwindigkeit_mmin) / 60                           # [m/s] = [m/min] / 60
    wirkungsgrad_getriebe = wirkungsgrad_getriebestufe ** getriebestufen            # [1]   = [1]^[1]
    gewicht_gesamt = gewicht_greifer_voll + gewicht_katze + gewicht_seile           # [kg]  = [kg] + [kg] + [kg]

    motor_leistung_beharrung = (fahrwerkwiderstand / 1000) * gewicht_gesamt * 9.81 * geschwindigkeit_ms / wirkungsgrad_getriebe / 1000  # [kW] = ([kg/t] / 1000 ) · [kg] · [m/s²] · [m/s] / [1] / 1000
    motor_leistung_beschl_translatorisch = gewicht_gesamt * geschwindigkeit_ms * beschleunigung_m_ss / wirkungsgrad_getriebe / 1000     # [kW] = [kg] * [m/s] [m/s²] / [1] / 1000
    omega = 2 * numpy.pi * drehzahl / 60                 # [1/s]    = 2 * pi * [1/min] / 60
    radius_eff_m = 0.20 # geschätzter Allgemeinwert zur Vereinfachung
    alpha = beschleunigung_m_ss / radius_eff_m           # [1/s²]   = [m/s²] / [m]
    motor_leistung_beschl_rotierend = massentraegheit * alpha * omega / wirkungsgrad_getriebe / 1000        # [kW] = [kg*m²] * [1/s²]] * [1/s] / [1] / 1000

    motor_leistung_min = (motor_leistung_beharrung + motor_leistung_beschl_translatorisch + motor_leistung_beschl_rotierend) / motorzahl / belastungsfaktor
    # [kW] = ( [kW] + [kW] + [kW] ) / [1] / [1]
    
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > (motor_leistung_min*1.1/1000): 
            motor_auswahl = leistung
            break

    motor_leistung_beschl_summe = motor_leistung_beschl_translatorisch + motor_leistung_beschl_rotierend    

    # Greifer leer
    wirkungsgrad_getriebe = wirkungsgrad_getriebestufe ** getriebestufen
    gewicht_gesamt_leer = gewicht_greifer_leer + gewicht_katze + gewicht_seile

    motor_leistung_beharrung_leer = fahrwerkwiderstand * gewicht_gesamt_leer * 9.81 * geschwindigkeit_ms / wirkungsgrad_getriebe / 1000
    motor_leistung_beschl_translatorisch_leer = gewicht_gesamt_leer * geschwindigkeit_ms**2 / beschleunigung_m_ss / wirkungsgrad_getriebe
    motor_leistung_beschl_rotierend_leer = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / beschleunigung_m_ss

    motor_leistung_leer = (motor_leistung_beharrung_leer + motor_leistung_beschl_translatorisch_leer + motor_leistung_beschl_rotierend_leer) / motorzahl / belastungsfaktor
    motor_leistung_beschl_leer = (motor_leistung_beschl_rotierend_leer + motor_leistung_beschl_translatorisch_leer)

    return {
                "Mindestmotorleistung": motor_leistung_min,
                "Motorauswahl": motor_auswahl,
                "Beschleunigungsleistungen": motor_leistung_beschl_summe,
                "Beharrungsleistung": motor_leistung_beharrung,
                "Motorleistung_leer": motor_leistung_leer,
                "Beschleunigungsleistungen_leer": motor_leistung_beschl_leer,
                "Beharrungsleistung_leer": motor_leistung_beharrung_leer
    }

def mechleistunghubwerk(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, geschwindigkeit_mmin, 
                         beschleunigung_m_ss, wirkungsgrad_seiltrieb, wirkungsgrad_getriebestufe, 
                        drehzahl, getriebestufen, motor_anzahl, massentraegheit):
    
    """ Berechnen der mechanischen Leistungswerte des Hubwerkes. Ausgegeben wird ein Dict mit folgenden Keys:
        Motorauswahl
        Gesamtleistung voll
        Gesamtbeschleunigungsleistung voll
        Beharrungsleistung voll
        Gesamtleistung leer
        Gesamtbeschleunigungsleistung leer
        Beharrungleistung leer
    """

    #  Grundlegende Berechnungen
    geschwindigkeit_ms = geschwindigkeit_mmin / 60
    wirkungsgrad_gesamt = wirkungsgrad_getriebestufe**getriebestufen * wirkungsgrad_seiltrieb

    # Berechnungen bei vollem Greifer (Hauptsächlich Heben)
    voll_gewicht_greifer = (greifer_volumen * muell_dichte) + gewicht_greifer_leer
    voll_gewicht_gesamt = gewicht_seile + voll_gewicht_greifer

    voll_motor_leistung_beharrung = voll_gewicht_gesamt * 9.81 * geschwindigkeit_ms * wirkungsgrad_gesamt
    voll_motor_leistung_beschl_translatorisch = voll_gewicht_gesamt * geschwindigkeit_ms**2 / beschleunigung_m_ss / wirkungsgrad_gesamt
    voll_motor_leistung_beschl_rotatorisch = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / beschleunigung_m_ss

    voll_motor_leistung_beschl_gesamt = voll_motor_leistung_beschl_translatorisch + voll_motor_leistung_beschl_rotatorisch
    voll_motor_leistung_gesamt = voll_motor_leistung_beharrung + voll_motor_leistung_beschl_rotatorisch + voll_motor_leistung_beschl_translatorisch

    motor_leistung_min = voll_motor_leistung_beharrung / motor_anzahl
    
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > (motor_leistung_min / 1000): 
            motor_auswahl = leistung
            break

    # Berechnung bei leerem Greifer (Hauptsächlich Senken)
    leer_gewicht_greifer = gewicht_greifer_leer
    leer_gewicht_gesamt = gewicht_seile + leer_gewicht_greifer

    leer_motor_leistung_beharrung = leer_gewicht_gesamt * 9.81 * geschwindigkeit_ms * wirkungsgrad_gesamt
    leer_motor_leistung_beschl_translatorisch = leer_gewicht_gesamt * geschwindigkeit_ms**2 / beschleunigung_m_ss / wirkungsgrad_gesamt
    leer_motor_leistung_beschl_rotatorisch = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / beschleunigung_m_ss

    leer_motor_leistung_beschl_gesamt = leer_motor_leistung_beschl_translatorisch + leer_motor_leistung_beschl_rotatorisch
    leer_motor_leistung_gesamt = leer_motor_leistung_beharrung + leer_motor_leistung_beschl_rotatorisch + leer_motor_leistung_beschl_translatorisch

    return {
        "Motorauswahl": motor_auswahl,
        "Gesamtleistung voll": voll_motor_leistung_gesamt,
        "Gesamtbeschleunigungsleistung voll": voll_motor_leistung_beschl_gesamt,
        "Beharrungsleistung voll": voll_motor_leistung_beharrung,
        "Gesamtleistung leer": leer_motor_leistung_gesamt,
        "Gesamtbeschleunigungsleistung leer": leer_motor_leistung_beschl_gesamt,
        "Beharrungsleistung leer": leer_motor_leistung_beharrung,
    }

def greiferhydraulik(leergewicht=3050,betriebsdruck=170, volumenstrom=66, wirkungsgrad_greifer=0.9, anteil_bewegte_masse=0.15, 
                     geschwindigkeit_m_pro_min=100, beschleunigung_m_pro_s2=0.5):

    """ Berechnung der benötigten elektrischen und mechanischen Leistung des Hydraulikgreifers
        Ausgegeben wird ein Dictionary mit folgenden Keys:
        
        Leistung Beharrung
        Leistung Beschleunigung"""
    leistung_hydraulisch_beharrung = betriebsdruck * volumenstrom / 600
    leistung_hydraulisch_beschleunigung = leergewicht * anteil_bewegte_masse * geschwindigkeit_m_pro_min * beschleunigung_m_pro_s2

    return { 
        "Leistung Beharrung": leistung_hydraulisch_beharrung,
        "Leistung Beschleunigung": leistung_hydraulisch_beschleunigung
            }

def kranfahrt(gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, gewicht_kran, gewicht_seile, beschleunigung_mss,
               geschwindigkeit_mmin, drehzahl, massentraegheit, fahrwiderstand, motoranzahl, wirkungsgrad_getriebestufe, 
               getriebestufen, belastungsfaktor=1.5):
    
    """ 
        Funktion berechnet die mech Leistung der Kranfahrt und gibt die Mindestleistung und den nächstgrößeren Motor aus.
        Ebenfalls wird die Summe der Beschleunigungsleistungen ausgegeben (Ohne weitere Berechnung, wie aufteilung auf Motoren etc.)

        Ausgegeben wird ein Dict mit folgenden Keys:
        Mindestleistung
        Motorauswahl
        Beschleunigungsleistungen
    """
    
    gewicht_greifer_voll = (greifer_volumen * muell_dichte) + gewicht_greifer_leer
    gewicht_gesamt = gewicht_greifer_voll + gewicht_katze + gewicht_kran + gewicht_seile
    geschwindigkeit_ms = geschwindigkeit_mmin / 60
    wirkungsgrad_getriebe = wirkungsgrad_getriebestufe**getriebestufen

    motor_leistung_beharrung = gewicht_gesamt * fahrwiderstand * 9.81 * geschwindigkeit_ms / wirkungsgrad_getriebe / 1000
    motor_leistung_beschl_translatorisch = gewicht_gesamt * beschleunigung_mss * geschwindigkeit_ms / wirkungsgrad_getriebe
    motor_leistung_beschl_rotation = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / (geschwindigkeit_ms/beschleunigung_mss)

    motor_leistung_min = (motor_leistung_beharrung + motor_leistung_beschl_rotation + motor_leistung_beschl_translatorisch) \
                            / belastungsfaktor / motoranzahl
    
    motor_leistung_beschl_gesamt = motor_leistung_beschl_translatorisch + motor_leistung_beschl_rotation
    
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > (motor_leistung_min/1000): 
            motor_auswahl = leistung
            break

    gewicht_gesamt_leer = gewicht_greifer_leer + gewicht_katze + gewicht_kran + gewicht_seile
    motor_leistung_beharrung_leer = gewicht_gesamt_leer * fahrwiderstand * 9.81 * geschwindigkeit_ms / wirkungsgrad_getriebe / 1000
    motor_leistung_beschl_translatorisch_leer = gewicht_gesamt_leer * beschleunigung_mss * geschwindigkeit_ms / wirkungsgrad_getriebe
    motor_leistung_beschl_rotation_leer = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / (geschwindigkeit_ms/beschleunigung_mss)

    motor_leistung_leer = (motor_leistung_beharrung_leer + motor_leistung_beschl_rotation_leer + motor_leistung_beschl_translatorisch_leer) \
                            / belastungsfaktor / motoranzahl
    
    motor_leistung_beschl_gesamt_leer = motor_leistung_beschl_translatorisch_leer + motor_leistung_beschl_rotation_leer
    return {
        "Mindestleistung" : motor_leistung_min,
        "Motorauswahl" : motor_auswahl,
        "Beschleunigungsleistungen": motor_leistung_beschl_gesamt,
        "Beharrungsleistung": motor_leistung_beharrung,
        "Motorleistung_leer": motor_leistung_leer,
        "Beschleunigungsleistungen_leer": motor_leistung_beschl_gesamt_leer,
        "Beharrungsleistung_leer": motor_leistung_beharrung_leer
    }

def mechleistunggreifervierseil(hubvorgang_beharrung, hubvorgang_beschl):
    """Die mechanische Leistungsberechnung des Greifers ergibt sich als Erfahrungswert aus einem Drittel des Hubvorganges
    Ausgegeben wird ein Dictionary mit den Key 'Beharrungsleistung' und 'Beschleunigungsleistung'
    """
    
    beharrung_greifer = hubvorgang_beharrung /3
    beschl_greifer = hubvorgang_beschl /3

    return {"Beharrungsleistung": beharrung_greifer,
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
    # Anlage
    anlage_anzahl_trichter = dict_anlage["anzahl_trichter"]
    anlage_verbrennung_trichter_kg = dict_anlage["verbrennung_trichter_kg"]
    anlage_muell_anlieferung_h_kg = dict_anlage["müll_anlieferung_h_kg"]
    anlage_müll_dichte_beschickung_kg_pro_m3 = dict_anlage["müll_dichte_beschickung_kg_pro_m3"]
    anlage_müll_dichte_anlieferung_kg_pro_m3 = dict_anlage["müll_dichte_anlieferung_kg_pro_m3"]
    anlage_energie_kosten = dict_anlage["energie_kosten"]
    anlage_müll_anlieferdauer = dict_anlage["müll_anlieferdauer"]

    # Greifer
    if dict_greifer["typ"] == "Vierseil-Greifer":
        greifer_leergewicht_kg = dict_greifer["leergewicht_kg"]
        greifer_volumen_m3 = dict_greifer["volumen_m3"]
        greifer_geschwindigkeit_m_pro_min = dict_greifer["geschwindigkeit_m_pro_min"]
        greifer_beschleunigung_m_pro_s2 = dict_greifer["beschleunigung_m_pro_s2"]
        greifer_typ = dict_greifer["typ"]
    elif dict_greifer["typ"] == "Hydraulikgreifer":
        greifer_leergewicht_kg = dict_greifer["leergewicht_kg"]
        greifer_volumen_m3 = dict_greifer["volumen_m3"]
        greifer_geschwindigkeit_m_pro_min = dict_greifer["geschwindigkeit_m_pro_min"]
        greifer_beschleunigung_m_pro_s2 = dict_greifer["beschleunigung_m_pro_s2"]
        greifer_typ = dict_greifer["typ"]
        greifer_motorleistung_kw = dict_greifer["motorleistung_kw"]
        greifer_wirkungsgrad_hydraulik = dict_greifer["wirkungsgrad_hydraulik"]
        greifer_volumenstrom_l_pro_min = dict_greifer["volumenstrom_l_pro_min"]
        greifer_betriebsdruck_bar = dict_greifer["betriebsdruck_bar"]

    # Kranmechanik
    # Hubwerk
    hubwerk_seilgewicht_kg = dict_hub["seilgewicht_kg"]
    hubwerk_hub_geschwindigkeit_m_pro_min = dict_hub["hub_geschwindigkeit_m_pro_min"]
    hubwerk_hub_beschleunigung_m_pro_s2 = dict_hub["hub_beschleunigung_m_pro_s2"]
    hubwerk_motordrehzahl_1_pro_min = dict_hub["motordrehzahl_1_pro_min"]
    hubwerk_massenträgheit_kgm2 = dict_hub["massenträgheit_kgm2"]
    hubwerk_anzahl_motoren = dict_hub["anzahl_motoren"]
    hubwerk_wirkungsgrad_getriebe = dict_hub["wirkungsgrad_getriebe"]
    hubwerk_wirkungsgrad_seiltrieb = dict_hub["wirkungsgrad_seiltrieb"]
    hubwerk_getriebestufen = dict_hub["getriebestufen"]
    hubwerk_wirkungsgrad_motor_hub = dict_hub["wirkungsgrad_motor_hub"]
    # Katzfahrwerk
    katze_gewicht_kg = dict_katz["gewicht_kg"]
    katze_geschwindigkeit_m_pro_min = dict_katz["geschwindigkeit_m_pro_min"]
    katze_beschleunigung_m_pro_s2 = dict_katz["beschleunigung_m_pro_s2"]
    katze_motordrehzahl_1_pro_min = dict_katz["motordrehzahl_1_pro_min"]
    katze_massenträgheit_kgm2 = dict_katz["massenträgheit_kgm2"]
    katze_anzahl_motoren = dict_katz["anzahl_motoren"]
    katze_wirkungsgrad_getriebe = dict_katz["wirkungsgrad_getriebe"]
    katze_getriebestufen = dict_katz["getriebestufen"]
    katze_fahrwiderstand_kg_pro_t = dict_katz["fahrwiderstand_kg_pro_t"]
    katze_wirkungsgrad_motor_katze = dict_katz["wirkungsgrad_motor_katze"]
    # Kranfahrwerk
    kranfahrwerk_gewicht_kg = dict_kran["gewicht_kg"]
    kranfahrwerk_geschwindigkeit_m_pro_min = dict_kran["geschwindigkeit_m_pro_min"]
    kranfahrwerk_beschleunigung_m_pro_s2 = dict_kran["beschleunigung_m_pro_s2"]
    kranfahrwerk_motordrehzahl_1_pro_min = dict_kran["motordrehzahl_1_pro_min"]
    kranfahrwerk_massenträgheit_kgm2 = dict_kran["massenträgheit_kgm2"]
    kranfahrwerk_anzahl_motoren = dict_kran["anzahl_motoren"]
    kranfahrwerk_wirkungsgrad_getriebe = dict_kran["wirkungsgrad_getriebe"]
    kranfahrwerk_wirkungsgrad_vorgelege = dict_kran["wirkungsgrad_vorgelege"]
    kranfahrwerk_getriebestufen = dict_kran["getriebestufen"]
    kranfahrwerk_fahrwiderstand_kg_pro_t = dict_kran["fahrwiderstand_kg_pro_t"]
    kranfahrwerk_wirkungsgrad_motor_kran = dict_kran["wirkungsgrad_motor_kran"]
    
    # Wege
    wege_weg_hebensenken_m = dict_wege["weg_hebensenken_m"]
    wege_weg_katzfahrt_m = dict_wege["weg_katzfahrt_m"]
    wege_weg_kranfahrt_einlagern_m = dict_wege["weg_kranfahrt_einlagern_m"]
    wege_weg_oeffnen_schliessen_m = dict_wege["weg_oeffnen_schliessen_m"]
    wege_weg_trichter_m = dict_wege["weg_trichter_m"]
    # endregion

    # region Grundfunktionen
    df_muell = muellberechnung(anlage_anzahl_trichter, anlage_verbrennung_trichter_kg, anlage_muell_anlieferung_h_kg, greifer_volumen_m3,
                   anlage_müll_dichte_beschickung_kg_pro_m3, anlage_müll_dichte_anlieferung_kg_pro_m3, anlage_müll_anlieferdauer)
    df_spielzeiten_hub = spielzeitenberechnung(hubwerk_hub_geschwindigkeit_m_pro_min, hubwerk_hub_beschleunigung_m_pro_s2, wege_weg_hebensenken_m)
    df_spielzeiten_katze = spielzeitenberechnung(katze_geschwindigkeit_m_pro_min, katze_beschleunigung_m_pro_s2, wege_weg_katzfahrt_m)
    df_spielzeiten_kran_einlager = spielzeitenberechnung(kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_beschleunigung_m_pro_s2, wege_weg_kranfahrt_einlagern_m)
    df_kran_beschick_wege_mittel = sum(wege_weg_trichter_m.values()) / len(wege_weg_trichter_m)
    df_spielzeiten_kran_beschick = spielzeitenberechnung(kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_beschleunigung_m_pro_s2, df_kran_beschick_wege_mittel)
    df_spielzeiten_greifer = spielzeitenberechnung(greifer_geschwindigkeit_m_pro_min, greifer_beschleunigung_m_pro_s2, wege_weg_oeffnen_schliessen_m)
    # endregion

    # region grundlegende mechanische Leistungsberechnungen
    df_mechleist_katz_einlager = mechleistungkatzfahrt(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_anlieferung_kg_pro_m3, katze_gewicht_kg, 
                                                       katze_geschwindigkeit_m_pro_min, katze_beschleunigung_m_pro_s2, katze_motordrehzahl_1_pro_min, katze_fahrwiderstand_kg_pro_t,
                                                       katze_getriebestufen, katze_wirkungsgrad_getriebe, katze_massenträgheit_kgm2, motorzahl = katze_anzahl_motoren)
    df_mechleist_katz_beschick = mechleistungkatzfahrt(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_beschickung_kg_pro_m3, katze_gewicht_kg, 
                                                       katze_geschwindigkeit_m_pro_min, katze_beschleunigung_m_pro_s2, katze_motordrehzahl_1_pro_min, katze_fahrwiderstand_kg_pro_t,
                                                       katze_getriebestufen, katze_wirkungsgrad_getriebe, katze_massenträgheit_kgm2, motorzahl = katze_anzahl_motoren)
    df_mechleist_hub_einlager = mechleistunghubwerk(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_anlieferung_kg_pro_m3, hubwerk_hub_geschwindigkeit_m_pro_min, 
                                                    hubwerk_hub_beschleunigung_m_pro_s2, hubwerk_wirkungsgrad_seiltrieb, hubwerk_wirkungsgrad_getriebe, hubwerk_motordrehzahl_1_pro_min, hubwerk_getriebestufen, 
                                                    hubwerk_anzahl_motoren, hubwerk_massenträgheit_kgm2)
    df_mechleist_hub_beschick = mechleistunghubwerk(hubwerk_seilgewicht_kg, greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_beschickung_kg_pro_m3, hubwerk_hub_geschwindigkeit_m_pro_min, 
                                                    hubwerk_hub_beschleunigung_m_pro_s2, hubwerk_wirkungsgrad_seiltrieb, hubwerk_wirkungsgrad_getriebe, hubwerk_motordrehzahl_1_pro_min, hubwerk_getriebestufen, 
                                                    hubwerk_anzahl_motoren, hubwerk_massenträgheit_kgm2)
    df_mechleist_kran_einlager = kranfahrt(greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_anlieferung_kg_pro_m3, katze_gewicht_kg, kranfahrwerk_gewicht_kg, hubwerk_seilgewicht_kg, 
                                           kranfahrwerk_beschleunigung_m_pro_s2, kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_motordrehzahl_1_pro_min, kranfahrwerk_massenträgheit_kgm2,
                                           kranfahrwerk_fahrwiderstand_kg_pro_t, kranfahrwerk_anzahl_motoren, kranfahrwerk_wirkungsgrad_getriebe, kranfahrwerk_getriebestufen)
    df_mechleist_kran_beschick = kranfahrt(greifer_leergewicht_kg, greifer_volumen_m3, anlage_müll_dichte_beschickung_kg_pro_m3, katze_gewicht_kg, kranfahrwerk_gewicht_kg, hubwerk_seilgewicht_kg, 
                                           kranfahrwerk_beschleunigung_m_pro_s2, kranfahrwerk_geschwindigkeit_m_pro_min, kranfahrwerk_motordrehzahl_1_pro_min, kranfahrwerk_massenträgheit_kgm2,
                                           kranfahrwerk_fahrwiderstand_kg_pro_t, kranfahrwerk_anzahl_motoren, kranfahrwerk_wirkungsgrad_getriebe, kranfahrwerk_getriebestufen)
    
    if greifer_typ == "Vierseil-Greifer":
        df_mechleist_oeffnenschliessen_vierseil = mechleistunggreifervierseil(df_mechleist_hub_einlager["Beharrungsleistung voll"], hubwerk_hub_beschleunigung_m_pro_s2)
    elif greifer_typ == "Hydraulikgreifer":
        df_mechleist_oeffnenschliessen_hydraulik = greiferhydraulik(greifer_leergewicht_kg, greifer_betriebsdruck_bar, greifer_volumenstrom_l_pro_min, greifer_wirkungsgrad_hydraulik, greifer_geschwindigkeit_m_pro_min, greifer_beschleunigung_m_pro_s2)
    # endregion

    # region mechanische Energieberechnungen einzelne Vorgänge

    # region Katze

    df_mechenergie_katz_einlager_voll = (
        df_mechleist_katz_einlager["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]
        + df_mechleist_katz_einlager["Beharrungsleistung"] * df_spielzeiten_katze["Kontinuierliche Zeit"]
    )
    df_mechenergie_katz_einlager_leer = (
        df_mechleist_katz_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]
        + df_mechleist_katz_einlager["Beharrungsleistung_leer"] * df_spielzeiten_katze["Kontinuierliche Zeit"] 
    )
    df_mechenergie_katz_beschick_voll = (
        df_mechleist_katz_beschick["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]
        + df_mechleist_katz_beschick["Beharrungsleistung"] * df_spielzeiten_katze["Kontinuierliche Zeit"]
    )
    df_mechenergie_katz_beschick_leer = (
        df_mechleist_katz_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]
        + df_mechleist_katz_beschick["Beharrungsleistung_leer"] * df_spielzeiten_katze["Kontinuierliche Zeit"] 
    )
    #endregion Katze

    # region Hub

    df_mechenergie_hub_einlager_voll = (
        df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]
        + df_mechleist_hub_einlager["Beharrungsleistung voll"] * df_spielzeiten_hub["Kontinuierliche Zeit"]
    )
    df_mechenergie_hub_einlager_leer = (
        df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]
        + df_mechleist_hub_einlager["Beharrungsleistung leer"] * df_spielzeiten_hub["Kontinuierliche Zeit"]
    )
    df_mechenergie_hub_beschick_voll = (
        df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]
        + df_mechleist_hub_beschick["Beharrungsleistung voll"] * df_spielzeiten_hub["Kontinuierliche Zeit"]
    )
    df_mechenergie_hub_beschick_leer = (
        df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]
        + df_mechleist_hub_beschick["Beharrungsleistung leer"] * df_spielzeiten_hub["Kontinuierliche Zeit"]
    )
    # endregion Hub

    # region Kran

    df_mechenergie_kran_einlager_voll = (
        df_mechleist_kran_einlager["Beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]
        + df_mechleist_kran_einlager["Beharrungsleistung"] * df_spielzeiten_kran_einlager["Kontinuierliche Zeit"]
    )
    df_mechenergie_kran_einlager_leer = (
        df_mechleist_kran_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]
        + df_mechleist_kran_einlager["Beharrungsleistung_leer"] * df_spielzeiten_kran_einlager["Kontinuierliche Zeit"]
    )
    df_mechenergie_kran_beschick_voll = (
        df_mechleist_kran_beschick["Beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]
        + df_mechleist_kran_beschick["Beharrungsleistung"] * df_spielzeiten_kran_beschick["Kontinuierliche Zeit"]
    )
    df_mechenergie_kran_beschick_leer = (
        df_mechleist_kran_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]
        + df_mechleist_kran_beschick["Beharrungsleistung_leer"] * df_spielzeiten_kran_beschick["Kontinuierliche Zeit"]
    )
    # endregion Kran

    # region Greifer
    if greifer_typ == "Vierseil-Greifer":
        df_mechenergie_greifer_oeffnenschliessen_vierseil = (
                df_mechleist_oeffnenschliessen_vierseil["Beschleunigungsleistung"] * df_spielzeiten_greifer["Beschleunigungszeit"] 
                + df_mechleist_oeffnenschliessen_vierseil["Beharrungsleistung"] * df_spielzeiten_greifer["Kontinuierliche Zeit"] 
            )
        
    elif greifer_typ == "Hydraulikgreifer":
        df_mechenergie_greifer_oeffnenschliessen_hydraulik = (
            df_mechleist_oeffnenschliessen_hydraulik["Leistung Beschleunigung"] * df_spielzeiten_greifer["Beschleunigungszeit"] 
            + df_mechleist_oeffnenschliessen_hydraulik["Leistung Beharrung"] * df_spielzeiten_greifer["Kontinuierliche Zeit"] 
        )
    # endregion Greifer
    # endregion mechanische Energieberechnung

    # region Elektrische Energieberechnung

    # region el Energie Katze
    df_elenergie_katz_einlager_voll = {
        "Verbrauch": (
            df_mechenergie_katz_einlager_voll / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_einlager["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        ),
        "Rückspeisung": (
            (df_mechleist_katz_einlager["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        )
    }
    df_elenergie_katz_einlager_leer = {
        "Verbrauch": (
            df_mechenergie_katz_einlager_leer / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        ),
        "Rückspeisung": (
            (df_mechleist_katz_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        )
    }
    df_elenergie_katz_beschick_voll = {
        "Verbrauch": (
            df_mechenergie_katz_beschick_voll / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_beschick["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        ),
        "Rückspeisung": (
            (df_mechleist_katz_beschick["Beschleunigungsleistungen"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        )
    }
    df_elenergie_katz_beschick_leer = {
        "Verbrauch": (
            df_mechenergie_katz_beschick_leer / dict_katz["wirkungsgrad_motor_katze"]
            - (df_mechleist_katz_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        ),
        "Rückspeisung": (
            (df_mechleist_katz_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_katze["Beschleunigungszeit"]) / dict_katz["wirkungsgrad_motor_katze"]
            * dict_rueckspeisung["faktor katze"] * dict_rueckspeisung["FU-Wirkungsgrad katze"]
        )
    }
    # endregion el Energie Katze

    # region el Energie Hub

    df_elenergie_hub_einlager_voll = {
        "Verbrauch": (
            df_mechenergie_hub_einlager_voll / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        ),
        "Rückspeisung": (
            (df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
    }
    df_elenergie_hub_einlager_leer = {
        "Verbrauch": (
            df_mechenergie_hub_einlager_leer / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        ),
        "Rückspeisung": (
            (df_mechleist_hub_einlager["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
    }
    df_elenergie_hub_beschick_voll = {
        "Verbrauch": (
            df_mechenergie_hub_beschick_voll / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        ),
        "Rückspeisung": (
            (df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung voll"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
    }
    df_elenergie_hub_beschick_leer = {
        "Verbrauch": (
            df_mechenergie_hub_beschick_leer / dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        ),
        "Rückspeisung": (
            (df_mechleist_hub_beschick["Gesamtbeschleunigungsleistung leer"] * df_spielzeiten_hub["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
        }
    # endregion el Energie Hub

    # region el Energie Kran

    df_elenergie_kran_einlager_voll = {
        "Verbrauch": (
            df_mechenergie_kran_einlager_voll / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_einlager["Beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        ),
        "Rückspeisung": (
            (df_mechleist_kran_einlager["Beschleunigungsleistungen"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        )
    }
    df_elenergie_kran_einlager_leer = {
        "Verbrauch": (
            df_mechenergie_kran_einlager_leer / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        ),
        "Rückspeisung": (
            (df_mechleist_kran_einlager["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_einlager["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        )
    }
    df_elenergie_kran_beschick_voll = {
        "Verbrauch": (
            df_mechenergie_kran_beschick_voll / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_beschick["Beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        ),
        "Rückspeisung": (
            (df_mechleist_kran_beschick["Beschleunigungsleistungen"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        )
    }
    df_elenergie_kran_beschick_leer = {
        "Verbrauch": (
            df_mechenergie_kran_beschick_leer / dict_kran["wirkungsgrad_motor_kran"]
            - (df_mechleist_kran_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        ),
        "Rückspeisung": (
            (df_mechleist_kran_beschick["Beschleunigungsleistungen_leer"] * df_spielzeiten_kran_beschick["Beschleunigungszeit"]) /dict_kran["wirkungsgrad_motor_kran"]
            * dict_rueckspeisung["faktor kran"] * dict_rueckspeisung["FU-Wirkungsgrad kran"]
        )
    }
    # endregion el Energie Kran

    # region el Energie Greifer

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_greifer_vierseil_oeffnen = (
            -1 * (df_mechenergie_greifer_oeffnenschliessen_vierseil * dict_hub["wirkungsgrad_motor_hub"]) /dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
        df_elenergie_greifer_vierseil_schliessen = (
            df_mechenergie_greifer_oeffnenschliessen_vierseil * dict_hub["wirkungsgrad_motor_hub"]
            - (df_mechleist_oeffnenschliessen_vierseil["Beschleunigungsleistung"] * df_spielzeiten_greifer["Beschleunigungszeit"]) / dict_hub["wirkungsgrad_motor_hub"]
            * dict_rueckspeisung["faktor hub"] * dict_rueckspeisung["FU-Wirkungsgrad hub"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        df_elenergie_greifer_hydraulik_oeffnenschliessen = (
            df_mechenergie_greifer_oeffnenschliessen_hydraulik * dict_greifer["wirkungsgrad_hydraulik"]
        )
    # endregion el Energie Greifer
    
    # endregion Elektrische Energieberechnung

    # region Tagesberechnungen Einlagerung (Greifer schließen -> Heben -> Katzfahrt -> Kranfahrt -> Senken -> Greifer öffnen -> Heben -> Katzfahrt -> Kranfahrt -> Senken)
    
    df_zyklen_einlager_d = df_muell["Anzahl Zyklen Mülleinlagerung / d"]

    # Verbrauch

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_einlager_verbrauch_zyklus = (
            df_elenergie_greifer_vierseil_schliessen + 
            df_elenergie_hub_einlager_voll["Verbrauch"] + 
            df_elenergie_katz_einlager_voll["Verbrauch"] + 
            df_elenergie_kran_einlager_voll["Verbrauch"] + 
            df_elenergie_hub_einlager_voll["Verbrauch"] +
            df_elenergie_greifer_vierseil_oeffnen +
            df_elenergie_hub_einlager_leer["Verbrauch"] +
            df_elenergie_kran_einlager_leer["Verbrauch"] +
            df_elenergie_katz_einlager_leer["Verbrauch"] +
            df_elenergie_hub_einlager_leer["Verbrauch"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        df_elenergie_einlager_verbrauch_zyklus = (
            df_elenergie_greifer_hydraulik_oeffnenschliessen + 
            df_elenergie_hub_einlager_voll["Verbrauch"] + 
            df_elenergie_katz_einlager_voll["Verbrauch"] + 
            df_elenergie_kran_einlager_voll["Verbrauch"] + 
            df_elenergie_hub_einlager_voll["Verbrauch"] +
            df_elenergie_greifer_hydraulik_oeffnenschliessen +
            df_elenergie_hub_einlager_leer["Verbrauch"] +
            df_elenergie_kran_einlager_leer["Verbrauch"] +
            df_elenergie_katz_einlager_leer["Verbrauch"] +
            df_elenergie_hub_einlager_leer["Verbrauch"]
        )
    df_elenergie_einlager_verbrauch_d = df_elenergie_einlager_verbrauch_zyklus * df_zyklen_einlager_d
    
    # Rückspeisung

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_einlager_rueckspeisung_zyklus = (
            df_elenergie_hub_einlager_voll["Rückspeisung"] + 
            df_elenergie_katz_einlager_voll["Rückspeisung"] + 
            df_elenergie_kran_einlager_voll["Rückspeisung"] + 
            df_elenergie_hub_einlager_voll["Rückspeisung"] +
            df_elenergie_hub_einlager_leer["Rückspeisung"] +
            df_elenergie_kran_einlager_leer["Rückspeisung"] +
            df_elenergie_katz_einlager_leer["Rückspeisung"] +
            df_elenergie_hub_einlager_leer["Rückspeisung"]
        )
    elif greifer_typ == "Hydraulikgreifer":
        df_elenergie_einlager_rueckspeisung_zyklus = (
            df_elenergie_hub_einlager_voll["Rückspeisung"] + 
            df_elenergie_katz_einlager_voll["Rückspeisung"] + 
            df_elenergie_kran_einlager_voll["Rückspeisung"] + 
            df_elenergie_hub_einlager_voll["Rückspeisung"] +
            df_elenergie_hub_einlager_leer["Rückspeisung"] +
            df_elenergie_kran_einlager_leer["Rückspeisung"] +
            df_elenergie_katz_einlager_leer["Rückspeisung"] +
            df_elenergie_hub_einlager_leer["Rückspeisung"]
        )
    df_elenergie_einlager_rueckspeisung_d = df_elenergie_einlager_rueckspeisung_zyklus * df_zyklen_einlager_d

    # endregion Tagesberechnung Einlagerung

    # region Tagesberechnungen Beschickung (Greifer schließen -> Heben -> Kranfahrt -> Katzfahrt -> Greifer öffnen -> Katzfahrt -> Kranfahrt -> Senken)

    df_zyklen_beschick_d = df_muell["Anzahl Zyklen Trichterbeschickung gesamt / d"]

    # Verbrauch

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_beschick_verbrauch_zyklus = (
            df_elenergie_greifer_vierseil_schliessen + 
            df_elenergie_hub_beschick_voll["Verbrauch"] +
            df_elenergie_kran_beschick_voll["Verbrauch"] +
            df_elenergie_katz_beschick_voll["Verbrauch"] +
            df_elenergie_greifer_vierseil_oeffnen +
            df_elenergie_katz_beschick_leer["Verbrauch"] +
            df_elenergie_kran_beschick_voll["Verbrauch"] +
            df_elenergie_hub_beschick_leer["Verbrauch"]
        )
    if greifer_typ == "Hydraulikgreifer":
        df_elenergie_beschick_verbrauch_zyklus = (
            df_elenergie_greifer_hydraulik_oeffnenschliessen + 
            df_elenergie_hub_beschick_voll["Verbrauch"] +
            df_elenergie_kran_beschick_voll["Verbrauch"] +
            df_elenergie_katz_beschick_voll["Verbrauch"] +
            df_elenergie_greifer_hydraulik_oeffnenschliessen +
            df_elenergie_katz_beschick_leer["Verbrauch"] +
            df_elenergie_kran_beschick_voll["Verbrauch"] +
            df_elenergie_hub_beschick_leer["Verbrauch"]
        )
    df_elenergie_beschick_verbrauch_d = df_elenergie_beschick_verbrauch_zyklus * df_zyklen_beschick_d

    # Rückspeisung 

    if greifer_typ == "Vierseil-Greifer":
        df_elenergie_beschick_rueckspeisung_zyklus = (
            df_elenergie_hub_beschick_voll["Rückspeisung"] +
            df_elenergie_kran_beschick_voll["Rückspeisung"] +
            df_elenergie_katz_beschick_voll["Rückspeisung"] +
            df_elenergie_katz_beschick_leer["Rückspeisung"] +
            df_elenergie_kran_beschick_voll["Rückspeisung"] +
            df_elenergie_hub_beschick_leer["Rückspeisung"]
        )
    if greifer_typ == "Hydraulikgreifer":
        df_elenergie_beschick_rueckspeisung_zyklus = (
            df_elenergie_hub_beschick_voll["Rückspeisung"] +
            df_elenergie_kran_beschick_voll["Rückspeisung"] +
            df_elenergie_katz_beschick_voll["Rückspeisung"] +
            df_elenergie_katz_beschick_leer["Rückspeisung"] +
            df_elenergie_kran_beschick_voll["Rückspeisung"] +
            df_elenergie_hub_beschick_leer["Rückspeisung"]
        )
    df_elenergie_beschick_rueckspeisung_d = df_elenergie_beschick_rueckspeisung_zyklus * df_zyklen_beschick_d

    # endregion Tagesberechnung Beschickung

    # Gesamtenergie in kWh

    df_elenergie_verbrauch_kwh      = (df_elenergie_beschick_verbrauch_d + df_elenergie_einlager_verbrauch_d) / 3600
    df_elenergie_rueckspeisung_kwh  = (df_elenergie_beschick_rueckspeisung_d + df_elenergie_einlager_rueckspeisung_d) / 3600

    # region Tagesberechnungen Energiekosten nach Region

    df_elenergie_kosten_eur = df_elenergie_verbrauch_kwh * anlage_energie_kosten / 100  # Euro für gesamtverbrauch


    return {
        "Verbrauch": df_elenergie_verbrauch_kwh,
        "Rückspeisung": df_elenergie_rueckspeisung_kwh,
        "Kosten": df_elenergie_kosten_eur,
        #"CO2": pass,
    }

