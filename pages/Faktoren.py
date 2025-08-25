import streamlit as st
import pandas as pd
import time

st.title("🔧 Faktoren eingeben")

#(Komma/Punkt) in float wandeln
def to_float(x, default=None):
    try:
        return float(str(x).replace(",", "."))
    except:
        return default

## Faktorenuswahl

# Lastplan
auswahl_ablauf = st.selectbox("Lastplan der Anlage", ["Standard", "Individuell"])
if auswahl_ablauf == "Individuell":
    auswahl_ablauf_menge         = st.text_input("Müllmenge in t pro Woche")
    auswahl_ablauf_greif_zyklen  = st.text_input("Anzahl der Greifzyklen pro Woche")
    auswahl_ablauf_standby       = st.text_input("Standby-Zeit in h")

#Anlagendimensionen
auswahl_dimension_länge   = st.number_input("Anlagendimensionen Länge in m")
auswahl_dimension_breite  = st.number_input("Anlagendimensionen Breite in m")
auswahl_dimension_höhe    = st.number_input("Anlagendimensionen Höhe in m")
auswahl_dimension_gewicht = st.number_input("Krangewicht in t")

auswahl_umgebung_temperatur = st.text_input("Durchschnittliche Umgebungstemperatur in °C")
auswahl_umgebung_korrosion  = st.selectbox("Korrosionsbelastung", ["Normal","Erhöht","Stark"])

#Stromauswahl
auswahl_strom = st.selectbox(
    "Strommix Standard oder individuelle Eingabe?",
    ["Standard","Individuell Erneuerbare oder Fossile", "Individuell Exakt"]
)
if auswahl_strom == "Standard":
    auswahl_land = st.selectbox("Land", ["Belgien","Bulgarien","Dänemark","Deutschland","Estland","Finnland","Frankreich","Griechenland","Irland","Italien","Kroatien","Lettland","Litauen","Luxemburg","Malta","Niederlande","Norwegen","Österreich","Polen","Portugal","Rumänien","Schweden","Slowakei","Slowenien","Spanien","Zypern"])
elif auswahl_strom == "Individuell Erneuerbare oder Fossile":
    auswahl_strommix_ee = st.number_input("Prozentualer Anteil Erneuerbare Energien")
    auswahl_strommix_fe = st.number_input("Prozentualer Anteil Fossile Energien")
elif auswahl_strom == "Individuell Exakt":
    auswahl_strommix_preis  = st.number_input("Preis pro kWh in Cent")
    auswahl_strommix_wasser = st.number_input("Anteil Wasserkraft [%]")
    auswahl_strommix_solar  = st.number_input("Anteil Solar [%]")
    auswahl_strommix_wind   = st.number_input("Anteil Windkraft [%]")
    auswahl_strommix_bio    = st.number_input("Anteil Biomasse [%]")
    auswahl_strommix_atom   = st.number_input("Anteil Atomkraft [%]")
    auswahl_strommix_erdgas = st.number_input("Anteil Erdgas [%]")
    auswahl_strommix_kohle  = st.number_input("Anteil Kohle [%]")
    auswahl_strommix_geo    = st.number_input("Anteil Geothermie [%]")
    auswahl_strommix_öl     = st.number_input("Anteil Öl [%]")

#Zu modernisierende Faktoren
auswahl_greifer_alt = st.selectbox("Bauart der Greifer", ["-","Vier-Seil-Greifer","Hydraulik-Greifer"], index=1, key="greifer_alt")
auswahl_steuerung_alt = st.selectbox("Steuerung", ["-","Manuell","Automatisch"], key="steuerung_alt")
auswahl_hubmotor_leistung_alt  = st.number_input("Hubmotor kW (alt)", key="hub_kw_alt")
auswahl_fahrmotor_leistung_alt = st.number_input("Fahrmotor kW (alt)", key="fahr_kw_alt")
auswahl_fu_alt = st.selectbox("Frequenzumrichter", ["Standard","ABB AC880","Siemens S120","Siemens Masterdrive"], key="fu_alt")
auswahl_geschwindigkeit_alt = st.number_input("Geschwindigkeit m/s", key="v_alt")

#Speichern & Wechseln
if st.button("Auswahl speichern & zur Auswertung"):
    st.session_state["faktoren"] = {
        "lastplan": auswahl_ablauf,
        "menge_t_woche": to_float(locals().get("auswahl_ablauf_menge")),
        "zyklen_woche": to_float(locals().get("auswahl_ablauf_greif_zyklen")),
        "standby_h": to_float(locals().get("auswahl_ablauf_standby")),
        "dim_l_m": float(auswahl_dimension_länge),
        "dim_b_m": float(auswahl_dimension_breite),
        "dim_h_m": float(auswahl_dimension_höhe),
        "kran_t":  float(auswahl_dimension_gewicht),
        "umg_temp_C": to_float(auswahl_umgebung_temperatur),
        "umg_korrosion": auswahl_umgebung_korrosion,
        "strommodus": auswahl_strom,
        "land": locals().get("auswahl_land"),
        "ee_%": locals().get("auswahl_strommix_ee"),
        "fe_%": locals().get("auswahl_strommix_fe"),
        "preis_cent_kwh": locals().get("auswahl_strommix_preis"),
        "mix_wasser_%": locals().get("auswahl_strommix_wasser"),
        "mix_solar_%":  locals().get("auswahl_strommix_solar"),
        "mix_wind_%":   locals().get("auswahl_strommix_wind"),
        "mix_bio_%":    locals().get("auswahl_strommix_bio"),
        "mix_atom_%":   locals().get("auswahl_strommix_atom"),
        "mix_gas_%":    locals().get("auswahl_strommix_erdgas"),
        "mix_kohle_%":  locals().get("auswahl_strommix_kohle"),
        "mix_geo_%":    locals().get("auswahl_strommix_geo"),
        "mix_oel_%":    locals().get("auswahl_strommix_öl"),
        "alt": {
            "greifer": st.session_state["greifer_alt"],
            "steuerung": st.session_state["steuerung_alt"],
            "hub_kw": st.session_state["hub_kw_alt"],
            "fahr_kw": st.session_state["fahr_kw_alt"],
            "fu": st.session_state["fu_alt"],
            "v_mps": st.session_state["v_alt"],
        },
    }

    # -> Baseline für Auswertung bereitstellen (so erwartet es die Auswertungsseite)
    preis_cent = st.session_state["faktoren"].get("preis_cent_kwh")
    preis_eur_kwh = float(preis_cent)/100.0 if preis_cent is not None else 0.30  # Default 0,30 €/kWh
    co2_g_kwh = 366.0  # Default; kannst du später aus Land/Strommix ableiten
    betriebsstunden = 4000  # Default; falls du das Feld noch nicht abfragst

    st.session_state["baseline"] = {
        "hub_kw": float(st.session_state["faktoren"]["alt"]["hub_kw"] or 0),
        "fahr_kw": float(st.session_state["faktoren"]["alt"]["fahr_kw"] or 0),
        "fu": st.session_state["faktoren"]["alt"]["fu"],
        "betriebsstunden": int(betriebsstunden),
        "preis_eur_kwh": float(preis_eur_kwh),
        "co2_g_kwh": float(co2_g_kwh),
    }

    st.session_state["ready_for_analysis"] = True
    st.toast("Eingaben gespeichert ✅", icon="✅")
    time.sleep(2)
    st.switch_page("pages/Auswertung.py")
