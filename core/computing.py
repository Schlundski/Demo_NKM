
## Hier werden die Berechnungen in Funktionen geschrieben, welche dictionarys ausgeben, sodass man über den key
## immer genau ausrechnen kann, was man haben möchte
import numpy
# from config.standards import Motorleistungen # wird erst beim Einsatz benutzt, um daten und funktionen zu trennen

def spielzeitenberechnung(geschwindigkeit_mmin, beschleunigung_mss, weg):

    """ Berechnung der Spielzeiten durch die gegebenen Argumente.

    Ausgegeben wird über ein Dictionary die values über folgende keys:

        "Beschleunigungszeit"
        "Beschleunigungsweg"
        "Kontinuierliche Zeit"
        "Kontinuierlicher Weg"
        "Summe der Zeit"

        """

    geschwindigkeit_ms = float(geschwindigkeit_mmin) / 60
    beschleunigung_zeit = geschwindigkeit_ms / beschleunigung_mss
    beschleunigung_weg = (beschleunigung_zeit**2) * (beschleunigung_mss / 2)
    kontinuierlich_weg = weg - (2* beschleunigung_weg)
    kontinuierlich_zeit = kontinuierlich_weg / geschwindigkeit_ms
    summe_zeit = kontinuierlich_zeit + (2* beschleunigung_zeit)

    return {
        "Beschleunigungszeit": beschleunigung_zeit, 
        "Beschleunigungsweg": beschleunigung_weg,
        "Kontinuierliche Zeit": kontinuierlich_zeit,
        "Kontinuierlicher Weg": kontinuierlich_weg,
        "Summe der Zeit": summe_zeit
        }

def müllberechnung(
        anzahl_trichter, verbrennung_je_trichter, anliefermenge_stunde, greifer_volumen,müll_dichte_beschickung, 
        müll_dichte_einlagerung, anlieferdauer
        ):
    
    """ Alle Berechnungen zum Thema Müll
    
    Ausgegeben wird ein Dictionary mit values zu folgenden keys:

        "Gesamter zu transportierender Müll / h"
        "Mülleinlagerung Pro Zyklus"
        "Anzahl Zyklen Mülleinlagerung / h"
        "Anzahl Zyklen Mülleinlagerung / d"
        "Trichterbeschickugngsmüll / Zyklus"
        "Anzahl Zyklen Trichterbeschickung / h"
        "Anzahl Zyklen Trichterbeschickung / d"
        "Anzahl Zyklen Trichterbeschickung gesamt / d"
    
    """

    müll_gesamt_proh = (anzahl_trichter * verbrennung_je_trichter) + anliefermenge_stunde
    müll_einlagerung_prozyklus = greifer_volumen * müll_dichte_einlagerung
    anzahl_zyklen_mülleinlagerung_proh = anliefermenge_stunde / müll_einlagerung_prozyklus
    anzahl_zyklen_mülleinlagerung_prod = anzahl_zyklen_mülleinlagerung_proh * anlieferdauer
    beschickung_prozyklus = müll_dichte_beschickung * greifer_volumen
    anzahl_zyklen_beschickung_proh = verbrennung_je_trichter / beschickung_prozyklus
    anzahl_zyklen_beschickung_prod = anzahl_zyklen_beschickung_proh * 24
    anzahl_zyklen_beschickung_gesamt_prod = anzahl_zyklen_beschickung_prod * anzahl_trichter

    return {
        "Gesamter zu transportierender Müll / h": müll_gesamt_proh,
        "Mülleinlagerung Pro Zyklus": müll_einlagerung_prozyklus,
        "Anzahl Zyklen Mülleinlagerung / h": anzahl_zyklen_mülleinlagerung_proh,
        "Anzahl Zyklen Mülleinlagerung / d": anzahl_zyklen_mülleinlagerung_prod,
        "Trichterbeschickugngsmüll / Zyklus": beschickung_prozyklus,
        "Anzahl Zyklen Trichterbeschickung / h": anzahl_zyklen_beschickung_proh,
        "Anzahl Zyklen Trichterbeschickung / d": anzahl_zyklen_beschickung_prod,
        "Anzahl Zyklen Trichterbeschickung gesamt / d": anzahl_zyklen_beschickung_gesamt_prod
    }

def mechleistungkatzfahrt(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, geschwindigkeit_mmin, beschleunigung_zeit_s, drehzahl=0, 
                          fahrwerkwiderstand=9.0, getriebestufen=3, wirkungsgrad_getriebestufe=0.980, massentraegheit=0.01, 
                          belastungsfaktor=1.55, motorzahl=1):
    
    """ Funktion zur Berechnung der mech Leistung der Katzfahrt
    Ausgegeben wird in Dict mit folgenden keys:
    Mindestmotorleistung
    Motorauswahl
    Beschleunigungsleistungen
    """

    Motorleistungen = [
    0.06, 0.09, 0.12, 0.18, 0.25, 0.37, 0.55, 0.75,
    1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11, 15, 18.5,
    22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200,
    250, 315, 355, 400, 450, 500, 560
]

    gewicht_greifer_voll = (greifer_volumen * muell_dichte) + gewicht_greifer_leer
    geschwindigkeit_ms = float(geschwindigkeit_mmin) / 60
    if drehzahl == 0: drehzahl = (geschwindigkeit_ms * 60 * 30) / (numpy.pi * 0.25)
    wirkungsgrad_getriebe = wirkungsgrad_getriebestufe ** getriebestufen
    gewicht_gesamt = gewicht_greifer_voll + gewicht_katze + gewicht_seile

    motor_leistung_beharrung = fahrwerkwiderstand * gewicht_gesamt * 9.81 * geschwindigkeit_ms / wirkungsgrad_getriebe / 1000
    motor_leistung_beschl_translatorisch = gewicht_gesamt * geschwindigkeit_ms**2 / beschleunigung_zeit_s / wirkungsgrad_getriebe
    motor_leistung_beschl_rotierend = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / beschleunigung_zeit_s

    motor_leistung_min = (motor_leistung_beharrung + motor_leistung_beschl_translatorisch + motor_leistung_beschl_rotierend) / motorzahl / belastungsfaktor
    
    motor_auswahl = 0 # variableninitialisierung
    for leistung in Motorleistungen:
        if leistung > (motor_leistung_min*1.1): 
            motor_auswahl = leistung
            break

    motor_leistung_beschl_summe = motor_leistung_beschl_translatorisch + motor_leistung_beschl_rotierend

    return {
                "Mindestmotorleistung": motor_leistung_min,
                "Motorauswahl": motor_auswahl,
                "Beschleunigungsleistungen": motor_leistung_beschl_summe
    }

def mechleistunghubwerk(gewicht_seile, gewicht_greifer_leer, greifer_volumen, muell_dichte, geschwindigkeit_mmin, 
                        beschleunigung_mss, beschleunigung_zeit_s, wirkungsgrad_seiltrieb, wirkungsgrad_getriebestufe, 
                        drehzahl, getriebestufen, motor_anzahl, massentraegheit):
    

    gewicht_greifer_voll = (greifer_volumen * muell_dichte) + gewicht_greifer_leer
    geschwindigkeit_ms = geschwindigkeit_mmin / 60
    gewicht_gesamt = gewicht_seile + gewicht_greifer_voll
    wirkungsgrad_gesamt = wirkungsgrad_getriebestufe**getriebestufen * wirkungsgrad_seiltrieb

    motor_leistung_beharrung = gewicht_gesamt * 9.81 * geschwindigkeit_ms * wirkungsgrad_gesamt / motor_anzahl
    motor_leistung_beschl_translatorisch = gewicht_gesamt * geschwindigkeit_ms**2 / beschleunigung_zeit_s / wirkungsgrad_gesamt
    motor_leistung_beschl_rotatorisch = numpy.pi * drehzahl**2 * massentraegheit / 30 / 9550 / beschleunigung_zeit_s

    motor_leistung_gesamt = motor_leistung_beharrung + motor_leistung_beschl_rotatorisch + motor_leistung_beschl_translatorisch
    # Wird Gesamtleistung oder Beharrungsleistung verwendet? Laut Excel ist es Beharrungsleistung

def greiferhydraulik(betriebsdruck=170, volumenstrom=66, wirkungsgrad_greifer=0.9):

    leistung_hydraulisch = betriebsdruck * volumenstrom / 600
    leistung_elektrisch = leistung_hydraulisch * wirkungsgrad_greifer

    return { "Hydraulische Leistung": leistung_hydraulisch, "Elektrische Leistung": leistung_elektrisch}

def kranfahrt(gewicht_greifer_leer, greifer_volumen, muell_dichte, gewicht_katze, gewicht_kran, gewicht_seile, beschleunigung_mss,
               geschwindigkeit_mmin, drehzahl, massentraegheit, fahrwiderstand, motoranzahl, wirkungsgrad_getriebestufe, 
               getriebestufen, belastungsfaktor):
    
    """ 
        Funktion berechnet die mech Leistung der Kranfahrt und gibt die Mindestleistung und den nächstgrößeren Motor aus.
        Ebenfalls wird die Summe der Beschleunigungsleistungen ausgegeben (Ohne weitere Berechnung, wie aufteilung auf Motoren etc.)

        Ausgegeben wird ein Dict mit folgenden Keys:
        Mindestleistung
        Motorauswahl
        Beschleunigungsleistungen
    """

    Motorleistungen = [
    0.06, 0.09, 0.12, 0.18, 0.25, 0.37, 0.55, 0.75,
    1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11, 15, 18.5,
    22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200,
    250, 315, 355, 400, 450, 500, 560
    ]
    
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
        if leistung > motor_leistung_min: 
            motor_auswahl = leistung
            break

    return {
        "Mindestleistung" : motor_leistung_min,
        "Motorauswahl" : motor_auswahl,
        "Beschleunigungsleistungen": motor_leistung_beschl_gesamt
    }
