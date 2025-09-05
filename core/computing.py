
## Hier werden die Berechnungen in Funktionen geschrieben, welche dictionarys ausgeben, sodass man über den key
## immer genau ausrechnen kann, was man haben möchte

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
        müll_dichte_greifer, anlieferdauer
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
    müll_einlagerung_prozyklus = greifer_volumen * müll_dichte_greifer
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

