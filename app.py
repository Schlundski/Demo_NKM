### Startseite und erste Login-Überprüfung

## Importieren nötiger Funktionen und Module
import streamlit as st
from common.page_init import page_init

## Seiteneinstellungen und Hintergrund
page_init("Anwendung Modernisierung", "🔒", "centered")

# Weiterleitung zur Startseite
st.switch_page("pages/startseite.py")
