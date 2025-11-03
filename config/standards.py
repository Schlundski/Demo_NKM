STANDARDWERTE = {
    "Greifer": 
    {
        "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        {
            "Leergewicht in Mg" : 3.05,
            "Motorleistung in kW"   : 18.8,
            "Greifervolumen in m³"     : 2.75,
            "Greiferart": "Hydraulikgreifer"
        },
        "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316":
        {
            "Leergewicht in Mg": 3.8,
            "Greifervolumen": 4.0,
            "Greiferart": "Vierseil-Greifer"
        }
    },
    "Müll": # Es handelt sich um die AVG Köln Werte des RMB
    {
            "Müll Gesamtmenge im Jahr in t": 760000,
            "Müll Anliefermenge in der Stunde": 235,
            "Müll Anlieferdauer in Stunden": 12,
            "Müll Dichte Einlagerung in t/m³": 0.7,
            "Müll Dichte Beschickung in t/m³": 0.8
    },  
    "Anlage":
    {
        "Anzahl Kräne": 2,
        "Anzahl Trichter": 4,
        "Verbrennung je Trichter": 21.2, 
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
        "Heben/Senken in m": 25,
        "Katzfahrt": 10,
        "Kranfahrt Einlagern": 35,
        "Öffnen/Schließen": 11,
        "Trichterweg 1": 10,
        "Trichterweg 2": 25,
        "Trichterweg 3": 40,
        "Trichterweg 4": 55,
    }
}

Motorleistungen = {
    0.06, 0.09, 0.12, 0.18, 0.25, 0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 
    110, 132, 160, 200, 250, 315, 335, 400, 450, 560
    }
# Daten sind aus IEC 60072.1 entnommen (Table 6 "Preferred rated output values")