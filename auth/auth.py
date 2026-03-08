## Hier findet die Autorisierung statt, ist tatsächlich recht simpel und funktioniert sehr gut

# Importieren nötiger Module
import streamlit as st
# Seiteneinstellungen
st.set_page_config(layout = "centered")

def check_login():
    if st.secrets.get("login_enabled", True): ## Soll überhaupt ein Login erfolgen? 
        # secrets.toml lesen (lokal oder über streamlit-cloud)
        auth_section = st.secrets.get("auth", st.secrets)
        USER = auth_section.get("username")
        PASS = auth_section.get("password")

        if not USER or not PASS:
            st.error("Login ist nicht konfiguriert. Bitte secrets.toml / Cloud-Secrets setzen.")
            st.stop()

        if st.session_state.get("logged_in"):
            return  # bereits eingeloggt

        st.markdown("### 🔒 Anmelden")
        with st.form("login_form", clear_on_submit=False):
            u = st.text_input("Benutzername")
            p = st.text_input("Passwort", type="password")
            ok = st.form_submit_button("Login")

        if ok:
            if u == USER and p == PASS:
                st.session_state["logged_in"] = True
                st.success("Erfolgreich angemeldet.")
                st.rerun()
            else:
                st.error("Falsche Zugangsdaten.")
                st.stop()

        # Wenn noch nicht eingeloggt: Seite hier hart beenden
        st.stop()
    else:
        st.session_state["logged_in"] = True