import streamlit as st
from auth import check_login
from ui.components import number_standard
from config.standards import STANDARDWERTE
import time

st.header("Allgemeinen Anlagendaten")

st.write("# :grey[Allgemeine Daten]")
anzahl_kraene = number_standard("Anzahl der Kräne", STANDARDWERTE["Anlage"]["Anzahl Kräne"], 1, 1, 10, "anzl_kraene")
anzahl_trichter = number_standard("Anzahl der Trichter", STANDARDWERTE["Anlage"]["Anzahl Trichter"], 1, 1, 10, "anzl_trichter")
verbrennung_trichter = number_standard("Verbrennung je Trichter [t]", STANDARDWERTE["Anlage"]["Verbrennung je Trichter"], 0, 0.1, 100, "vbrng_trichter" )

st.write("# :grey[Eingabe der Mülldaten]")
müll_anlieferung_h = number_standard("Müllanliefermenge pro Stunde [t/h]", STANDARDWERTE["Müll"]["Müll Anliefermenge in der Stunde"], 0, 0.1, 1000, "ml_anlfrmg")
müll_dichte_beschickung = number_standard("Müll Dichte bei Beschickung [t/m³]", STANDARDWERTE["Müll"]["Müll Dichte Beschickung in t/m³"], 0, 1, 2, "ml_dcht_beschickung")
müll_dichte_anlieferung = number_standard("Müll Dichte bei Anlieferung [t/m³]", STANDARDWERTE["Müll"]["Müll Dichte Einlagerung in t/m³"], 0, 0.1, 2, "ml_dcht_anlieferung")

button = st.button(
    "Speichern und weiter")

if button: 
    st.write(":green[Erfolgreich gespeichert✅]")
    time.sleep(2)
    st.switch_page("pages/Mech.py")