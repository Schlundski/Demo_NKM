### Startseite mit Einführung und Navigation
## Importieren nötiger Funktionen und Module
# Bibliotheken
import streamlit as st
# Eigene Module mit Funktionen
from common.page_init import page_init

## Seiteneinstellungen, Hintergrund und Login-Überprüfung
page_init("Startseite", "🏠", "centered")

## UI-Inhalte der Startseite
st.image("assets/noell.jpg")
st.markdown("""
# 🏭 Energie- & CO₂-Analyse für Krananlagen

Willkommen bei der Analyse-Anwendung für Bestands- und Neuanlagen.
            
Dieses Tool unterstützt Betreiber, Kunden und Planer dabei, Modernisierungseffekte von Krananlagen transparent zu bewerten.

Mit diesem Programm können Sie:

• die technischen Daten einer bestehenden Krananlage erfassen  
• den Energiebedarf in kWh berechnen  
• die daraus entstehenden Stromkosten ermitteln  
• den CO₂-Ausstoß abhängig vom Standort analysieren  
• und mögliche Einsparungen durch eine Modernisierung sichtbar machen  
            """)

with st.expander("🔍 Wie funktioniert das?"):
    st.markdown("""

    1. Sie geben die Daten Ihrer bestehenden Anlage ein.  
    2. Anschließend können Sie eine modernisierte Variante definieren.  
    3. Das System vergleicht beide Anlagen automatisch.  
    4. Sie erhalten eine übersichtliche Auswertung zu:         
        • Energieverbrauch  
        • Kosten  
        • CO₂-Emissionen  
        • **Einsparpotenzial**  

    """)

st.markdown("Wenn Sie bereit sind, starten Sie mit der Eingabe Ihrer Anlagendaten.")

# Navigation zur Anlagenseite
if st.button(label="Jetzt starten"):
    st.switch_page("pages/anlage.py")