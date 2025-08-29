import streamlit as st

#Startseite generieren, damit app nicht links steht in der Navigation
def startseite():
    st.image("image/Noell.jpg")
    st.write("# 🏭Willkommen! \nZuerst müssen Sie die Daten der Bestandsanlage eingeben und speichern. \n\nDann können Sie Änderungen eingeben und in Echt-Zeit eine Auswertung der faktorenspezifischen Daten erhalten. \n\nWenn Sie bereit sind, drücken sie die Taste \"Eingabe der Daten der Anlage\".")

    if st.button(label="Eingabe der Daten der Anlage"):
        st.switch_page("pages/Faktoren.py")

#Navigation konfigurieren
pg = st.navigation([
    st.Page(startseite, title="Startseite", icon="🏭"),
    st.Page("pages/Faktoren.py", title="Faktoren", icon="🔧"),
    st.Page("pages/Auswertung.py", title="Auswertung", icon="📊"),
])
pg.run()


