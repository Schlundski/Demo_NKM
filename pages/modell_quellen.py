# pages/ModellQuellen.py
import math
from typing import Any

import pandas as pd
import streamlit as st

from config.standards import STANDARDWERTE
from ui.components import my_sidebar_nav
from ui.theme import set_background_auto_theme

# Rechenfunktionen (für echte Zwischenergebnisse)
from core.computing import (
    spielzeitenberechnung,
    muellberechnung,
    mechleistunghubwerk,
    mechleistungkatzfahrt,
    kranfahrt,
    greiferhydraulik,
    mechleistunggreifervierseil,
)

# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
my_sidebar_nav()
st.set_page_config(page_title="Modell & Quellen", layout="centered")
set_background_auto_theme(
    "assets/bg_light.jpg",
    "assets/bg_dark.jpg",
)
st.title("📖 Modell & Quellen")
st.caption(
    "Diese Seite dient der Nachvollziehbarkeit der in der Auswertung dargestellten Ergebnisse "
    "(Annahmen, verwendete Tabellenwerte, Quellen und aktuell eingesetzte Parameter). "
    "Zusätzlich wird der Rechenweg mit Formeln nachvollziehbar dargestellt."
)


# ------------------------------------------------------------
# Helper (Pylance/Typing-friendly)
# ------------------------------------------------------------

##Zahlenwerte sicher in Int konvertieren
def to_int(x: Any, default: int = 0) -> int:
    """Robust: None/''/— -> default, sonst int(float(x))."""
    try:
        if x is None:
            return default
        if isinstance(x, str) and x.strip() in ("", "—"):
            return default
        return int(x)
    except Exception:
        return default

##Zahlenwerte sicher in float konvertieren
def as_float(x: Any, default: float | None = None) -> float | None:
    """Robust: None/''/— -> default, sonst float(x)."""
    try:
        if x is None:
            return default
        if isinstance(x, str) and x.strip() in ("", "—"):
            return default
        return float(x)
    except Exception:
        return default

##Zahlenwerte auf 3 Nachkommastellen kürzen und zu String konvertieren; Einheit anhängen
def fmt_num(x: Any, unit: str = "", digits: int = 3, fallback: str = "—") -> str:
    v = as_float(x, None)
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return fallback
    s = f"{v:.{digits}f}"
    return f"{s} {unit}".rstrip()

##Verschachtelte Dictionaries zu unverschachtelten Listen entpacken für tabellarische Darstellung
def flatten_dict(d: dict, parent_key: str = "") -> list[dict]:
    rows: list[dict] = []
    for k, v in d.items():
        new_parent = f"{parent_key} / {k}" if parent_key else str(k)
        if isinstance(v, dict):
            rows.extend(flatten_dict(v, new_parent))
        else:
            rows.append({"Pfad": parent_key if parent_key else "ROOT", "Parameter": str(k), "Wert": v})
    return rows

##Dictionary-Pfade dur .-Trennung schreibbar machen und Wert zurückgeben
def dict_get(dct: dict | None, path: str, default: Any = "—") -> Any:
    """Sicheres Holen aus verschachtelten Dicts via 'a.b.c'-Pfad."""
    if not isinstance(dct, dict):
        return default
    cur: Any = dct
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur

# ------------------------------------------------------------
# Daten laden
# ------------------------------------------------------------

##CSV-Dateien einmal auslesen
@st.cache_data(show_spinner=False)      ##Nachfolgende Methode ohne Animation cachen -> CSV nur einmal laden
def load_strommix_csv(path: str) -> tuple[pd.DataFrame, pd.Series | None]:
    """
    Liest eure CSV (;) ein.
    Trennt die letzte Zeile 'CO2Faktor' ab (falls vorhanden) und gibt sie als Series zurück.
    """
    df = pd.read_csv(path, sep=";", engine="python")
    df.columns = [c.strip() for c in df.columns]

    #Sonderfall: CO2-Faktor in CSV separat speichern
    co2_row = None
    if "Land" in df.columns:
        mask = df["Land"].astype(str).str.strip().eq("CO2Faktor")
        if mask.any():
            co2_row = df.loc[mask].iloc[0]
            df = df.loc[~mask].copy()

    # Zahlen konvertieren, wo sinnvoll
    numeric_cols = [c for c in df.columns if c not in ("Land", "Quellen")]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    #Anteil am Strommix aller Energieträger in neue Spalte
    mix_cols = [c for c in ["Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges"] if c in df.columns]
    if mix_cols:
        df["Summe Strommix [%]"] = df[mix_cols].sum(axis=1, skipna=True)

    #Preisspalte auf 2 Nachkommastellen runden
    if "Preis in c/kWh" in df.columns:
        df["Preis in c/kWh"] = df["Preis in c/kWh"].round(2)

    #Länderspalte alphabetisch sortieren
    if "Land" in df.columns:
        df = df.sort_values("Land")

    return df, co2_row


# ------------------------------------------------------------
# Renderer
# ------------------------------------------------------------

##Standartwerte als Tabelle mit Tabs darstellen
def render_standards(standards: dict):
    st.subheader("Standardwerte")
    st.write("Diese Werte sind firmeninterne Erfahrungs- und Durchschnittswerte und dienen nur als Orientierung\n" 
    "Es werden alle Standartwerte gezeigt, auch diejenigen, die bei der aktuellen Konfiguration nicht genutzt werden")

    cats = list(standards.keys())
    tabs = st.tabs([cat.capitalize() for cat in cats])

    for tab, cat in zip(tabs, cats):
        with tab:
            val = standards[cat]

            #Dropdown zur Greifermodellauswahl
            if isinstance(val, dict) and cat == "greifer":
                greifer_names = list(val.keys())
                sel = st.selectbox("Greifer-Modell", greifer_names, key="src_greifer_select", help="Beispielmodelle zur erhebung von Standartwerten")
                df = pd.DataFrame([{"Parameter": p, "Wert": w} for p, w in val[sel].items()])
                st.dataframe(df, use_container_width=True, hide_index=True)
            #Alle anderen Tabs ohne Dropdown
            else:
                if isinstance(val, dict):
                    # Filter für Rückspeisung: Zeilen mit 'fu_' ausblenden
                    if cat == "rueckspeisung":
                        val = {k: v for k, v in val.items() if not k.startswith("faktor_")}
                    df = pd.DataFrame([{"Parameter": p, "Wert": w} for p, w in val.items()])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.write(val)

    #Tabelle auch ohne Tabs anzeigbar
    with st.expander("Alles als flache Gesamtliste anzeigen"):
        flat = flatten_dict(standards)
        st.dataframe(pd.DataFrame(flat), use_container_width=True, hide_index=True)

##Alle eingegebenen Werte tabellarisch Darstellen und ggf. Differenzen berechnen
def render_aktuelle_werte_ist_neu():
    st.subheader("🔎 Aktuell eingesetzte Werte (IST vs. NEU/SOLL)")
    #st.write(st.session_state)
    ist_anlage = st.session_state.get("ist_anlage", {})
    neu_anlage = st.session_state.get("neu_anlage", {})

    auswahl = st.session_state.get("radio_auswertung")

    if auswahl == "Vergleich mit modernisierter Neu-Anlage":
        outer_tab_names = ["IST", "NEU/SOLL", "Vergleich"]
    else:
        outer_tab_names = ["IST"]

    outer_tabs = st.tabs(outer_tab_names)

    # Hilfsfunktion, um alle Daten als DataFrame zu erzeugen
    def make_table(dct: dict) -> pd.DataFrame:
        # --- Anlage ---
        rows = [
            
            ("Anlage", "Standort", dict_get(dct, "anlage.anlage_standort")),
            ("Anlage", "Anzahl Kräne", dict_get(dct, "anlage.anzahl_kraene")),
            ("Anlage", "Anzahl Trichter", dict_get(dct, "anlage.anzahl_trichter")),
            ("Anlage", "Verbrennung je Trichter [kg/h]", dict_get(dct, "anlage.verbrennung_trichter_kg")),
            ("Anlage", "Energiekosten [ct/kWh]", dict_get(dct, "anlage.energie_kosten")),
            ("Anlage", "Müll Anlieferung [kg/h]", dict_get(dct, "anlage.muell_anlieferung_h_kg")),
            ("Anlage", "Müll Anlieferdauer [h/d]", dict_get(dct, "anlage.muell_anlieferdauer")),
            ("Anlage", "Müll Dichte Beschickung [kg/m³]", dict_get(dct, "anlage.muell_dichte_beschickung_kg_pro_m3")),
            ("Anlage", "Müll Dichte Anlieferung [kg/m³]", dict_get(dct, "anlage.muell_dichte_anlieferung_kg_pro_m3")),
        ]
        # --- Greifer ---
        if dict_get(dct, "greifer.typ") == "Hydraulikgreifer":
            if dict_get(dct,"greifer.auswahl_parameter") == "Schließ/Öffnungszeit":
                rows.extend([
                    ("Greifer", "Typ", dict_get(dct, "greifer.typ")),
                    ("Greifer", "Leergewicht [kg]", dict_get(dct, "greifer.leergewicht_kg")),
                    ("Greifer", "Volumen [m³]", dict_get(dct, "greifer.volumen_m3")),
                    ("Greifer", "Schließzeit [s]", dict_get(dct, "greifer.schliesszeit_s")),
                    ("Greifer", "Öffnungszeit [s]", dict_get(dct, "greifer.oeffnungszeit_s")),
                    ("Greifer", "Motorleistung [kW]", dict_get(dct, "greifer.motorleistung_kw")),
                    ("Greifer", "Wirkungsgrad Hydraulik [-]", dict_get(dct, "greifer.wirkungsgrad_hydraulik")),
                    ("Greifer", "Volumenstrom [l/min]", dict_get(dct, "greifer.volumenstrom_l_pro_min")),
                    ("Greifer", "Betriebsdruck [bar]", dict_get(dct, "greifer.betriebsdruck_bar")),
                ])
            else:
                rows.extend([
                    ("Greifer", "Typ", dict_get(dct, "greifer.typ")),
                    ("Greifer", "Leergewicht [kg]", dict_get(dct, "greifer.leergewicht_kg")),
                    ("Greifer", "Volumen [m³]", dict_get(dct, "greifer.volumen_m3")),
                    ("Greifer", "Geschwindigkeit [m/min]", dict_get(dct, "greifer.geschwindigkeit_m_pro_min")),
                    ("Greifer", "Beschleunigung [m/s²]", dict_get(dct, "greifer.beschleunigung_m_pro_s2")),
                    ("Greifer", "Motorleistung [kW]", dict_get(dct, "greifer.motorleistung_kw")),
                    ("Greifer", "Wirkungsgrad Hydraulik [-]", dict_get(dct, "greifer.wirkungsgrad_hydraulik")),
                    ("Greifer", "Volumenstrom [l/min]", dict_get(dct, "greifer.volumenstrom_l_pro_min")),
                    ("Greifer", "Betriebsdruck [bar]", dict_get(dct, "greifer.betriebsdruck_bar")),
                ])
        elif dict_get(dct, "greifer.typ") == "Vierseil-Greifer":
            rows.extend([
                ("Greifer", "Typ", dict_get(dct, "greifer.typ")),
                ("Greifer", "Leergewicht [kg]", dict_get(dct, "greifer.leergewicht_kg")),
                ("Greifer", "Volumen [m³]", dict_get(dct, "greifer.volumen_m3")),
                ("Greifer", "Geschwindigkeit [m/min]", dict_get(dct, "greifer.geschwindigkeit_m_pro_min")),
                ("Greifer", "Beschleunigung [m/s²]", dict_get(dct, "greifer.beschleunigung_m_pro_s2")),
            ])
        else:
            st.warning("Es wurde keine Greiferart gewählt, bitte nachholen!")
        rows.extend([ 
        # --- Hubwerk ---
            ("Hubwerk", "Seilgewicht [kg]", dict_get(dct, "kran_mechanik.hubwerk.seilgewicht_kg")),
            ("Hubwerk", "Geschwindigkeit [m/min]", dict_get(dct, "kran_mechanik.hubwerk.hub_geschwindigkeit_m_pro_min")),
            ("Hubwerk", "Beschleunigungt [m/s²]", dict_get(dct, "kran_mechanik.hubwerk.hub_beschleunigung_m_pro_s2")),
            ("Hubwerk", "Anzahl Motoren", dict_get(dct, "kran_mechanik.hubwerk.anzahl_motoren")),
            ("Hubwerk", "Getriebewirkungsgrad", dict_get(dct, "kran_mechanik.hubwerk.wirkungsgrad_getriebe")),
            ("Hubwerk", "Seiltriebwirkungsgrad", dict_get(dct, "kran_mechanik.hubwerk.wirkungsgrad_seiltrieb")),
            ("Hubwerk", "Getriebestufen", dict_get(dct, "kran_mechanik.hubwerk.getriebestufen")),
            ("Hubwerk", "Motorwirkungsgrad", dict_get(dct, "kran_mechanik.hubwerk.wirkungsgrad_motor_hub")),

        # --- Katze ---
            ("Katze", "Eigengewicht Katze [kg]", dict_get(dct, "kran_mechanik.katze.gewicht_kg")),
            ("Katze", "Geschwindigkeit [m/min]", dict_get(dct, "kran_mechanik.katze.geschwindigkeit_m_pro_min")),
            ("Katze", "Beschleunigung [m/s²]", dict_get(dct, "kran_mechanik.katze.beschleunigung_m_pro_s2")),
            ("Katze", "Anzahl Motoren", dict_get(dct, "kran_mechanik.katze.anzahl_motoren")),
            ("Katze", "Getriebewirkungsgrad", dict_get(dct, "kran_mechanik.katze.wirkungsgrad_getriebe")),
            ("Katze", "Gertiebestufen", dict_get(dct, "kran_mechanik.katze.getriebestufen")),
            ("Katze", "Fahrwiderstang [kg/t]", dict_get(dct, "kran_mechanik.katze.fahrwiderstand_kg_pro_t")),
            ("Katze", "Motorwirkungsgrad", dict_get(dct, "kran_mechanik.katze.wirkungsgrad_motor_katze")),

        # --- Kran ---
            ("Kran", "Eigengewicht Kran [kg]", dict_get(dct, "kran_mechanik.kranfahrwerk.gewicht_kg")),
            ("Kran", "Geschwindigkeit [m/min]", dict_get(dct, "kran_mechanik.kranfahrwerk.geschwindigkeit_m_pro_min")),
            ("Kran", "Beschleunigung [m/s²]", dict_get(dct, "kran_mechanik.kranfahrwerk.beschleunigung_m_pro_s2")),
            ("Kran", "Anzahl Motoren", dict_get(dct, "kran_mechanik.kranfahrwerk.anzahl_motoren")),
            ("Kran", "Getriebewirkungsgrad", dict_get(dct, "kran_mechanik.kranfahrwerk.wirkungsgrad_getriebe")),
            ("Kran", "Vorgelegewirkungsgrad", dict_get(dct, "kran_mechanik.kranfahrwerk.wirkungsgrad_vorgelege")),
            ("Kran", "Getriebestufen", dict_get(dct, "kran_mechanik.kranfahrwerk.getriebestufen")),
            ("Kran", "Fahrwiderstand [kg/t]", dict_get(dct, "kran_mechanik.kranfahrwerk.fahrwiderstand_kg_pro_t")),
            ("Kran", "Motorwirkungsgrad", dict_get(dct, "kran_mechanik.kranfahrwerk.wirkungsgrad_motor_kran")),

        # --- Wege ---           
            ("Wege", "Heben/Senken [m]", dict_get(dct, "wege.weg_hebensenken_m")),
            ("Wege", "Katzfahrt [m]", dict_get(dct, "wege.weg_katzfahrt_m")),
            ("Wege", "Kranfahrt Einlagern [m]", dict_get(dct, "wege.weg_kranfahrt_einlagern_m")),        
        ])
            #Trichterwege abhängig der Anzahl der Trichter
        anz_trichter = to_int(dict_get(dct, "anlage.anzahl_trichter"))
        trichter_dict = dict_get(dct, "wege.weg_trichter_m", {})
        for i in range(anz_trichter):
            rows.append((
                    "Wege",
                    f"Referenzweg Trichter {i+1} [m]",
                    trichter_dict.get(i, "—")
            ))
        rows.extend([
            ("Wege", "Öffnen/Schließen [m]", dict_get(dct, "wege.weg_oeffnen_schliessen_m")),
        ])

        #--- Rückspeisung ---
        if dict_get(dct, "greifer.typ") == "Vierseil-Greifer":
            rows.extend([
                ("Rückspeisung", "Wirkungsgrad Frequenzumrichter Greifer", dict_get(dct, "rueckspeisung.fu_wirkungsgrad_greifer")),
            ])
        rows.extend([
            ("Rückspeisung", "Wirkungsgrad Frequenzumrichter Hubwerk", dict_get(dct, "rueckspeisung.fu_wirkungsgrad_hub")),
            ("Rückspeisung", "Wirkungsgrad Frequenzumrichter Kran", dict_get(dct, "rueckspeisung.fu_wirkungsgrad_kran")),
            ("Rückspeisung", "Wirkungsgrad Frequenzumrichter Katze", dict_get(dct, "rueckspeisung.fu_wirkungsgrad_katze")),
        ])  
        return pd.DataFrame(rows, columns=["Kategorie", "Parameter", "Wert"])

    #Kategorien, die als untertabs Dargestellt werden
    categories = ["Anlage", "Greifer", "Hubwerk", "Katze", "Kran", "Wege", "Rückspeisung"]

    # --- Tab: IST ---
    with outer_tabs[0]:
        inner_tabs = st.tabs(categories)
        df_ist = make_table(ist_anlage)
        for i, cat in enumerate(categories):
            with inner_tabs[i]:
                df = df_ist[df_ist["Kategorie"] == cat].drop(columns="Kategorie")
                st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Tab: NEU/SOLL ---
    if auswahl == "Vergleich mit modernisierter Neu-Anlage":
        with outer_tabs[1]:
            inner_tabs = st.tabs(categories)
            df_neu = make_table(neu_anlage)
            for i, cat in enumerate(categories):
                with inner_tabs[i]:
                    df = df_neu[df_neu["Kategorie"] == cat].drop(columns="Kategorie")
                    st.dataframe(df, use_container_width=True, hide_index=True)

    # --- Tab: Vergleich ---
    if auswahl == "Vergleich mit modernisierter Neu-Anlage":
        with outer_tabs[2]:
            ist_df = make_table(ist_anlage).rename(columns={"Wert": "IST"})
            ist_df = ist_df.fillna("—")
            neu_df = make_table(neu_anlage).rename(columns={"Wert": "NEU/SOLL"})
            neu_df = neu_df.fillna("—")
            cmp_df = ist_df.merge(neu_df, on=["Kategorie", "Parameter"], how="outer")
            cmp_df = cmp_df.fillna("—")
        

        #Berechnung von Differenzen, "—" falls keine Zahlenwerte
        def diff(a: Any, b: Any):
            try:
                return float(b) - float(a)
            except Exception:
                return "—"

        cmp_df["Δ (NEU-IST)"] = [diff(a, b) for a, b in zip(cmp_df["IST"], cmp_df["NEU/SOLL"])]

        inner_tabs = st.tabs(categories)
        for i, cat in enumerate(categories):
            with inner_tabs[i]:
                df = cmp_df[cmp_df["Kategorie"] == cat].drop(columns="Kategorie")
                st.dataframe(df, use_container_width=True, hide_index=True)

def render_rechenweg():
    st.subheader("🧮 Rechenwege")

    ist = st.session_state.get("ist_anlage", None)
    neu = st.session_state.get("neu_anlage", None)

    #Absicherung, falls keine Dictionaries angelegt wurden. Sollte nicht möglich sein
    if not isinstance(ist, dict) or not ist:
        st.info("Keine IST-Daten im Session State gefunden (ist_anlage). Bitte erst auf den Eingabeseiten Werte speichern.")
        return

    if not isinstance(neu, dict) or not neu:
        st.info("Keine NEU/SOLL-Daten im Session State gefunden (neu_anlage). Der Rechenweg wird nur für IST angezeigt.")
        neu = None

    tabs = st.tabs(["IST", "NEU/SOLL"] if neu else ["IST"])

    def get_inputs(dct: dict):
        # Pfade
        anlage = dct.get("anlage", {})
        greifer = dct.get("greifer", {})
        hub = dct.get("kran_mechanik", {}).get("hubwerk", {})
        katz = dct.get("kran_mechanik", {}).get("katze", {})
        kran = dct.get("kran_mechanik", {}).get("kranfahrwerk", {})
        wege = dct.get("wege", {})
        rueck = dct.get("rueckspeisung", {})
        return anlage, greifer, hub, katz, kran, wege, rueck

    def render_for(dct: dict, label: str):
        anlage, greifer, hub, katz, kran, wege, rueck = get_inputs(dct)

        # --- Basisgrößen (sicher ziehen) ---
        n_trichter = as_float(anlage.get("anzahl_trichter"), None)
        verb_trichter = as_float(anlage.get("verbrennung_trichter_kg"), None)  # kg/h pro Trichter
        anliefer_h = as_float(anlage.get("muell_anlieferung_h_kg"), None)  # kg/h
        anlieferdauer = as_float(anlage.get("muell_anlieferdauer"), None)  # h/d

        rho_beschick = as_float(anlage.get("muell_dichte_beschickung_kg_pro_m3"), None)
        rho_anliefer = as_float(anlage.get("muell_dichte_anlieferung_kg_pro_m3"), None)

        V = as_float(greifer.get("volumen_m3"), None)

        # Greifer
        greifer_typ = greifer.get("typ", "—")
        m_greifer_leer = as_float(greifer.get("leergewicht_kg"), None)
        v_greifer_mmin = as_float(greifer.get("geschwindigkeit_m_pro_min"), None)
        a_greifer = as_float(greifer.get("beschleunigung_m_pro_s2"), None)

        # Hub/Katze/Kran
        m_seil = as_float(hub.get("seilgewicht_kg"), None)

        v_hub_mmin = as_float(hub.get("hub_geschwindigkeit_m_pro_min"), None)
        a_hub = as_float(hub.get("hub_beschleunigung_m_pro_s2"), None)
        eta_hub_getr = as_float(hub.get("wirkungsgrad_getriebe"), None)
        eta_seil = as_float(hub.get("wirkungsgrad_seiltrieb"), None)
        hub_stufen = to_int(hub.get("getriebestufen", 1), 1)
        hub_motoren = to_int(hub.get("anzahl_motoren", 1), 1)

        m_katze = as_float(katz.get("gewicht_kg"), None)
        v_katz_mmin = as_float(katz.get("geschwindigkeit_m_pro_min"), None)
        a_katz = as_float(katz.get("beschleunigung_m_pro_s2"), None)
        eta_katz_getr = as_float(katz.get("wirkungsgrad_getriebe"), None)
        katz_stufen = to_int(katz.get("getriebestufen", 1), 1)
        katz_motoren = to_int(katz.get("anzahl_motoren", 1), 1)
        fw_katz = as_float(katz.get("fahrwiderstand_kg_pro_t"), None)

        m_kran = as_float(kran.get("gewicht_kg"), None)
        v_kran_mmin = as_float(kran.get("geschwindigkeit_m_pro_min"), None)
        a_kran = as_float(kran.get("beschleunigung_m_pro_s2"), None)
        eta_kran_getr = as_float(kran.get("wirkungsgrad_getriebe"), None)
        kran_stufen = to_int(kran.get("getriebestufen", 1), 1)
        kran_motoren = to_int(kran.get("anzahl_motoren", 1), 1)
        fw_kran = as_float(kran.get("fahrwiderstand_kg_pro_t"), None)

        # Wege
        weg_hub = as_float(wege.get("weg_hebensenken_m"), None)
        weg_katz = as_float(wege.get("weg_katzfahrt_m"), None)
        weg_kran_einlager = as_float(wege.get("weg_kranfahrt_einlagern_m"), None)
        weg_oeffnen = as_float(wege.get("weg_oeffnen_schliessen_m"), None)

        st.markdown(f"### {label}")

        # ------------------------------------------------------------
        # Müll / Zyklen
        # ------------------------------------------------------------
        with st.expander("Müllmodell & Zyklen (pro Tag)", expanded=False):
            st.latex(r"m_\mathrm{einlager, Zyklus} = V \cdot \rho")
            st.latex(r"N_\mathrm{Zyklen/h} = \frac{\dot m_\mathrm{Anlieferung}}{m_\mathrm{einlager, Zyklus}}")
            st.latex(r"N_\mathrm{Zyklen/d} = N_\mathrm{Zyklen/h} \cdot t_\mathrm{Anlieferung}")

            if None in (n_trichter, verb_trichter, anliefer_h, V, rho_anliefer, rho_beschick, anlieferdauer):
                st.warning("Nicht alle Eingangsgrößen vorhanden (Anlage/Müll/Greifer).")
            else:
                muell_dict = muellberechnung(
                    to_int(n_trichter, 0),
                    as_float(verb_trichter),
                    as_float(anliefer_h),
                    as_float(V),
                    as_float(rho_beschick),
                    as_float(rho_anliefer),
                    as_float(anlieferdauer),
                )

                df_muell = pd.DataFrame({
                    "Größe": [
                        "Mülleinlagerung [kg/Zyklus]",
                        "Zyklen Einlagerung [1/d]",
                        "Zyklen Trichter gesamt [1/d]",
                    ],
                    "Wert": [
                        muell_dict["muelleinlagerung_kg_pro_zyklus"],
                        muell_dict["anzahl_zyklen_muelleinlagerung_pro_d"],
                        muell_dict["anzahl_zyklen_trichterbeschickung_gesamt_pro_d"],
                    ]
                })

                # --- Werte formatieren ---
                df_muell["Wert"] = df_muell["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_muell, use_container_width=True, hide_index=True)
                
        # ------------------------------------------------------------
        # Spielzeiten
        # ------------------------------------------------------------
        with st.expander("Spielzeiten", expanded=False):
            st.latex(r"v = \frac{v_{m/min}}{60}")
            st.latex(r"t_\mathrm{acc} = \frac{v}{a}")
            st.latex(r"s_\mathrm{acc} = \frac{1}{2} a t_\mathrm{acc}^2")
            st.latex(r"t_\mathrm{konst} = \frac{s - 2 s_\mathrm{acc}}{v}")
            st.latex(r"t_\mathrm{ges} = t_\mathrm{konst} + 2 t_\mathrm{acc}")

            def show_spiel(name: str, v_mmin: Any, a: Any, s: Any):
                v_mmin_f = as_float(v_mmin, None)
                a_f = as_float(a, None)
                s_f = as_float(s, None)
                if None in (v_mmin_f, a_f, s_f) or a_f == 0:
                    st.warning(f"{name}: fehlende Werte oder a=0.")
                    return None
                stw = spielzeitenberechnung(as_float(v_mmin_f), as_float(a_f), as_float(s_f))
                st.markdown(f"**{name}**")
                df = pd.DataFrame({
                    "Parameter": ["Beschleunigungszeit (t_acc) [s]", "Beschleunigungsweg (s_acc) [m]", "Zeit konstanter Bewegung (t_konst) [s]", "Gesamte Zeit (t_ges) [s]"],
                    "Wert": [
                        fmt_num(stw["beschleunigungszeit"], "", 3),
                        fmt_num(stw["beschleunigungsweg"], "", 3),
                        fmt_num(stw["kontinuierliche_zeit"], "", 3),
                        fmt_num(stw["summe_der_zeit"], "", 3),
                    ]
                })
                df = df.reset_index(drop=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
                return stw

            stw_hub = show_spiel("Hubwerk", v_hub_mmin, a_hub, weg_hub)
            stw_katz = show_spiel("Katzfahrt", v_katz_mmin, a_katz, weg_katz)
            stw_kran = show_spiel("Kranfahrt (Einlagern)", v_kran_mmin, a_kran, weg_kran_einlager)
            stw_greif = show_spiel("Greifer Öffnen/Schließen", v_greifer_mmin, a_greifer, weg_oeffnen)

        # ------------------------------------------------------------
        # Mechanik: Hubwerk
        # ------------------------------------------------------------
        with st.expander("Hubwerk – Leistungen", expanded=False):
            st.latex(r"P_\mathrm{beh}=\frac{m \cdot g \cdot v}{\eta}")
            st.latex(r"P_\mathrm{acc,mittel}=\frac{0.5 \cdot m \cdot v^2}{t_\mathrm{acc}\cdot \eta}")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, v_hub_mmin, eta_seil, eta_hub_getr) or not stw_hub:
                st.warning("Hubwerk: fehlende Eingangsgrößen.")
            else:
                hub_dict = mechleistunghubwerk(
                    gewicht_seile=as_float(m_seil),
                    gewicht_greifer_leer=as_float(m_greifer_leer),
                    greifer_volumen=as_float(V),
                    muell_dichte=as_float(rho_anliefer),
                    geschwindigkeit_mmin=as_float(v_hub_mmin),
                    beschleunigung_zeit=as_float(stw_hub["beschleunigungszeit"]),
                    wirkungsgrad_seiltrieb=as_float(eta_seil),
                    wirkungsgrad_getriebestufe=as_float(eta_hub_getr),
                    getriebestufen=int(hub_stufen),
                    motor_anzahl=int(hub_motoren),
                    )

                df_hub = pd.DataFrame({
                    "Größe": [
                        "Beharrungsleistung voll [kW]",
                        "Beschleunigungsleistung voll [kW]",
                        "Beharrungsleistung leer [kW]",
                        "Beschleunigungsleistung leer [kW]",
                    ],
                    "Wert": [
                        hub_dict["beharrungsleistung_voll"],
                        hub_dict["gesamtbeschleunigungsleistung_voll"],
                        hub_dict["beharrungsleistung_leer"],
                        hub_dict["gesamtbeschleunigungsleistung_leer"],
                    ]
                })

                # --- Werte formatieren ---
                df_hub["Wert"] = df_hub["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_hub, use_container_width=True, hide_index=True)
                
        # ------------------------------------------------------------
        # Mechanik: Katze
        # ------------------------------------------------------------
        with st.expander("Katzfahrt – Leistungen", expanded=False):
            st.latex(r"P_\mathrm{beh}=\frac{f \cdot m \cdot g \cdot v}{\eta}")
            st.latex(r"P_\mathrm{acc,mittel}=\frac{0.5 \cdot m \cdot v^2}{t_\mathrm{acc}\cdot \eta}")
            st.caption("Hinweis: Fahrwiderstand f in [kgf/t] → f = (kgf/t)/1000")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, m_katze, v_katz_mmin, fw_katz, eta_katz_getr) or not stw_katz:
                st.warning("Katzfahrt: fehlende Eingangsgrößen.")
            else:
                katz_dict = mechleistungkatzfahrt(
                    gewicht_seile=as_float(m_seil),
                    gewicht_greifer_leer=as_float(m_greifer_leer),
                    greifer_volumen=as_float(V),
                    muell_dichte=as_float(rho_anliefer),
                    gewicht_katze=as_float(m_katze),
                    geschwindigkeit_mmin=as_float(v_katz_mmin),
                    fahrwerkwiderstand=as_float(fw_katz),
                    getriebestufen=int(katz_stufen),
                    wirkungsgrad_getriebestufe=as_float(eta_katz_getr),
                    motorzahl=int(katz_motoren),
                    # ✅ Signature erwartet int -> cast
                    beschleunigungszeit=to_int(stw_katz["beschleunigungszeit"], 0),
                )

                df_katz = pd.DataFrame({
                    "Größe": [
                        "Beharrungsleistung voll [kW]",
                        "Beschleunigungsleistung voll [kW]",
                        "Beharrungsleistung leer [kW]",
                        "Beschleunigungsleistung leer [kW]",
                    ],
                    "Wert": [
                        katz_dict["beharrungsleistung"],
                        katz_dict["beschleunigungsleistungen"],
                        katz_dict["beharrungsleistung_leer"],
                        katz_dict["beschleunigungsleistungen_leer"],
                    ]
                })

                # --- Werte formatieren ---
                df_katz["Wert"] = df_katz["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_katz, use_container_width=True, hide_index=True)


        # ------------------------------------------------------------
        # Mechanik: Kran
        # ------------------------------------------------------------
        with st.expander("Kranfahrt – Leistungen", expanded=False):
            st.latex(r"P_\mathrm{beh}=\frac{f \cdot m \cdot g \cdot v}{\eta}")
            st.latex(r"P_\mathrm{acc,mittel}=\frac{0.5 \cdot m \cdot v^2}{t_\mathrm{acc}\cdot \eta}")
            st.caption("Hinweis: Fahrwiderstand f in [kgf/t] → f = (kgf/t)/1000")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, m_katze, m_kran, v_kran_mmin, fw_kran, eta_kran_getr) or not stw_kran:
                st.warning("Kranfahrt: fehlende Eingangsgrößen.")
            else:
                kran_dict = kranfahrt(
                    gewicht_greifer_leer=as_float(m_greifer_leer),
                    greifer_volumen=as_float(V),
                    muell_dichte=as_float(rho_anliefer),
                    gewicht_katze=as_float(m_katze),
                    gewicht_kran=as_float(m_kran),
                    gewicht_seile=as_float(m_seil),
                    geschwindigkeit_mmin=as_float(v_kran_mmin),
                    fahrwiderstand=as_float(fw_kran),
                    motoranzahl=int(kran_motoren),
                    wirkungsgrad_getriebestufe=as_float(eta_kran_getr),
                    getriebestufen=int(kran_stufen),
                    # ✅ Signature erwartet int -> cast
                    beschleunigungszeit=to_int(stw_kran["beschleunigungszeit"], 0),
                )

                df_kran = pd.DataFrame({
                    "Größe": [
                        "Beharrungsleistung voll [kW]",
                        "Beschleunigungsleistung voll [kW]",
                        "Beharrungsleistung leer [kW]",
                        "Beschleunigungsleistung leer [kW]",
                    ],
                    "Wert": [
                        kran_dict["beharrungsleistung"],
                        kran_dict["beschleunigungsleistungen"],
                        kran_dict["beharrungsleistung_leer"],
                        kran_dict["beschleunigungsleistungen_leer"],

                    ]
                })
                
                # --- Werte formatieren ---
                df_kran["Wert"] = df_kran["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_kran, use_container_width=True, hide_index=True)

        # ------------------------------------------------------------
        # Mechanik: Greifer: Vierseil vs Hydraulik
        # ------------------------------------------------------------
        with st.expander("Greifer – Leistung", expanded=False):
            st.markdown(f"**Greifertyp:** `Hydraulikgreifer`")

            p = as_float(greifer.get("betriebsdruck_bar"), None)
            q = as_float(greifer.get("volumenstrom_l_pro_min"), None)
            eta_h = as_float(greifer.get("wirkungsgrad_hydraulik"), None)

            st.latex(r"P_\mathrm{hydr}=\frac{p\cdot Q}{600}")
            if None in (p, q):
                st.warning("Hydraulikgreifer: p oder Q fehlt.")
            else:
                # ✅ Signature erwartet int -> cast
                h_dict = greiferhydraulik(
                    betriebsdruck=to_int(p, 0),
                    volumenstrom=to_int(q, 0),
                )

                df_h = pd.DataFrame ({
                    "Größe": [
                        "Hydraulikleistung [kW]",
                    ],
                    "Wert": [
                        h_dict["leistung_beharrung"],
                    ],
                })
                
                # --- Werte formatieren ---
                df_h["Wert"] = df_h["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_h, use_container_width=True, hide_index=True)

            st.markdown(f"**Greifertyp:** `Vierseil-Greifer`")
            st.caption("Erfahrungswert: Greiferleistung ≈ 1/3 der Hubwerksleistung (beharrend und beschleunigend).")
            st.latex(r"P_\mathrm{Greifer} = \frac{P_\mathrm{Hub}}{3}")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, v_hub_mmin, eta_seil, eta_hub_getr) or not stw_hub:
                st.warning("Vierseil: Hubwerk-Werte fehlen, um den 1/3-Ansatz zu zeigen.")
            else:
                hub_dict = mechleistunghubwerk(
                    gewicht_seile=as_float(m_seil),
                    gewicht_greifer_leer=as_float(m_greifer_leer),
                    greifer_volumen=as_float(V),
                    muell_dichte=as_float(rho_anliefer),
                    geschwindigkeit_mmin=as_float(v_hub_mmin),
                    beschleunigung_zeit=as_float(stw_hub["beschleunigungszeit"]),
                    wirkungsgrad_seiltrieb=as_float(eta_seil),
                    wirkungsgrad_getriebestufe=as_float(eta_hub_getr),
                    getriebestufen=int(hub_stufen),
                    motor_anzahl=int(hub_motoren),
                )

                v_dict = mechleistunggreifervierseil(
                    hub_dict["beharrungsleistung_voll"],
                    hub_dict["gesamtbeschleunigungsleistung_voll"],
                )

                df_v = pd.DataFrame ({
                    "Größe": [
                        "Beharrungsleistung [kW]",
                        "Beschleunigungsleistung [kW]",
                    ],
                    "Wert": [
                        v_dict["beharrungsleistung"],
                        v_dict["beschleunigungsleistung"],
                    ]
                })
                # --- Werte formatieren ---
                df_v["Wert"] = df_v["Wert"].apply(lambda x: fmt_num(x, "", 2))

                # --- Tabelle anzeigen ---
                st.markdown("##### Werte")
                st.dataframe(df_v, use_container_width=True, hide_index=True)
        
        # ------------------------------------------------------------
        # Mechanische Energie
        # ------------------------------------------------------------
        with st.expander("Mechanische Energie", expanded=False):
            st.latex(r"E_\mathrm{mech}=P_\mathrm{beh} \cdot t_\mathrm{beh} + P_\mathrm{bes} \cdot t_\mathrm{bes}")
            st.caption("Hinweis: Bei allen Vorgängen")

        # ------------------------------------------------------------
        # Rückspeisung
        # ------------------------------------------------------------
        with st.expander("Rückspeisung", expanded=False):
            st.latex(r"E_\mathrm{rück}=\frac{E_\mathrm{mech}} {\eta_\mathrm{motor}} \cdot {\eta_\mathrm{FU}}")
            st.caption("Hinweis: Bei allen Vorgängen, bei welchen Energie rückgespeist wird")

        # ------------------------------------------------------------
        # Elektrische Energie
        # ------------------------------------------------------------
        with st.expander("Elektrische Energie", expanded=False):
            st.latex(r"E_\mathrm{el}=\frac{E_\mathrm{mech}} {\eta_\mathrm{motor}} - E_\mathrm{rück}")
            st.caption("Hinweis: Bei allen Vorgängen")

        # ------------------------------------------------------------
        # Auswertung
        # ------------------------------------------------------------
        with st.expander("Auswertung", expanded=False):
            st.latex(r"E_\mathrm{el_{ges}}=\sum{E_\mathrm{el}} \cdot N_\mathrm{Zyklen/Zeit}")
            st.latex(r"E_\mathrm{rück_{ges}}=\sum{E_\mathrm{rück}} \cdot N_\mathrm{Zyklen/Zeit}")
            st.latex(r"Kosten=\sum{E_\mathrm{el}} \cdot Preis_\mathrm{kWh}")
            st.latex(r"CO_{2_{Jahr}}=\frac{E_\mathrm{el_{Jahr}} \cdot CO_2Faktor} {1000}")
            st.caption("Hinweis: Die Anzahl der Zyklen wird entsprechend des betrachteten Zeitraumes über die Spielzeiten berechnet")

    with tabs[0]:
        render_for(ist, "IST")
    if neu:
        with tabs[1]:
            render_for(neu, "NEU/SOLL")

    st.caption("Quelle für Formeln: Physikalische Grundsätze, Firmeninterne Berechnungsmethoden und Erfahrungswerte aus der Praxis.")


def render_strommix_table():
    st.subheader("⚡ Stromländerpreise + Strommix")

    df, co2_row = load_strommix_csv("tabellen/Stromländerpreise+CO2.csv")

    col1, col2 = st.columns([1, 1])
    with col1:
        country = st.selectbox("Land auswählen", ["(alle)"] + df["Land"].tolist(), key="src_country_select")

    view = df.copy()
    if country != "(alle)":
        view = view.loc[view["Land"] == country].copy()

    source_text = None
    if country != "(alle)" and "Quellen" in view.columns and not view.empty:
        source_text = view.iloc[0].get("Quellen", None)

    ordered = [
        "Land",
        "Preis in c/kWh",
        "Wasserkraft",
        "Solar",
        "Wind",
        "Atom",
        "Erdgas",
        "Kohle",
        "Öl",
        "Sonstiges",
        "Summe Strommix [%]",
    ]
    ordered = [c for c in ordered if c in view.columns]
    view = view[ordered]

    pct_cols = [
        c
        for c in ["Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges", "Summe Strommix [%]"]
        if c in view.columns
    ]
    fmt_map: dict[str, str] = {c: "{:.1f}" for c in pct_cols}
    if "Preis in c/kWh" in view.columns:
        fmt_map["Preis in c/kWh"] = "{:.2f}"

    st.dataframe(view.style.format(fmt_map, na_rep="—"), use_container_width=True, hide_index=True)

    st.caption("Quelle Strompreise:")
    st.caption("     https://de.statista.com/statistik/daten/studie/151260/umfrage//strompreise-fuer-industriekunden-in-europa/")
    st.caption("Quelle Strommix:")
    st.caption("     https://lowcarbonpower.org/de/, Stand 2024")

    if source_text:
        st.caption("Hinweis/Quellen (CSV-Zeile):")
        st.write(source_text)

    if co2_row is not None:
        st.subheader("🌍 CO₂-Faktoren")

        co2 = co2_row.copy()
        co2 = co2.drop(labels=["Land", "Quellen"], errors="ignore")

        items: list[dict[str, Any]] = []
        for k, v in co2.items():
            num = pd.to_numeric(v, errors="coerce")
            if pd.notna(num):
                items.append({"Energieträger": k, "CO₂-Faktor": as_float(num)})

        st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
        st.caption('Quelle CO₂-Faktoren außer "Sonstiges":')
        st.caption("     https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf, Table A.III.2")
        st.caption('CO₂-Faktor "Sonstiges" ist Durchschnittswert des Strommixes: ')
        st.caption("     https://www.iea.org/reports/electricity-2025/emissions")
        st.caption('Quelle CO₂-Faktor "Öl" :')
        st.caption(
            "     https://www.bafa.de/SharedDocs/Downloads/DE/Energie/eew_infoblatt_co2_faktoren_2022.pdf?__blob=publicationFile&v=6, Tabelle 2"
        )

# ------------------------------------------------------------
# Render page
# ------------------------------------------------------------

render_standards(STANDARDWERTE)
st.divider()

render_aktuelle_werte_ist_neu()
st.divider()

render_rechenweg()
st.divider()

render_strommix_table()
st.divider()
