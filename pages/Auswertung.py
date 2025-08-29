import streamlit as st
import time

st.title("📊 Auswertung")

# Abfrage, ob Daten von der Faktorenseite übermittelt wurden
if "faktoren" not in st.session_state:
    st.warning("Keine Faktoren gefunden. Bitte zuerst auf der Seite „Faktoren“ eingeben.")
    st.stop()

f = st.session_state["faktoren"]

def get(dct, path, default=None):
    cur = dct
    for p in path.split("."):
        if isinstance(cur, dict) and p in cur:
            cur = cur[p]
        else:
            return default
    return cur

def safe_float(x, default=0.0):
    try:
        return float(x)
    except Exception:
        return default

# Neue Faktoren initial befüllen
if "neu_faktoren" not in st.session_state:
    st.session_state["neu_faktoren"] = {
        "greifer": {
            "greiferart":           get(f, "greifer.greiferart", "Vierseil-Greifer"),
            "leergewicht_Mg":       safe_float(get(f, "greifer.leergewicht_Mg", 0.0)),
            "motorleistung_kW":     safe_float(get(f, "greifer.motorleistung_kW", 0.0)),
            "volumen_m3":           safe_float(get(f, "greifer.volumen_m3", 0.0)),
        },
        "motoren": {
            "greifer_wirkungsgrad_pct": safe_float(get(f, "motoren.greifer_wirkungsgrad_pct", 92.0)),
            "hub_kW":               safe_float(get(f, "motoren.hub_kW", 0.0)),
            "hub_wirkungsgrad_pct": safe_float(get(f, "motoren.hub_wirkungsgrad_pct", 94.0)),
            "katz_kW":              safe_float(get(f, "motoren.katz_kW", 0.0)),
            "katz_wirkungsgrad_pct":safe_float(get(f, "motoren.katz_wirkungsgrad_pct", 93.0)),
            "kran_kW":              safe_float(get(f, "motoren.kran_kW", 0.0)),
            "kran_wirkungsgrad_pct":safe_float(get(f, "motoren.kran_wirkungsgrad_pct", 93.0)),
        },
        "geschwindigkeiten": {
            "heben_senken_m_min":   safe_float(get(f, "geschwindigkeiten.heben_senken_m_min", 0.0)),
            "katzfahrt_m_min":      safe_float(get(f, "geschwindigkeiten.katzfahrt_m_min", 0.0)),
            "kranfahrt_m_min":      safe_float(get(f, "geschwindigkeiten.kranfahrt_m_min", 0.0)),
            "oeffnen_schliessen_einh": safe_float(get(f, "geschwindigkeiten.oeffnen_schliessen_einh", 0.0)),
        },
        "beschleunigungen": {
            "heben_senken_m_s2":    safe_float(get(f, "beschleunigungen.heben_senken_m_s2", 0.0)),
            "katzfahrt_m_s2":       safe_float(get(f, "beschleunigungen.katzfahrt_m_s2", 0.0)),
            "kranfahrt_m_s2":       safe_float(get(f, "beschleunigungen.kranfahrt_m_s2", 0.0)),
            "oeffnen_schliessen_m_s2": safe_float(get(f, "beschleunigungen.oeffnen_schliessen_m_s2", 0.0)),
        },
    }

nf = st.session_state["neu_faktoren"]

col_left, col_right = st.columns(2)

# -----------------------------------------------
# Linke Spalte: Anzeige (Ist)
with col_left:
    st.subheader("Eingegebene Faktoren (Ist-Zustand)")

    st.write("**Greiferart:**",                    get(f, "greifer.greiferart", "—"))
    st.write("**Greifer Leergewicht [Mg]:**",      get(f, "greifer.leergewicht_Mg", "—"))
    st.write("**Motorleistung Greifer [kW]:**",    get(f, "greifer.motorleistung_kW", "—"))
    st.write("**Wirkungsgrad Greifermotor [%]:**", get(f, "motoren.greifer_wirkungsgrad_pct", "—"))
    st.write("**Greifervolumen [m³]:**",           get(f, "greifer.volumen_m3", "—"))

    st.markdown("---")
    st.write("**Geschwindigkeiten**")
    st.write("• Heben/Senken [m/min]:",    get(f, "geschwindigkeiten.heben_senken_m_min", "—"))
    st.write("• Katzfahrt [m/min]:",       get(f, "geschwindigkeiten.katzfahrt_m_min", "—"))
    st.write("• Kranfahrt [m/min]:",       get(f, "geschwindigkeiten.kranfahrt_m_min", "—"))
    st.write("• Öffnen/Schließen [Einheit]:", get(f, "geschwindigkeiten.oeffnen_schliessen_einh", "—"))

    st.markdown("---")
    st.write("**Beschleunigungen**")
    st.write("• Heben/Senken [m/s²]:",     get(f, "beschleunigungen.heben_senken_m_s2", "—"))
    st.write("• Katzfahrt [m/s²]:",        get(f, "beschleunigungen.katzfahrt_m_s2", "—"))
    st.write("• Kranfahrt [m/s²]:",        get(f, "beschleunigungen.kranfahrt_m_s2", "—"))
    st.write("• Öffnen/Schließen [m/s²]:", get(f, "beschleunigungen.oeffnen_schliessen_m_s2", "—"))

    st.markdown("---")
    st.write("**Antriebsdaten**")
    st.write("• Nennleistung Hubmotor [kW]:",     get(f, "motoren.hub_kW", "—"))
    st.write("• Wirkungsgrad Hubmotor [%]:",      get(f, "motoren.hub_wirkungsgrad_pct", "—"))
    st.write("• Nennleistung Katzfahrt [kW]:",    get(f, "motoren.katz_kW", "—"))
    st.write("• Wirkungsgrad Katzfahrt [%]:",     get(f, "motoren.katz_wirkungsgrad_pct", "—"))
    st.write("• Nennleistung Kranfahrt [kW]:",    get(f, "motoren.kran_kW", "—"))
    st.write("• Wirkungsgrad Kranfahrt [%]:",     get(f, "motoren.kran_wirkungsgrad_pct", "—"))

    with st.expander("Allgemeine Daten"):
        st.write("**Anzahl Kräne:**",                   get(f, "allgemein.anzahl_kraene", "—"))
        st.write("**Anzahl Trichter:**",               get(f, "allgemein.anzahl_trichter", "—"))
        st.write("**Verbrennung je Trichter [Mg/h]:**", get(f, "allgemein.verbrennung_pro_trichter_Mg_h", "—"))
        st.write("**Müllmenge im Jahr [Mg]:**",        get(f, "muell.gesamtmenge_Mg_a", "—"))
        st.write("**Anliefermenge Stunde [Mg/h]:**",   get(f, "muell.anliefermenge_Mg_h", "—"))
        st.write("**Anlieferdauer Stunden [h]:**",     get(f, "muell.anlieferdauer_h", "—"))
        st.write("**Dichte Einlagerung [Mg/m³]:**",    get(f, "muell.dichte_einlagerung_Mg_m3", "—"))
        st.write("**Dichte Beschickung [Mg/m³]:**",    get(f, "muell.dichte_beschickung_Mg_m3", "—"))
        st.markdown("---")
        st.write("**Referenzwege (Info)**")
        st.write("• Heben/Senken [m]:",                get(f, "referenzwege.heben_senken_m", "—"))
        st.write("• Katzfahrt [m]:",                   get(f, "referenzwege.katzfahrt_m", "—"))
        st.write("• Kranfahrt Einlagern [m]:",         get(f, "referenzwege.kranfahrt_m", "—"))
        st.write("• Öffnen/Schließen [m]:",            get(f, "referenzwege.oeffnen_schliessen_m", "—"))
        tw = get(f, "referenzwege.trichterwege_m", []) or []
        st.write("• Trichterweg 1 [m]:", tw[0] if len(tw) > 0 else "—")
        st.write("• Trichterweg 2 [m]:", tw[1] if len(tw) > 1 else "—")
        st.write("• Trichterweg 3 [m]:", tw[2] if len(tw) > 2 else "—")
        st.write("• Trichterweg 4 [m]:", tw[3] if len(tw) > 3 else "—")

# ------------------------------------------------
# Rechte Spalte: Anzeige/Bearbeitung
with col_right:
    st.subheader("Neu-Anlage")
    edit_mode = st.checkbox("Bearbeiten", value=False, key="neu_edit_mode")

    # Anzeige-Modus zeigt neuwerte
    if not edit_mode:
        st.write("**Greiferart:**",                    get(nf, "greifer.greiferart", "—"))
        st.write("**Greifer Leergewicht [Mg]:**",      get(nf, "greifer.leergewicht_Mg", "—"))
        st.write("**Motorleistung Greifer [kW]:**",    get(nf, "greifer.motorleistung_kW", "—"))
        st.write("**Wirkungsgrad Greifermotor [%]:**", get(nf, "motoren.greifer_wirkungsgrad_pct", "—"))
        st.write("**Greifervolumen [m³]:**",           get(nf, "greifer.volumen_m3", "—"))

        st.markdown("---")
        st.write("**Geschwindigkeiten**")
        st.write("• Heben/Senken [m/min]:",    get(nf, "geschwindigkeiten.heben_senken_m_min", "—"))
        st.write("• Katzfahrt [m/min]:",       get(nf, "geschwindigkeiten.katzfahrt_m_min", "—"))
        st.write("• Kranfahrt [m/min]:",       get(nf, "geschwindigkeiten.kranfahrt_m_min", "—"))
        st.write("• Öffnen/Schließen [Einheit]:", get(nf, "geschwindigkeiten.oeffnen_schliessen_einh", "—"))

        st.markdown("---")
        st.write("**Beschleunigungen**")
        st.write("• Heben/Senken [m/s²]:",     get(nf, "beschleunigungen.heben_senken_m_s2", "—"))
        st.write("• Katzfahrt [m/s²]:",        get(nf, "beschleunigungen.katzfahrt_m_s2", "—"))
        st.write("• Kranfahrt [m/s²]:",        get(nf, "beschleunigungen.kranfahrt_m_s2", "—"))
        st.write("• Öffnen/Schließen [m/s²]:", get(nf, "beschleunigungen.oeffnen_schliessen_m_s2", "—"))

        st.markdown("---")
        st.write("**Antriebsdaten**")
        st.write("• Nennleistung Hubmotor [kW]:",     get(nf, "motoren.hub_kW", "—"))
        st.write("• Wirkungsgrad Hubmotor [%]:",      get(nf, "motoren.hub_wirkungsgrad_pct", "—"))
        st.write("• Nennleistung Katzfahrt [kW]:",    get(nf, "motoren.katz_kW", "—"))
        st.write("• Wirkungsgrad Katzfahrt [%]:",     get(nf, "motoren.katz_wirkungsgrad_pct", "—"))
        st.write("• Nennleistung Kranfahrt [kW]:",    get(nf, "motoren.kran_kW", "—"))
        st.write("• Wirkungsgrad Kranfahrt [%]:",     get(nf, "motoren.kran_wirkungsgrad_pct", "—"))

    # Edit Modus
    else:
        neu_greiferart = st.selectbox(
            "Greiferart",
            ["Vierseil-Greifer", "Hydraulikgreifer"],
            index = (0 if get(nf, "greifer.greiferart") == "Vierseil-Greifer" else 1)
                    if get(nf, "greifer.greiferart") in ("Vierseil-Greifer","Hydraulikgreifer") else 0,
            key="neu_greiferart"
        )
        neu_g_leer = st.number_input("Greifer Leergewicht [Mg]",
                                     value=safe_float(get(nf, "greifer.leergewicht_Mg", 0.0)),
                                     key="neu_g_leer")
        neu_g_kw   = st.number_input("Motorleistung Greifer [kW]",
                                     value=safe_float(get(nf, "greifer.motorleistung_kW", 0.0)),
                                     key="neu_g_kw")
        neu_g_eta  = st.number_input("Wirkungsgrad Greifermotor [%]",
                                     value=safe_float(get(nf, "motoren.greifer_wirkungsgrad_pct", 92.0)),
                                     key="neu_g_eta")
        neu_g_vol  = st.number_input("Greifervolumen [m³]",
                                     value=safe_float(get(nf, "greifer.volumen_m3", 0.0)),
                                     key="neu_g_vol")

        st.markdown("---")
        st.write("**Geschwindigkeiten**")
        neu_v_heben = st.number_input("Geschwindigkeit Heben/Senken [m/min]",
                                      value=safe_float(get(nf, "geschwindigkeiten.heben_senken_m_min", 0.0)),
                                      key="neu_v_heben")
        neu_v_katz  = st.number_input("Geschwindigkeit Katzfahrt [m/min]",
                                      value=safe_float(get(nf, "geschwindigkeiten.katzfahrt_m_min", 0.0)),
                                      key="neu_v_katz")
        neu_v_kran  = st.number_input("Geschwindigkeit Kranfahrt [m/min]",
                                      value=safe_float(get(nf, "geschwindigkeiten.kranfahrt_m_min", 0.0)),
                                      key="neu_v_kran")
        neu_v_oes   = st.number_input("Geschwindigkeit Öffnen/Schließen [Einheit]",
                                      value=safe_float(get(nf, "geschwindigkeiten.oeffnen_schliessen_einh", 0.0)),
                                      key="neu_v_oes")

        st.markdown("---")
        st.write("**Beschleunigungen**")
        neu_a_heben = st.number_input("Beschleunigung Heben/Senken [m/s²]",
                                      value=safe_float(get(nf, "beschleunigungen.heben_senken_m_s2", 0.0)),
                                      key="neu_a_heben")
        neu_a_katz  = st.number_input("Beschleunigung Katzfahrt [m/s²]",
                                      value=safe_float(get(nf, "beschleunigungen.katzfahrt_m_s2", 0.0)),
                                      key="neu_a_katz")
        neu_a_kran  = st.number_input("Beschleunigung Kranfahrt [m/s²]",
                                      value=safe_float(get(nf, "beschleunigungen.kranfahrt_m_s2", 0.0)),
                                      key="neu_a_kran")
        neu_a_oes   = st.number_input("Beschleunigung Öffnen/Schließen [m/s²]",
                                      value=safe_float(get(nf, "beschleunigungen.oeffnen_schliessen_m_s2", 0.0)),
                                      key="neu_a_oes")

        # ÄÄnderungen übernehmen
        st.session_state["neu_faktoren"] = {
            "greifer": {
                "greiferart": st.session_state["neu_greiferart"],
                "leergewicht_Mg": st.session_state["neu_g_leer"],
                "motorleistung_kW": st.session_state["neu_g_kw"],
                "volumen_m3": st.session_state["neu_g_vol"],
            },
            "motoren": {
                "greifer_wirkungsgrad_pct": st.session_state["neu_g_eta"],
                "hub_kW": get(nf, "motoren.hub_kW", 0.0),
                "hub_wirkungsgrad_pct": get(nf, "motoren.hub_wirkungsgrad_pct", 94.0),
                "katz_kW": get(nf, "motoren.katz_kW", 0.0),
                "katz_wirkungsgrad_pct": get(nf, "motoren.katz_wirkungsgrad_pct", 93.0),
                "kran_kW": get(nf, "motoren.kran_kW", 0.0),
                "kran_wirkungsgrad_pct": get(nf, "motoren.kran_wirkungsgrad_pct", 93.0),
            },
            "geschwindigkeiten": {
                "heben_senken_m_min": st.session_state["neu_v_heben"],
                "katzfahrt_m_min": st.session_state["neu_v_katz"],
                "kranfahrt_m_min": st.session_state["neu_v_kran"],
                "oeffnen_schliessen_einh": st.session_state["neu_v_oes"],
            },
            "beschleunigungen": {
                "heben_senken_m_s2": st.session_state["neu_a_heben"],
                "katzfahrt_m_s2": st.session_state["neu_a_katz"],
                "kranfahrt_m_s2": st.session_state["neu_a_kran"],
                "oeffnen_schliessen_m_s2": st.session_state["neu_a_oes"],
            },
        }

# Debug halt
with st.expander("Debug: Session-Faktoren"):
    st.write("**faktoren**")
    st.json(st.session_state.get("faktoren", {}))
    st.write("**neu_faktoren**")
    st.json(st.session_state.get("neu_faktoren", {}))

st.write("Die Auswertung kommt, wenn die mathematischen Zusammenhänge ausgearbeitet wurden")
st.image("image/image.jpg")