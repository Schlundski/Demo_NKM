import streamlit as st

def check_login():
    """
    Blockt die Seite, bis korrektes (username, password) aus st.secrets eingegeben wurde.
    Merkt den Login in st.session_state['auth_ok'].
    """
    # eingeloggt?
    if st.session_state.get("auth_ok"):
        return True

    # Secrets vorhanden?
    user_expected = st.secrets.get("username")
    pwd_expected  = st.secrets.get("password")
    if not user_expected or not pwd_expected:
        st.error("Secrets 'username' und/oder 'password' fehlen. "
                 "Setze sie in Streamlit Cloud → App → Settings → Secrets.")
        st.stop()

    # Login-Form
    with st.form("login"):
        u = st.text_input("Benutzername")
        p = st.text_input("Passwort", type="password")
        ok = st.form_submit_button("Anmelden")

    if ok:
        if u == user_expected and p == pwd_expected:
            st.session_state["auth_ok"] = True
            st.session_state["auth_user"] = u
            st.rerun()
        else:
            st.error("Benutzername oder Passwort falsch.")
            st.stop()
    else:
        st.stop()

