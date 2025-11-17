STANDARDWERTE = {
    "Anlage":
    {
        "Anzahl Kräne": 2,
        "Anzahl Trichter": 4,
        "Verbrennung je Trichter": 21.2,
        "Standort": "Deutschland",
    },

    "Greifer": 
    {
        "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        {
            "Leergewicht" : 3.05,
            "Motorleistung"   : 18.8,
            "Greifervolumen"     : 2.75,
            "Wirkungsgrad" : 0.9,
            "Volumenstrom" : 66.0,
            "Betriebsdruck" : 170,
            "Greifgeschwindigkeit" : 100.0,
            "Greifbeschleunigung" : 0.5,
            "Greiferart": "Hydraulikgreifer",
            "Oeffnungszeit": 6,
            "Schliesszeit": 10.5,
            
        },
        "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316":
        {
            "Leergewicht": 3.8,
            "Greifervolumen": 4.0,
            "Greifgeschwindigkeit" : 100.0,
            "Greifbeschleunigung" : 0.5,
            "Greiferart": "Vierseil-Greifer",
            "Oeffnungszeit": 6,
            "Schliesszeit": 10.5,
        }
    },
    
    "Müll": # Es handelt sich um die AVG Köln Werte des RMB
    {
            "Müll Gesamtmenge im Jahr[t]": 760000,
            "Müll Anliefermenge in der Stunde[t]": 235,
            "Müll Anlieferdauer Stunden[h]": 12,
            "Müll Dichte Einlagerung[t/m³]": 0.7,
            "Müll Dichte Beschickung[t/m³]": 0.8
    },

    "Geschwindigkeiten": {
        "heben_senken_m_min": 100.0,
        "katzfahrt_m_min": 85.0,
        "kranfahrt_m_min": 85.0,
        "oeffnen_schliessen_einh": 100.0,
    },

    "Beschleunigungen": {
        "heben_senken_m_s2": 0.5,
        "katzfahrt_m_s2": 0.22,
        "kranfahrt_m_s2": 0.22,
        "oeffnen_schliessen_m_s2": 0.5,
    },

    "Referenzwege":
    {
        "Heben/Senken": 25,
        "Katzfahrt": 10,
        "Kranfahrt Einlagern": 35,
        "Öffnen/Schließen": 11,
        "Trichterweg 1": 10,
        "Trichterweg 2": 25,
        "Trichterweg 3": 40,
        "Trichterweg 4": 55,
        "Trichterweg 5": 70,
        "Trichterweg 6": 85,
        "Trichterweg 7": 100
    },

    "Hubwerk": {#Werte aus 831022M.010000-8_Motorgreifer
        "Seilgewicht": 200.0,
        "Geschwindigkeit": 80.0,
        "Beschleunigung": 0.67,
        "Motordrehzahl": 1488,
        "Massentraegheit": 5.3,
        "AnzahlMotoren": 1,
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradSeiltrieb": 0.99,
        "Getriebestufen": 3,
        "WirkungsgradMotor": 0.967
    },

    "Katze": {#Werte aus 831022M.010000-8_Motorgreifer
        "Gewicht": 12300.0,
        "Geschwindigkeit": 60.0,
        "Beschleunigung": 0.25,
        "Motordrehzahl": 1456,
        "Massentraegheit": 0.008,
        "AnzahlMotoren": 2,
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradMotor": 0.896,
        "Getriebestufen": 2,
        "Fahrwiderstand": 8.5,      
    },

    "Kran": {#Werte aus 831022M.010000-8_Motorgreifer
        "Gewicht": 30200.0,
        "Geschwindigkeit": 80.0,
        "Beschleunigung": 0.3,
        "Motordrehzahl": 1461,
        "Massentraegheit": 0.098,
        "AnzahlMotoren": 4,
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradVorgelege": 1.0,
        "Getriebestufen": 3,
        "Fahrwiderstand": 7,  
        "WirkungsgradMotor": 0.904 
    }
}

Motorleistungen = [
    0.06, 0.09, 0.12, 0.18, 0.25, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 
    110, 132, 160, 200, 250, 315, 335, 400, 450, 560
]
# Daten sind aus IEC 60072.1 entnommen (Table 6 "Preferred rated output values")

#Aliase
hydr = STANDARDWERTE["Greifer"]["Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1"]
viers = STANDARDWERTE["Greifer"]["Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316"]
hubw = STANDARDWERTE["Hubwerk"]
katze = STANDARDWERTE["Katze"]
kran = STANDARDWERTE["Kran"]