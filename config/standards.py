STANDARDWERTE = {
    "Anlage":
    {
        "Anzahl Kräne": 2,                      #stk
        "Anzahl Trichter": 4,                   #Stk
        "Verbrennung je Trichter": 21200,       #kg
        "Standort": "Deutschland",
    },

    "Greifer": 
    {
        "Motor-Mehrschalengreifer MRS Greifer 2-12-31667-1":
        {
            "Leergewicht" : 3050,               #kg
            "Motorleistung"   : 18.8,           #kW
            "Greifervolumen"     : 2.75,        #m³
            "Wirkungsgrad" : 0.9,           
            "Volumenstrom" : 66.0,              #l/min
            "Betriebsdruck" : 170,              #bar
            "Greifgeschwindigkeit" : 100.0,     #m/min
            "Greifbeschleunigung" : 0.5,        #m/s²
            "Greiferart": "Hydraulikgreifer",
            "Oeffnungszeit": 6,                 #s
            "Schliesszeit": 10.5,               #s
            "Anteil bewegte Masse": 0.15        #%
            
        },
        "Vierseil-Mehrschalen Müllgreifer MRS Greifer 1-26-6315-6316":
        {
        "Leergewicht": 3800,                    #kg
            "Greifervolumen": 4.0,              #m³
            "Greifgeschwindigkeit" : 100.0,     #m/min
            "Greifbeschleunigung" : 0.5,        #m/s²
            "Greiferart": "Vierseil-Greifer",
            "Oeffnungszeit": 6,                 #s
            "Schliesszeit": 10.5,               #s
        }
    },
    
    "Müll": # Es handelt sich um die AVG Köln Werte des RMB
    {
            "Müll Gesamtmenge im Jahr[kg]": 760_000_000,            #kg     
            "Müll Anliefermenge in der Stunde[kg]": 235_000,        #kg     
            "Müll Anlieferdauer Stunden[h]": 12,                    #h
            "Müll Dichte Einlagerung[kg/m³]": 700,                  #kg/m³  
            "Müll Dichte Beschickung[kg/m³]": 800                   #kg/m³  
    },

    "Geschwindigkeiten": {
        "heben_senken_m_min": 100.00,           #m/min
        "katzfahrt_m_min": 85.0,                #m/min
        "kranfahrt_m_min": 85.0,                #m/min
        "oeffnen_schliessen_einh": 100.0,       #m/min
    },

    "Beschleunigungen": {
        "heben_senken_m_s2": 0.5,               #m/s²
        "katzfahrt_m_s2": 0.22,                 #m/s²
        "kranfahrt_m_s2": 0.22,                 #m/s²
        "oeffnen_schliessen_m_s2": 0.5,         #m/s²
    },

    "Referenzwege":
    {
        "Heben/Senken": 25,                     #m
        "Katzfahrt": 10,                        #m
        "Kranfahrt Einlagern": 35,              #m
        "Öffnen/Schließen": 11,                 #m
        "Trichterweg 1": 10,                    #m
        "Trichterweg 2": 25,                    #m
        "Trichterweg 3": 40,                    #m
        "Trichterweg 4": 55,                    #m
        "Trichterweg 5": 70,                    #m
        "Trichterweg 6": 85,                    #m
        "Trichterweg 7": 100,                   #m
        "Trichterweg 8": 115,                    #m
        "Trichterweg 9": 130,                   #m
        "Trichterweg 10": 145,                  #m
    },

    "Hubwerk": {#Werte aus 831022M.010000-8_Motorgreifer
        "Seilgewicht": 200.0,                   #kg
        "Geschwindigkeit": 80.0,                #m/min
        "Beschleunigung": 0.67,                 #m/s²
        "Motordrehzahl": 1488,                  #1/s
        "Massentraegheit": 5.3,                 #kg*m²
        "AnzahlMotoren": 1,                     #Stk
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradSeiltrieb": 0.99,
        "Getriebestufen": 3,
        "WirkungsgradMotor": 0.967
    },

    "Katze": {#Werte aus 831022M.010000-8_Motorgreifer
        "Gewicht": 12300.0,                     #kg
        "Geschwindigkeit": 60.0,                #m/min
        "Beschleunigung": 0.25,                 #m/s²
        "Motordrehzahl": 1456,                  #1/s
        "Massentraegheit": 0.008,               #kg*m²
        "AnzahlMotoren": 2,                     #Stk
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradMotor": 0.896,
        "Getriebestufen": 2,
        "Fahrwiderstand": 8.5,                  #kg/t
    },

    "Kran": {#Werte aus 831022M.010000-8_Motorgreifer
        "Gewicht": 30200.0,                     #kg
        "Geschwindigkeit": 80.0,                #m/min
        "Beschleunigung": 0.3,                  #m/s²
        "Motordrehzahl": 1461,                  #1/s
        "Massentraegheit": 0.098,               #kg*m²
        "AnzahlMotoren": 2,                     #Stk
        "WirkungsgradGetrStufe": 0.98,
        "WirkungsgradVorgelege": 1.0,
        "Getriebestufen": 3,
        "Fahrwiderstand": 7,                    #kg/t
        "WirkungsgradMotor": 0.904
    },
    "Rückspeisung": {
        "FU-Wirkungsgrad Greifer": 0.98,
        "FU-Wirkungsgrad Hubfahrt": 0.98,
        "FU-Wirkungsgrad Kranfahrt": 0.98,
        "FU-Wirkungsgrad Katzfahrt": 0.98
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