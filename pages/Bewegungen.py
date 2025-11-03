# Bewegungseingaben

import streamlit as st

f = st.session_state["faktoren"]
# UI

st.title("Kranbewegungen")

# Greiferbewegungen
if st.session_state("greiferart") == "Vierseil-Greifer":
    with st.expander("Greiferbewegungen", width="stretch"):
        st.write("Schließgeschwindigkeit des Greifers [m/min]\n")
        geschwindigkeit_greifer = st.number_input("Höchstschließgeschwindigkeit", key = "gesch_greifer", step = 1, min_value = 5)
        st.write("\n\n")

        st.write("Schließbeschleunigung des Greifers [m/s²]\n")
        beschleunigung_greifer = st.number_input("Schließbeschleunigung", key = "besch_greifer")
        st.write("\n\n")

# Hubwerkbewegungen

with st.expander("Hubwerkbewegungen", width="stretch"):
    st.write("Hubgeschwindigkeit [m/min]\n")
    geschweindigkeit_hubwerk = st.number_input("Höchsthubgeschwindigkeit", key = "gesch_hubwerk")
    st.write("\n\n")

    st.write("Hubwerkbeschleunigung [m/s²]\n")
    beschleunigung_hubwerk = st.number_input("Hubwerkbeschleunigung", key = "besch_hubwerk")
    st.write("\n\n")

# Katzenbewegung

with st.expander("Katzenbeewegung", width="stretch"):
    st.write("Höchstgeschwindigkeit der Katze [m/min]\n")
    geschwindigkeit_katze = st.number_input("Höchstgeschwindigkeit der Katze", key = "gesch_katze")
    st.write("\n\n")

    st.write("Beschleunigung der Katze [m/s²]\n")
    beschleunigung_katze = st.number_input("Beschleunigung der Katze", key = "besch_katze")
    st.write("\n\n")

#Kranbewegung

with st.expander("Kranbewegung", width="stretch"):
    st.write("Höchstgeschwindigkeit der Kranbrücke [m/s]")
    geschwindigkeit_kran = st.number_input("Höchstgeschwindigkeit der Kranbrücke", key = "gesch_kran")
    st.write("\n\n")

    st.write("Beschleunigung der Kranbrücke [m/s²]")
    beschleunigung_kran = st.number_input("Beschleunigung der Kranbrücke", key = "besch_kran")
    st.write("\n\n")
