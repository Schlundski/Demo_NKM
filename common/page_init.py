### Gemeinsame Seiteneinstellungen, Hintergrund und Login-Überprüfung
## Importieren nötiger Funktionen und Module
import streamlit as st
from auth.auth import check_login
from ui.theme import set_background_auto_theme
from ui.components import my_sidebar_nav

## Funktion für gemeinsame Seiteneinstellungen, Hintergrund und Login-Überprüfung
def page_init(title, icon, layout):

    st.set_page_config(page_title=title, page_icon=icon, layout = layout)

    set_background_auto_theme(
        "assets/bg_light.jpg",
        "assets/bg_dark.jpg",
    )

    check_login()

    my_sidebar_nav()