# pages/ModellQuellen.py
import math
import pandas as pd
import streamlit as st

from config.standards import STANDARDWERTE

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
st.set_page_config(page_title="Modell & Quellen", layout="centered")
st.title("📖 Modell & Quellen")
st.caption(
    "Diese Seite dient der Nachvollziehbarkeit der in der Auswertung dargestellten Ergebnisse "
    "(Annahmen, verwendete Tabellenwerte, Quellen und aktuell eingesetzte Parameter). "
    "Zusätzlich wird der Rechenweg mit Formeln und eingesetzten Werten (IST & NEU/SOLL) nachvollziehbar dargestellt."
)
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


def as_float(x, default=None):
    try:
        if x is None:
            return default
        if isinstance(x, str) and x.strip() in ("", "—"):
            return default
        return float(x)
    except Exception:
        return default


def fmt_num(x, unit: str = "", digits: int = 3, fallback: str = "—"):
    v = as_float(x, None)
    if v is None or (isinstance(v, float) and (math.isnan(v) or math.isinf(v))):
        return fallback
    s = f"{v:.{digits}f}"
    return f"{s} {unit}".rstrip()


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

def render_standards(standards: dict):
    st.subheader("Standardwerte")
    st.write("Diese Werte sind firmeninterne Erfahrungs- und Durchschnittswerte und dienen nur als Orientierung")

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
    st.subheader("🔎 Aktuell eingesetzte Werte (IST vs. NEU/SOLL)")

    ist_anlage = st.session_state.get("ist_anlage", {})
    neu_anlage = st.session_state.get("neu_anlage", {})

    tabs = st.tabs(["IST", "NEU/SOLL", "Vergleich"])

    def make_table(dct: dict):
        rows = [
            # Anlage
            ("Anlage", "Standort", dict_get(dct, "anlage.anlage_standort")),
            ("Anlage", "Anzahl Kräne", dict_get(dct, "anlage.anzahl_kraene")),
            ("Anlage", "Anzahl Trichter", dict_get(dct, "anlage.anzahl_trichter")),
            ("Anlage", "Verbrennung je Trichter [kg/h]", dict_get(dct, "anlage.verbrennung_trichter_kg")),
            ("Anlage", "Energiekosten [ct/kWh]", dict_get(dct, "anlage.energie_kosten")),
            ("Anlage", "Müll Anlieferung [kg/h]", dict_get(dct, "anlage.müll_anlieferung_h_kg")),
            ("Anlage", "Müll Anlieferdauer [h/d]", dict_get(dct, "anlage.müll_anlieferdauer")),
            ("Anlage", "Müll Dichte Beschickung [kg/m³]", dict_get(dct, "anlage.müll_dichte_beschickung_kg_pro_m3")),
            ("Anlage", "Müll Dichte Anlieferung [kg/m³]", dict_get(dct, "anlage.müll_dichte_anlieferung_kg_pro_m3")),

            # Greifer
            ("Greifer", "Typ", dict_get(dct, "greifer.typ")),
            ("Greifer", "Leergewicht [kg]", dict_get(dct, "greifer.leergewicht_kg")),
            ("Greifer", "Volumen [m³]", dict_get(dct, "greifer.volumen_m3")),
            ("Greifer", "Geschwindigkeit [m/min]", dict_get(dct, "greifer.geschwindigkeit_m_pro_min")),
            ("Greifer", "Beschleunigung [m/s²]", dict_get(dct, "greifer.beschleunigung_m_pro_s2")),
            ("Greifer", "Wirkungsgrad Hydraulik [-]", dict_get(dct, "greifer.wirkungsgrad_hydraulik")),
            ("Greifer", "Volumenstrom [l/min]", dict_get(dct, "greifer.volumenstrom_l_pro_min")),
            ("Greifer", "Betriebsdruck [bar]", dict_get(dct, "greifer.betriebsdruck_bar")),

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
        neu_df = make_table(neu_anlage).rename(columns={"Wert": "NEU/SOLL"})
        cmp_df = ist_df.merge(neu_df, on=["Kategorie", "Parameter"], how="outer")

        def diff(a, b):
            try:
                a_num = float(a)
                b_num = float(b)
                return b_num - a_num
            except Exception:
                return "—"

        cmp_df["Δ (NEU-IST)"] = [diff(a, b) for a, b in zip(cmp_df["IST"], cmp_df["NEU/SOLL"])]
        st.dataframe(cmp_df, use_container_width=True, hide_index=True)

        with st.expander("Hinweis"):
            st.markdown(
                "- `Δ` wird nur berechnet, wenn beide Werte numerisch sind.\n"
                "- Fehlende Werte erscheinen als „—“.\n"
                "- Wenn ihr weitere Felder anzeigen wollt: in `make_table()` einfach ergänzen."
            )

def render_rechenweg():
    st.subheader("🧮 Rechenweg (Formeln + eingesetzte Werte)")

    ist = st.session_state.get("ist_anlage", None)
    neu = st.session_state.get("neu_anlage", None)

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
        anliefer_h = as_float(anlage.get("müll_anlieferung_h_kg"), None)       # kg/h
        anlieferdauer = as_float(anlage.get("müll_anlieferdauer"), None)      # h/d

        rho_beschick = as_float(anlage.get("müll_dichte_beschickung_kg_pro_m3"), None)
        rho_anliefer = as_float(anlage.get("müll_dichte_anlieferung_kg_pro_m3"), None)

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
        hub_stufen = int(hub.get("getriebestufen", 1) or 1)
        hub_motoren = int(hub.get("anzahl_motoren", 1) or 1)

        m_katze = as_float(katz.get("gewicht_kg"), None)
        v_katz_mmin = as_float(katz.get("geschwindigkeit_m_pro_min"), None)
        a_katz = as_float(katz.get("beschleunigung_m_pro_s2"), None)
        eta_katz_getr = as_float(katz.get("wirkungsgrad_getriebe"), None)
        katz_stufen = int(katz.get("getriebestufen", 1) or 1)
        katz_motoren = int(katz.get("anzahl_motoren", 1) or 1)
        fw_katz = as_float(katz.get("fahrwiderstand_kg_pro_t"), None)

        m_kran = as_float(kran.get("gewicht_kg"), None)
        v_kran_mmin = as_float(kran.get("geschwindigkeit_m_pro_min"), None)
        a_kran = as_float(kran.get("beschleunigung_m_pro_s2"), None)
        eta_kran_getr = as_float(kran.get("wirkungsgrad_getriebe"), None)
        kran_stufen = int(kran.get("getriebestufen", 1) or 1)
        kran_motoren = int(kran.get("anzahl_motoren", 1) or 1)
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
                df_muell = muellberechnung(
                    int(n_trichter),
                    float(verb_trichter),
                    float(anliefer_h),
                    float(V),
                    float(rho_beschick),
                    float(rho_anliefer),
                    float(anlieferdauer),
                )
                # kompakt anzeigen
                st.table({
                    "Größe": [
                        "Mülleinlagerung [kg/Zyklus]",
                        "Zyklen Einlagerung [1/d]",
                        "Zyklen Trichter gesamt [1/d]",
                    ],
                    "Wert": [
                        fmt_num(df_muell["Mülleinlagerung kg / Zyklus"], "kg", 1),
                        fmt_num(df_muell["Anzahl Zyklen Mülleinlagerung / d"], "1/d", 2),
                        fmt_num(df_muell["Anzahl Zyklen Trichterbeschickung gesamt / d"], "1/d", 2),
                    ]
                })

        # ------------------------------------------------------------
        # Spielzeiten
        # ------------------------------------------------------------
        with st.expander("Spielzeiten (Trapezprofil, linear a)", expanded=False):
            st.latex(r"v = \frac{v_{m/min}}{60}")
            st.latex(r"t_\mathrm{acc} = \frac{v}{a}")
            st.latex(r"s_\mathrm{acc} = \frac{1}{2} a t_\mathrm{acc}^2")
            st.latex(r"t_\mathrm{konst} = \frac{s - 2 s_\mathrm{acc}}{v}")
            st.latex(r"t_\mathrm{ges} = t_\mathrm{konst} + 2 t_\mathrm{acc}")

            def show_spiel(name, v_mmin, a, s):
                if None in (v_mmin, a, s) or a == 0:
                    st.warning(f"{name}: fehlende Werte oder a=0.")
                    return None
                stw = spielzeitenberechnung(v_mmin, a, s)
                st.markdown(f"**{name}**")
                st.table({
                    "Parameter": ["t_acc", "s_acc", "t_konst", "t_ges"],
                    "Wert": [
                        fmt_num(stw["Beschleunigungszeit"], "s", 3),
                        fmt_num(stw["Beschleunigungsweg"], "m", 3),
                        fmt_num(stw["Kontinuierliche Zeit"], "s", 3),
                        fmt_num(stw["Summe der Zeit"], "s", 3),
                    ]
                })
                return stw

            stw_hub = show_spiel("Hubwerk", v_hub_mmin, a_hub, weg_hub)
            stw_katz = show_spiel("Katzfahrt", v_katz_mmin, a_katz, weg_katz)
            stw_kran = show_spiel("Kranfahrt (Einlagern)", v_kran_mmin, a_kran, weg_kran_einlager)
            stw_greif = show_spiel("Greifer Öffnen/Schließen", v_greifer_mmin, a_greifer, weg_oeffnen)

        # ------------------------------------------------------------
        # Mechanik: Hubwerk
        # ------------------------------------------------------------
        with st.expander("Hubwerk – Leistungen (mit Formel + Einsetzen)", expanded=False):
            st.latex(r"P_\mathrm{beh}=\frac{m \cdot g \cdot v}{\eta}")
            st.latex(r"P_\mathrm{acc,mittel}=\frac{0.5 \cdot m \cdot v^2}{t_\mathrm{acc}\cdot \eta}")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, v_hub_mmin, eta_seil, eta_hub_getr) or not stw_hub:
                st.warning("Hubwerk: fehlende Eingangsgrößen.")
            else:
                df_hub = mechleistunghubwerk(
                    gewicht_seile=float(m_seil),
                    gewicht_greifer_leer=float(m_greifer_leer),
                    greifer_volumen=float(V),
                    muell_dichte=float(rho_anliefer),
                    geschwindigkeit_mmin=float(v_hub_mmin),
                    beschleunigung_zeit=float(stw_hub["Beschleunigungszeit"]),
                    wirkungsgrad_seiltrieb=float(eta_seil),
                    wirkungsgrad_getriebestufe=float(eta_hub_getr),
                    getriebestufen=int(hub_stufen),
                    motor_anzahl=int(hub_motoren),
                )

                # Einsetzen für "voll" (Einlagerung)
                v_ms = float(v_hub_mmin) / 60.0
                eta_ges = (float(eta_hub_getr) ** int(hub_stufen)) * float(eta_seil)
                m_voll = float(m_seil) + (float(V) * float(rho_anliefer) + float(m_greifer_leer))
                tacc = float(stw_hub["Beschleunigungszeit"])

                st.latex(
                    rf"P_\mathrm{{beh}} = \frac{{{m_voll:.0f}\cdot 9.81 \cdot {v_ms:.4f}}}{{{eta_ges:.4f}}}\cdot\frac{{1}}{{1000}}"
                    rf" = {df_hub['Beharrungsleistung voll']:.3f}\ \mathrm{{kW}}"
                )
                st.latex(
                    rf"P_\mathrm{{acc}} = \frac{{0.5\cdot {m_voll:.0f}\cdot {v_ms:.4f}^2}}{{{tacc:.4f}\cdot {eta_ges:.4f}}}\cdot\frac{{1}}{{1000}}"
                    rf" = {df_hub['Gesamtbeschleunigungsleistung voll']:.3f}\ \mathrm{{kW}}"
                )

        # ------------------------------------------------------------
        # Mechanik: Katze & Kran
        # ------------------------------------------------------------
        with st.expander("Katzfahrt & Kranfahrt – Leistungen", expanded=False):
            st.latex(r"P_\mathrm{beh}=\frac{f \cdot m \cdot g \cdot v}{\eta}")
            st.latex(r"P_\mathrm{acc,mittel}=\frac{0.5 \cdot m \cdot v^2}{t_\mathrm{acc}\cdot \eta}")
            st.caption("Hinweis: Fahrwiderstand als kgf/t → f = (kgf/t)/1000 (dimensionslos).")

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, m_katze, v_katz_mmin, fw_katz, eta_katz_getr) or not stw_katz:
                st.warning("Katzfahrt: fehlende Eingangsgrößen.")
            else:
                df_katz = mechleistungkatzfahrt(
                    gewicht_seile=float(m_seil),
                    gewicht_greifer_leer=float(m_greifer_leer),
                    greifer_volumen=float(V),
                    muell_dichte=float(rho_anliefer),
                    gewicht_katze=float(m_katze),
                    geschwindigkeit_mmin=float(v_katz_mmin),
                    fahrwerkwiderstand=float(fw_katz),
                    getriebestufen=int(katz_stufen),
                    wirkungsgrad_getriebestufe=float(eta_katz_getr),
                    motorzahl=int(katz_motoren),
                    beschleunigungszeit=float(stw_katz["Beschleunigungszeit"]),
                )
                st.table({
                    "Katzfahrt": ["P_beh (voll)", "P_acc (voll)", "P_beh (leer)", "P_acc (leer)"],
                    "kW": [
                        fmt_num(df_katz["Beharrungsleistung"], "kW", 3),
                        fmt_num(df_katz["Beschleunigungsleistungen"], "kW", 3),
                        fmt_num(df_katz["Beharrungsleistung_leer"], "kW", 3),
                        fmt_num(df_katz["Beschleunigungsleistungen_leer"], "kW", 3),
                    ]
                })

            if None in (m_seil, m_greifer_leer, V, rho_anliefer, m_katze, m_kran, v_kran_mmin, fw_kran, eta_kran_getr) or not stw_kran:
                st.warning("Kranfahrt: fehlende Eingangsgrößen.")
            else:
                df_kran = kranfahrt(
                    gewicht_greifer_leer=float(m_greifer_leer),
                    greifer_volumen=float(V),
                    muell_dichte=float(rho_anliefer),
                    gewicht_katze=float(m_katze),
                    gewicht_kran=float(m_kran),
                    gewicht_seile=float(m_seil),
                    geschwindigkeit_mmin=float(v_kran_mmin),
                    fahrwiderstand=float(fw_kran),
                    motoranzahl=int(kran_motoren),
                    wirkungsgrad_getriebestufe=float(eta_kran_getr),
                    getriebestufen=int(kran_stufen),
                    beschleunigungszeit=float(stw_kran["Beschleunigungszeit"]),
                )
                st.table({
                    "Kranfahrt": ["P_beh (voll)", "P_acc (voll)", "P_beh (leer)", "P_acc (leer)"],
                    "kW": [
                        fmt_num(df_kran["Beharrungsleistung"], "kW", 3),
                        fmt_num(df_kran["Beschleunigungsleistungen"], "kW", 3),
                        fmt_num(df_kran["Beharrungsleistung_leer"], "kW", 3),
                        fmt_num(df_kran["Beschleunigungsleistungen_leer"], "kW", 3),
                    ]
                })

        # ------------------------------------------------------------
        # Greifer: Vierseil vs Hydraulik
        # ------------------------------------------------------------
        with st.expander("Greifer – Rechenweg", expanded=False):
            st.markdown(f"**Greifertyp:** `{greifer_typ}`")

            if greifer_typ == "Hydraulikgreifer":
                p = as_float(greifer.get("betriebsdruck_bar"), None)
                q = as_float(greifer.get("volumenstrom_l_pro_min"), None)
                eta_h = as_float(greifer.get("wirkungsgrad_hydraulik"), None)

                st.latex(r"P_\mathrm{hydr}=\frac{p\cdot Q}{600}")
                if None in (p, q):
                    st.warning("Hydraulikgreifer: p oder Q fehlt.")
                else:
                    df_h = greiferhydraulik(betriebsdruck=float(p), volumenstrom=float(q))
                    p_hyd = df_h["Leistung Beharrung"]
                    st.latex(rf"P_\mathrm{{hydr}}=\frac{{{p:.1f}\cdot {q:.1f}}}{{600}} = {p_hyd:.3f}\ \mathrm{{kW}}")
                    if eta_h is not None and eta_h > 0:
                        st.latex(rf"P_\mathrm{{el}}=\frac{{P_\mathrm{{hydr}}}}{{\eta}}=\frac{{{p_hyd:.3f}}}{{{eta_h:.3f}}} = {(p_hyd/eta_h):.3f}\ \mathrm{{kW}}")
                    else:
                        st.caption("Hinweis: Wirkungsgrad Hydraulik nicht gesetzt oder 0 → elektrische Leistung kann nicht sauber umgerechnet werden.")

            elif greifer_typ == "Vierseil-Greifer":
                st.caption("Erfahrungswert: Greiferleistung ≈ 1/3 der Hubwerksleistung (beharrend und beschleunigend).")
                st.latex(r"P_\mathrm{Greifer} = \frac{1}{3} P_\mathrm{Hub}")

                # Wir zeigen das mit den zuvor berechneten Hubwerten (sofern vorhanden)
                if None in (m_seil, m_greifer_leer, V, rho_anliefer, v_hub_mmin, eta_seil, eta_hub_getr) or not stw_hub:
                    st.warning("Vierseil: Hubwerk-Werte fehlen, um den 1/3-Ansatz zu zeigen.")
                else:
                    df_hub = mechleistunghubwerk(
                        gewicht_seile=float(m_seil),
                        gewicht_greifer_leer=float(m_greifer_leer),
                        greifer_volumen=float(V),
                        muell_dichte=float(rho_anliefer),
                        geschwindigkeit_mmin=float(v_hub_mmin),
                        beschleunigung_zeit=float(stw_hub["Beschleunigungszeit"]),
                        wirkungsgrad_seiltrieb=float(eta_seil),
                        wirkungsgrad_getriebestufe=float(eta_hub_getr),
                        getriebestufen=int(hub_stufen),
                        motor_anzahl=int(hub_motoren),
                    )
                    g = mechleistunggreifervierseil(
                        df_hub["Beharrungsleistung voll"],
                        df_hub["Gesamtbeschleunigungsleistung voll"],
                    )
                    st.table({
                        "Greifer (1/3 Hub)": ["P_beh", "P_acc"],
                        "kW": [fmt_num(g["Beharrungsleistung"], "kW", 3), fmt_num(g["Beschleunigungsleistung"], "kW", 3)]
                    })
            else:
                st.info("Unbekannter Greifertyp oder noch nicht gewählt.")

    # Render tabs
    with tabs[0]:
        render_for(ist, "IST")
    if neu:
        with tabs[1]:
            render_for(neu, "NEU/SOLL")

    st.caption("Quelle für Formeln: Firmeninterne Berechnungsmethoden und Erfahrungswerte aus der Praxis.")

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

    source_text = None
    if show_sources and country != "(alle)" and "Quellen" in view.columns and not view.empty:
        source_text = view.iloc[0].get("Quellen", None)

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

    st.caption("Quelle Strompreise:")  
    st.caption("     https://de.statista.com/statistik/daten/studie/151260/umfrage//strompreise-fuer-industriekunden-in-europa/")                    
    st.caption("Quelle Strommix:")
    st.caption("     https://lowcarbonpower.org/de/, Stand 2024")


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
        st.caption("Quelle CO₂-Faktoren außer \"Sonstiges\":")
        st.caption("     https://www.ipcc.ch/site/assets/uploads/2018/02/ipcc_wg3_ar5_annex-iii.pdf, Table A.III.2")
        st.caption("CO2Faktor \"Sonstiges\" ist Durchschnittswert des Strommixes: ")
        st.caption("     https://www.iea.org/reports/electricity-2025/emissions")

# ------------------------------------------------------------
# Render page
# ------------------------------------------------------------
render_aktuelle_werte_ist_neu()
st.divider()

render_rechenweg()
st.divider()

render_standards(STANDARDWERTE)
st.divider()

render_strommix_table()
st.divider()

