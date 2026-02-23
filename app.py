### Startseite und erste Login-Überprüfung

## Importieren nötiger Funktionen und Module
import streamlit as st
from auth.auth import check_login
from ui.theme import set_background_auto_theme

## Seiteneinstellungen und Hintergrund
if "logged_in" in st.session_state and st.session_state["logged_in"]:
    icon = "🏭"
else:
    icon = "🔒"
st.set_page_config(page_title="Anwendung Modernisierung", page_icon="🔒", layout="centered")

set_background_auto_theme(
"assets/bg_light.jpg",
"assets/bg_dark.jpg",
)

## Login-Überprüfung -> Weiterleitung zur Startseite bei Bestehen
check_login()

# Weiterleitung zur Startseite
st.switch_page("pages/startseite.py")
