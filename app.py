import streamlit as st
from auth import check_login

st.set_page_config(page_title="Meine App", page_icon="🔒")
check_login()

#Startseite generieren, damit app nicht links steht in der Navigation
def startseite():
    st.image("image/Noell.jpg")
    st.markdown("""
             # 🏭Willkommen!
             Zuerst werden Sie durch die Dateneingabe Ihrer Bestandsanlage geführt.\n
             Dann können Sie ihre Eingaben nochmals überprüfen und speichern.\n
             Abschließend kommt eine Auswertung der Eingaben. Dort können Sie auch Erneuerungen vornehmen und der Unterschied wird anschaulich Visualisiert.\n
             Wenn Sie bereit sind, drücken sie die Taste \"Eingabe der Daten der Anlage\".
             """)
             

    if st.button(label="Eingabe der Daten der Anlage"):
        st.switch_page("pages/Faktoren.py")

#Navigation konfigurieren
pg = st.navigation([
    st.Page(startseite, title="Startseite", icon="🏭"),
    st.Page("pages/Faktoren.py", title="Faktoren", icon="🔧"),
    st.Page("pages/Auswertung.py", title="Auswertung", icon="📊"),
])
pg.run()


