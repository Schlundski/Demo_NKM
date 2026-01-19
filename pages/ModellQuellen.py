# pages/Modell_Quellen.py
import pandas as pd
import streamlit as st

from config.standards import STANDARDWERTE

# ------------------------------------------------------------
# Page config
# ------------------------------------------------------------
st.set_page_config(page_title="Modell & Quellen", layout="centered")
st.title("📖 Modell & Quellen")
st.caption(
    "Diese Seite dient der Nachvollziehbarkeit der in der Auswertung dargestellten Ergebnisse "
    "(Annahmen, verwendete Tabellenwerte, Quellen und aktuell eingesetzte Parameter)."
)

# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def flatten_dict(d: dict, parent_key: str = "") -> list[dict]:
    rows = []
    for k, v in d.items():
        new_parent = f"{parent_key} / {k}" if parent_key else str(k)
        if isinstance(v, dict):
            rows.extend(flatten_dict(v, new_parent))
        else:
            rows.append({"Pfad": parent_key if parent_key else "ROOT", "Parameter": str(k), "Wert": v})
    return rows


def dict_get(dct: dict | None, path: str, default="—"):
    """Sicheres Holen aus verschachtelten Dicts via 'a.b.c'-Pfad."""
    if not isinstance(dct, dict):
        return default
    cur = dct
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


@st.cache_data(show_spinner=False)
def load_strommix_csv(path: str) -> tuple[pd.DataFrame, pd.Series | None]:
    """
    Liest eure CSV (;) ein.
    Trennt die letzte Zeile 'CO2Faktor' ab (falls vorhanden) und gibt sie als Series zurück.
    """
    df = pd.read_csv(path, sep=";", engine="python")
    df.columns = [c.strip() for c in df.columns]

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

    mix_cols = [c for c in ["Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges"] if c in df.columns]
    if mix_cols:
        df["Summe Strommix [%]"] = df[mix_cols].sum(axis=1, skipna=True)

    if "Preis in c/kWh" in df.columns:
        df["Preis in c/kWh"] = df["Preis in c/kWh"].round(2)

    if "Land" in df.columns:
        df = df.sort_values("Land")

    return df, co2_row


def sources_block(source_text: str | None, prefix: str = "Quellen:"):
    """Quellen/Kommentare schön unter einer Tabelle anzeigen."""
    if not source_text:
        return
    text = str(source_text).strip()
    if not text:
        return
    st.caption(f"{prefix} {text}")


# ------------------------------------------------------------
# Sections
# ------------------------------------------------------------
def render_standards(standards: dict):
    st.subheader("Standardwerte")
    st.write("Diese Werte sind lediglich Erfahrungs- und Durchschnittswerte und dienen nur als Orientierung")

    cats = list(standards.keys())
    tabs = st.tabs(cats)

    for tab, cat in zip(tabs, cats):
        with tab:
            val = standards[cat]

            if isinstance(val, dict) and cat == "Greifer":
                greifer_names = list(val.keys())
                sel = st.selectbox("Greifer-Modell", greifer_names, key="src_greifer_select")
                df = pd.DataFrame([{"Parameter": p, "Wert": w} for p, w in val[sel].items()])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                if isinstance(val, dict):
                    df = pd.DataFrame([{"Parameter": p, "Wert": w} for p, w in val.items()])
                    st.dataframe(df, use_container_width=True, hide_index=True)
                else:
                    st.write(val)

    with st.expander("Alles als flache Gesamtliste anzeigen"):
        flat = flatten_dict(standards)
        st.dataframe(pd.DataFrame(flat), use_container_width=True, hide_index=True)


def render_aktuelle_werte_ist_neu():
    st.subheader("🔎 Aktuell eingesetzte Werte (IST vs. NEU)")

    ist_anlage = st.session_state.get("ist_anlage", {})
    neu_anlage = st.session_state.get("neu_anlage", {})

    tabs = st.tabs(["IST", "NEU", "Vergleich"])

    def make_table(dct: dict):
        rows = [
            # Anlage
            ("Anlage", "Standort", dict_get(dct, "anlage.anlage_standort")),
            ("Anlage", "Anzahl Kräne", dict_get(dct, "anlage.anzahl_kraene")),
            ("Anlage", "Anzahl Trichter", dict_get(dct, "anlage.anzahl_trichter")),
            ("Anlage", "Verbrennung je Trichter [kg]", dict_get(dct, "anlage.verbrennung_trichter_kg")),
            ("Anlage", "Energiekosten [ct/kWh]", dict_get(dct, "anlage.energie_kosten")),
            ("Anlage", "Müll Anlieferung [kg/h]", dict_get(dct, "anlage.müll_anlieferung_h_kg")),
            ("Anlage", "Müll Anlieferdauer [h]", dict_get(dct, "anlage.müll_anlieferdauer")),
            ("Anlage", "Müll Dichte Beschickung [kg/m³]", dict_get(dct, "anlage.müll_dichte_beschickung_kg_pro_m3")),
            ("Anlage", "Müll Dichte Anlieferung [kg/m³]", dict_get(dct, "anlage.müll_dichte_anlieferung_kg_pro_m3")),

            # Greifer
            ("Greifer", "Typ", dict_get(dct, "greifer.typ")),
            ("Greifer", "Leergewicht [kg]", dict_get(dct, "greifer.leergewicht_kg")),
            ("Greifer", "Volumen [m³]", dict_get(dct, "greifer.volumen_m3")),
            ("Greifer", "Geschwindigkeit [m/min]", dict_get(dct, "greifer.geschwindigkeit_m_pro_min")),
            ("Greifer", "Beschleunigung [m/s²]", dict_get(dct, "greifer.beschleunigung_m_pro_s2")),
            ("Greifer", "Motorleistung [kW]", dict_get(dct, "greifer.motorleistung_kw")),
            ("Greifer", "Wirkungsgrad Hydraulik [-]", dict_get(dct, "greifer.wirkungsgrad_hydraulik")),
            ("Greifer", "Volumenstrom [l/min]", dict_get(dct, "greifer.volumenstrom_l_pro_min")),
            ("Greifer", "Betriebsdruck [bar]", dict_get(dct, "greifer.betriebsdruck_bar")),
            ("Greifer", "Anteil bewegte Masse [-]", dict_get(dct, "greifer.anteil_bew_masse")),

            # Wege
            ("Wege", "Heben/Senken [m]", dict_get(dct, "wege.weg_hebensenken_m")),
            ("Wege", "Katzfahrt [m]", dict_get(dct, "wege.weg_katzfahrt_m")),
            ("Wege", "Kranfahrt Einlagern [m]", dict_get(dct, "wege.weg_kranfahrt_einlagern_m")),
            ("Wege", "Öffnen/Schließen [m]", dict_get(dct, "wege.weg_oeffnen_schliessen_m")),
        ]
        return pd.DataFrame(rows, columns=["Kategorie", "Parameter", "Wert"])

    with tabs[0]:
        st.dataframe(make_table(ist_anlage), use_container_width=True, hide_index=True)

    with tabs[1]:
        st.dataframe(make_table(neu_anlage), use_container_width=True, hide_index=True)

    with tabs[2]:
        ist_df = make_table(ist_anlage).rename(columns={"Wert": "IST"})
        neu_df = make_table(neu_anlage).rename(columns={"Wert": "NEU"})
        cmp_df = ist_df.merge(neu_df, on=["Kategorie", "Parameter"], how="outer")

        def diff(a, b):
            try:
                a_num = float(a)
                b_num = float(b)
                return b_num - a_num
            except Exception:
                return "—"

        cmp_df["Δ (NEU-IST)"] = [diff(a, b) for a, b in zip(cmp_df["IST"], cmp_df["NEU"])]
        st.dataframe(cmp_df, use_container_width=True, hide_index=True)

        with st.expander("Hinweis"):
            st.markdown(
                "- `Δ` wird nur berechnet, wenn beide Werte numerisch sind.\n"
                "- Fehlende Werte erscheinen als „—“.\n"
                "- Wenn ihr weitere Felder anzeigen wollt: in `make_table()` einfach ergänzen."
            )


def render_strommix_table():
    st.subheader("⚡ Stromländerpreise + Strommix")

    df, co2_row = load_strommix_csv("tabellen/Stromländerpreise+CO2.csv")

    col1, col2 = st.columns([1, 1])
    with col1:
        country = st.selectbox("Land auswählen", ["(alle)"] + df["Land"].tolist(), key="src_country_select")
    with col2:
        show_sources = st.toggle("Quellen/Kommentare unter Tabelle anzeigen", value=True)

    view = df.copy()
    if country != "(alle)":
        view = view.loc[view["Land"] == country].copy()

    # Quellen/Kommentare einsammeln (auch bei "(alle)" wird es lang -> nur bei Einzelland anzeigen)
    source_text = None
    if show_sources and country != "(alle)" and "Quellen" in view.columns and not view.empty:
        source_text = view.iloc[0].get("Quellen", None)

    # Tabellenansicht OHNE Quellen-Spalte
    ordered = [
        "Land",
        "Preis in c/kWh",
        "Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges",
        "Summe Strommix [%]",
    ]
    ordered = [c for c in ordered if c in view.columns]
    view = view[ordered]

    pct_cols = [c for c in ["Wasserkraft", "Solar", "Wind", "Atom", "Erdgas", "Kohle", "Öl", "Sonstiges", "Summe Strommix [%]"] if c in view.columns]
    fmt = {c: "{:.1f}" for c in pct_cols}
    if "Preis in c/kWh" in view.columns:
        fmt["Preis in c/kWh"] = "{:.2f}"

    st.dataframe(view.style.format(fmt, na_rep="—"), use_container_width=True, hide_index=True)

    if show_sources and country == "(alle)":
        st.caption("Quellen/Kommentare werden bei „(alle)“ nicht einzeln angezeigt. Wähle ein Land, um die Quelle zu sehen.")
    else:
        sources_block(source_text, prefix="Quelle/Kommentar:")

    # CO2-Faktoren separat
    if co2_row is not None:
        st.subheader("🌍 CO₂-Faktoren")

        co2 = co2_row.copy()
        co2_src = co2.get("Quellen", None) if "Quellen" in co2.index else None
        co2 = co2.drop(labels=["Land", "Quellen"], errors="ignore")

        items = []
        for k, v in co2.items():
            num = pd.to_numeric(v, errors="coerce")
            if pd.notna(num):
                items.append({"Energieträger": k, "CO₂-Faktor (wie in CSV)": float(num)})

        st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
        sources_block(co2_src, prefix="Quelle/Kommentar (CO₂-Faktoren):")


def render_strommix_fuer_auswahl_ist_neu():
    st.subheader("📌 Strommix passend zum Standort (IST & NEU)")

    ist = st.session_state.get("ist_anlage", {})
    neu = st.session_state.get("neu_anlage", {})
    ist_land = dict_get(ist, "anlage.anlage_standort")
    neu_land = dict_get(neu, "anlage.anlage_standort")

    df, _ = load_strommix_csv("tabellen/Stromländerpreise+CO2.csv")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("**IST Standort**")
        if ist_land == "—":
            st.info("Kein IST-Standort gesetzt.")
        else:
            row = df.loc[df["Land"] == ist_land]
            if row.empty:
                st.warning(f"Kein CSV-Eintrag für IST '{ist_land}'.")
            else:
                # Quelle merken (Spalte ausblenden)
                src = row.iloc[0].get("Quellen", None) if "Quellen" in row.columns else None
                show = row.drop(columns=["Quellen"], errors="ignore")
                st.dataframe(show, use_container_width=True, hide_index=True)
                sources_block(src, prefix="Quelle/Kommentar (IST):")

    with col2:
        st.markdown("**NEU Standort**")
        if neu_land == "—":
            st.info("Kein NEU-Standort gesetzt.")
        else:
            row = df.loc[df["Land"] == neu_land]
            if row.empty:
                st.warning(f"Kein CSV-Eintrag für NEU '{neu_land}'.")
            else:
                src = row.iloc[0].get("Quellen", None) if "Quellen" in row.columns else None
                show = row.drop(columns=["Quellen"], errors="ignore")
                st.dataframe(show, use_container_width=True, hide_index=True)
                sources_block(src, prefix="Quelle/Kommentar (NEU):")


# ------------------------------------------------------------
# Render page
# ------------------------------------------------------------
render_aktuelle_werte_ist_neu()
st.divider()

render_standards(STANDARDWERTE)
st.divider()

render_strommix_table()
st.divider()

render_strommix_fuer_auswahl_ist_neu()
