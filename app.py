import streamlit as st
from auth import check_login
from ui.theme import set_background_auto_theme

st.set_page_config(page_title="Anwendung Modernisierung", page_icon="🔒")

set_background_auto_theme(
"assets/bg_light.jpg",
"assets/bg_dark.jpg",
)

check_login()

def startseite():
    st.set_page_config(layout = "centered")

    st.image("assets/Noell.jpg")
    st.markdown("""
             # 🏭Willkommen!
             Zuerst werden Sie durch die Dateneingabe Ihrer Bestandsanlage geführt.\n
             Dann können Sie ihre Eingaben nochmals überprüfen und speichern.\n
             Abschließend kommt eine Auswertung der Eingaben. Dort können Sie auch Erneuerungen vornehmen und der Unterschied wird anschaulich Visualisiert.\n
             Wenn Sie bereit sind, drücken sie die Taste \"Eingabe der Daten der Anlage\".
             """)
             

    if st.button(label="Eingabe der Daten der Anlage"):
        st.switch_page("pages/Anlage.py")

startseite()