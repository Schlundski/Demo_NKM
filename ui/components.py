import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Literal

df_laender = pd.read_csv("tabellen/Stromländerpreise+CO2.csv", sep=';')

## Helper für die Faktoreneingabe---------------------------------------------------------------
# Helper für die Eingabeoberfläche für numerische Eingaben mit Standardcheckbox
def number_standard(
        titel="not defined",
        standard=0.0,
        min=0.0,
        steps=0.1,
        max=15,
        key="not_defined",
        helptext=None,
        nachkommastellen=2
        ):

    "Unser UI Standart für numerische Eingaben, returned nur den Eingabe- bzw. Standartwert"
    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Standard", value=False, key=f"use_default_{key}")

    if use_std:
        key2 = f"value_{key}_standard"
    else:
        key2 = f"value_{key}"

    ausgabe = st.number_input(
        titel,
        value=float(standard),
        min_value=float(min),
        max_value=float(max),
        step=float(steps),
        disabled=True if use_std else False,
        key=key2,
        label_visibility="collapsed",
        format=f"%.{nachkommastellen}f"
    )
    return ausgabe

# Helper für die Eingabeoberfläche für Texteingaben mit Auswahl mit Standardcheckbox
def selectbox_standard(
        titel="not defined",
        standard = "not defined",
        auswahl = ["nicht definiert"],
        key="not_defined",
        helptext=None
        ):

    "Unser UI Standart für Texteingaben, returned nur den Eingabe- bzw. Standartwert"

    index_converted = auswahl.index(standard)

    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Standard", value=False, key=f"use_default_{key}")

    if use_std:
        key2 = f"value_{key}_standard"
    else:
        key2 = f"value_{key}"

    ausgabe = st.selectbox(
        label = titel,
        options = auswahl,
        placeholder = "Deutschland",
        index = index_converted,
        disabled = True if use_std else False,
        key = key2
    )

    return ausgabe

# Helper für die Eingabeoberfläche für Texteingaben mit Standardcheckbox
def text_standard(
        titel="not defined",
        standard="Hier Text eingeben",
        key="not_defined",
        helptext=None
        ):

    "Unser UI Standart für Texteingaben, returned nur den Eingabe- bzw. Standartwert"

    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Standard", value=False, key=f"use_default_{key}")

    if use_std:
        key2 = f"value_{key}_standard"
    else:
        key2 = f"value_{key}"

    ausgabe = st.text_input(
        titel,
        value=standard,
        disabled=True if use_std else False,
        key= key2,
        label_visibility="collapsed",
        help = helptext
    )

    return ausgabe

# Helper für das Ankreuzen der Rückspeiseabfragen
def rueckspeisung_standard(        
        titel="not defined",
        standard=0.98,
        min=0.0,
        steps=0.1,
        max=15.0,
        key="not_defined",
        helptext=None,
        nachkommastellen=2
        ):
    
    "Unser UI Standart für Werteeingaben, returned nur den True/False und je nachdem vielleicht den Wert"

    ausgabe_checkbox = st.checkbox(titel, False, f"{key}_check", help=helptext)
    if ausgabe_checkbox == True:
        ausgabe_numberbox = st.number_input(
            f"FU-Wirkungsgrad für {titel}",
            float(min), float(max), float(standard), float(steps),
            key= f"{key}_number",
            format=f"%.{nachkommastellen}f" )
        return ausgabe_numberbox, 1
    
    return 0, 0

## Helper für die Modernisierungseingaben (Fast dasselbe wie oben)------------------------------
# Helper für die Eingabeoberfläche für numerische Eingaben mit Standardcheckbox
def number_soll(
        titel="not defined",
        ist=0.0,
        min=0.0,
        steps=0.1,
        max=15,
        key="not_defined",
        helptext=None,
        nachkommastellen=2
        ):

    "Unser UI Standart für numerische Eingaben, returned nur den Eingabe- bzw. Standartwert"
    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Ist-Wert", value=False, key=f"soll_use_default_{key}")

    if use_std:
        key2 = f"soll_value_{key}_standard"
    else:
        key2 = f"soll_value_{key}"

    ausgabe = st.number_input(
        titel,
        value=float(ist),
        min_value=float(min),
        max_value=float(max),
        step=float(steps),
        disabled=True if use_std else False,
        key=key2,
        label_visibility="collapsed",
        format=f"%.{nachkommastellen}f"
    )
    return ausgabe

# Helper für die Eingabeoberfläche für Texteingaben mit Auswahl mit Standardcheckbox
def selectbox_soll(
        titel="not defined",
        ist = "not defined",
        auswahl = ["nicht definiert"],
        key="not_defined",
        helptext=None
        ):

    "Unser UI Standart für Texteingaben, returned nur den Eingabe- bzw. Standartwert"

    index_converted = auswahl.index(ist)

    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Ist-Wert", value=False, key=f"soll_use_default_{key}")

    if use_std:
        key2 = f"soll_value_{key}_standard"
    else:
        key2 = f"soll_value_{key}"

    ausgabe = st.selectbox(
        label = titel,
        options = auswahl,
        placeholder = "Deutschland",
        index = index_converted,
        disabled = True if use_std else False,
        key = key2
    )

    return ausgabe

# Helper für die Eingabeoberfläche für Texteingaben mit Standardcheckbox
def text_soll(
        titel="not defined",
        ist="Hier Text eingeben",
        key="not_defined",
        helptext=None
        ):

    "Unser UI Standart für Texteingaben, returned nur den Eingabe- bzw. Standartwert"

    col1, col2 = st.columns([5, 2])
    with col1:
        st.markdown(titel, help=helptext)
    with col2:
        use_std = st.checkbox("Ist-Wert", value=False, key=f"soll_use_default_{key}")

    if use_std:
        key2 = f"soll_value_{key}_standard"
    else:
        key2 = f"soll_value_{key}"

    ausgabe = st.text_input(
        titel,
        value=ist,
        disabled=True if use_std else False,
        key= key2,
        label_visibility="collapsed",
        help = helptext
    )

    return ausgabe

## Visualisierung-------------------------------------------------------------------------------
# Helper für das Erstellen der Plots mit links den Daten und rechts dem Plot plus Slider für die Hochrechnungen auf verschiedene Zeiträume
DeltaColor = Literal["normal", "inverse", "off"] # Auswahl für deltacolor festlegen, um schreibfehler zu verhindern

def plot_ldaten_rdiagramm(titel, wertart, ist_tag, neu_tag, unterschied: DeltaColor = "inverse"):
    
    st.divider()
    st.header(titel)

    label = st.select_slider(
        "Zeitraum wählen",
        options=["1 Tag", "1 Woche", "1 Monat", "1 Jahr",
                 "2 Jahre", "3 Jahre", "5 Jahre", "10 Jahre", "20 Jahre"],
        value="1 Jahr",
        key=f"slider_{titel}"
    )

    faktor_map = {
        "1 Tag": 1,
        "1 Woche": 7,
        "1 Monat": 30,
        "1 Jahr": 365,
        "2 Jahre": 730,
        "3 Jahre": 1095,
        "5 Jahre": 1825,
        "10 Jahre": 3650,
        "20 Jahre": 7300,
    }
    faktor = faktor_map[label]

    ist_summe = ist_tag * faktor
    neu_summe = neu_tag * faktor
    einsparung = (ist_summe - neu_summe) *-1

    col1, col2 = st.columns(2)
    with col1:
        st.write("## ")
        st.subheader("Errechnete Werte")
        st.metric(f"{wertart} (Ist)", f"{ist_summe:,.2f}")
        st.metric(f"{wertart} (Neu)", f"{neu_summe:,.2f}", delta=f"{einsparung:,.2f}", delta_color=unterschied)

    with col2:
        df = pd.DataFrame({"Variante": ["Ist", "Neu"], wertart: [ist_summe, neu_summe]})
        fig = px.bar(df, x="Variante", y=wertart, color="Variante", text_auto=True, color_discrete_map={"Ist": "#d9534f", "Neu": "#5cb85c",})
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

def plot_aufteilung_CO2(standort: str, kWh_ist_proTag: float, kWh_neu_proTag: float):

    ENERGIE_SPALTEN = ["Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges"]

    # --- Zeile für das Land holen ---
    row_df = df_laender.loc[df_laender["Land"] == standort]
    if row_df.empty:
        st.error(f"Land '{standort}' nicht gefunden.")
        return
    land_row = row_df.iloc[0]

    # --- CO2-Faktor-Zeile holen ---
    co2_df = df_laender.loc[df_laender["Land"] == "CO2Faktor"]
    if co2_df.empty:
        st.error("Zeile 'CO2Faktor' nicht gefunden.")
        return
    co2_row = co2_df.iloc[0]

    # --- Werte in floats ---
    anteile_pct = pd.to_numeric(land_row[ENERGIE_SPALTEN], errors="coerce").fillna(0.0)   # %
    co2_faktoren = pd.to_numeric(co2_row[ENERGIE_SPALTEN], errors="coerce").fillna(0.0)  # gCO2/kWh (Annahme)

    # --- CO2 je Quelle berechnen (g/Tag) ---
    def co2_g_pro_tag(kwh_pro_tag: float) -> pd.Series:
        return kwh_pro_tag * (anteile_pct / 100.0) * co2_faktoren

    co2_ist_g = co2_g_pro_tag(kWh_ist_proTag)
    co2_neu_g = co2_g_pro_tag(kWh_neu_proTag)

    gesamt_ist_kg = float(co2_ist_g.sum()) / 1000.0
    gesamt_neu_kg = float(co2_neu_g.sum()) / 1000.0
    diff_kg = gesamt_ist_kg - gesamt_neu_kg

    # --- UI ---
    show_anteile = st.checkbox("CO₂-Aufteilung nach Energiequelle anzeigen", value=True)

    fig = go.Figure()

    if show_anteile:
        # Gestapelte Balken: IST vs NEU, aufgeteilt nach Quellen
        for quelle in ENERGIE_SPALTEN:
            fig.add_trace(go.Bar(
                x=["IST", "NEU"],
                y=[float(co2_ist_g[quelle]) / 1000.0, float(co2_neu_g[quelle]) / 1000.0],
                name=quelle
            ))

        fig.update_layout(
            title=f"CO₂-Aufteilung pro Tag (IST vs NEU) – {standort}",
            xaxis_title="Zustand",
            yaxis_title="CO₂ (kg/Tag)",
            barmode="stack",
            legend_title="Energiequelle"
        )
    else:
        # Nur Gesamt: IST vs NEU
        fig.add_trace(go.Bar(x=["IST", "NEU"], y=[gesamt_ist_kg, gesamt_neu_kg], name="Gesamt CO₂"))
        fig.update_layout(
            title=f"Gesamt CO₂ pro Tag (IST vs NEU) – {standort}",
            xaxis_title="Zustand",
            yaxis_title="CO₂ (kg/Tag)",
        )

    st.plotly_chart(fig, use_container_width=True)

    # --- Kennzahlen ---
    c1, c2, c3 = st.columns(3)
    c1.metric("IST CO₂ / Tag", f"{gesamt_ist_kg:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", "."))
    c2.metric("NEU CO₂ / Tag", f"{gesamt_neu_kg:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", "."))
    c3.metric("Ersparnis / Tag", f"{diff_kg:,.2f} kg".replace(",", "X").replace(".", ",").replace("X", "."))
