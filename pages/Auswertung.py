import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Auswertung", page_icon="📊", layout="wide")
st.title("📊 Auswertung: Alt vs. Neu (live)")

# Modellannahmen
ETA_BY_FU = {
    "Standard": 0.88,
    "ABB AC880": 0.93,
    "Siemens S120": 0.94,
    "Siemens Masterdrive": 0.92,
}
REGEN_EFF = {
    "Standard": 0.10,
    "ABB AC880": 0.25,
    "Siemens S120": 0.30,
    "Siemens Masterdrive": 0.20,
}
GREIFER_FACTOR = {
    "-": 1.00,
    "Hydraulik-Greifer": 1.00,
    "Vier-Seil-Greifer": 1.05,
}

def regen_share_from(steuerung: str, v_mps: float) -> float:
    """Plausibler Reku-Zeitanteil [0..0.5] aus Steuerung + Geschwindigkeit."""
    base = 0.25 if steuerung == "Automatisch" else 0.20
    if v_mps >= 1.3:
        base += 0.05
    return float(np.clip(base, 0.0, 0.5))

def compute_metrics(hub_kw, fahr_kw, fu_type, h_per_year, price_eur_kwh,
                    co2_g_per_kwh, greifer_type="-", steuerung="Manuell", v_mps=1.0):
    p_total = max(hub_kw, 0.0) + max(fahr_kw, 0.0)                  # kW
    load_fac = GREIFER_FACTOR.get(greifer_type, 1.0)
    e_brutto = p_total * max(h_per_year, 0.0) * load_fac            # kWh/Jahr

    eta = ETA_BY_FU.get(fu_type, 0.9)
    e_el = e_brutto / max(eta, 1e-6)                                # kWh

    regen_share = regen_share_from(steuerung, v_mps)
    regen_eff   = REGEN_EFF.get(fu_type, 0.2)
    e_reku = e_el * regen_share * regen_eff                         # kWh

    e_netto = max(e_el - e_reku, 0.0)
    co2_kg  = e_netto * (co2_g_per_kwh / 1000.0)
    kosten  = e_netto * price_eur_kwh
    return dict(E_netto_kWh=e_netto, CO2_kg=co2_kg, Kosten_EUR=kosten)

def _f(x, default=0.0):
    """sicher zu float casten"""
    try:
        return float(x)
    except Exception:
        return float(default)

# Baseline prüfen
if "baseline" not in st.session_state:
    st.error("Es sind keine Basisdaten vorhanden. Bitte zuerst auf der Seite **Faktoren** speichern.")
    st.stop()

base = st.session_state["baseline"]
# erwartete Keys: hub_kw, fahr_kw, fu, betriebsstunden, preis_eur_kwh, co2_g_kwh

# Eingaben für NEU
colA, colN = st.columns(2)

with colA:
    st.subheader("🔴 Alt")
    st.write(f"**FU‑Typ**: {base['fu']}")
    st.write(f"**Hub/Fahr**: {_f(base['hub_kw']):.1f} / {_f(base['fahr_kw']):.1f} kW")
    st.write(f"**Betriebsstunden/Jahr**: {int(_f(base['betriebsstunden']))}")
    st.write(f"**Preis**: {_f(base['preis_eur_kwh']):.2f} €/kWh")
    st.write(f"**CO₂‑Faktor**: {_f(base['co2_g_kwh']):.0f} g/kWh")

with colN:
    st.subheader("🟢 Neu")
    greifer_neu   = st.selectbox("Greiferart (neu)", ["-","Vier-Seil-Greifer","Hydraulik-Greifer"], index=1)
    steuerung_neu = st.selectbox("Steuerungsart (neu)", ["Manuell","Automatisch"], index=1)
    hub_neu  = st.number_input("Hubmotorleistung kW (neu)", 0.0, 5000.0, _f(base["hub_kw"]), 5.0)
    fahr_neu = st.number_input("Fahrmotorleistung kW (neu)", 0.0, 5000.0, _f(base["fahr_kw"]), 5.0)
    fu_neu   = st.selectbox("Frequenzumrichter (neu)", list(ETA_BY_FU.keys()),
                             index=list(ETA_BY_FU.keys()).index(base["fu"]) if base["fu"] in ETA_BY_FU else 0)
    v_neu    = st.number_input("Durchschnittliche Geschwindigkeit m/s (neu)", 0.0, 10.0, 1.2, 0.1)

# Rechnen
alt_metrics = compute_metrics(
    hub_kw=_f(base["hub_kw"]), fahr_kw=_f(base["fahr_kw"]), fu_type=base["fu"],
    h_per_year=int(_f(base["betriebsstunden"])), price_eur_kwh=_f(base["preis_eur_kwh"]),
    co2_g_per_kwh=_f(base["co2_g_kwh"]), greifer_type="-", steuerung="Manuell", v_mps=1.2
)
neu_metrics = compute_metrics(
    hub_kw=_f(hub_neu), fahr_kw=_f(fahr_neu), fu_type=fu_neu,
    h_per_year=int(_f(base["betriebsstunden"])), price_eur_kwh=_f(base["preis_eur_kwh"]),
    co2_g_per_kwh=_f(base["co2_g_kwh"]), greifer_type=greifer_neu,
    steuerung=steuerung_neu, v_mps=_f(v_neu, 1.2)
)

# Neu − Alt
dE   = _f(neu_metrics["E_netto_kWh"] - alt_metrics["E_netto_kWh"])
dCO2 = _f(neu_metrics["CO2_kg"]      - alt_metrics["CO2_kg"])
dEUR = _f(neu_metrics["Kosten_EUR"]  - alt_metrics["Kosten_EUR"])

# Energie
st.divider()
st.subheader("Energie")

E_alt = _f(alt_metrics["E_netto_kWh"])
E_neu = _f(neu_metrics["E_netto_kWh"])

c1, c2 = st.columns(2)
with c1:
    st.metric("Energie Alt [kWh/J]", f"{E_alt:,.0f}")
with c2:
    st.metric("Energie Neu [kWh/J]", f"{E_neu:,.0f}",
              delta=f"{dE:,.0f} kWh", delta_color="inverse")

df_energy = pd.DataFrame({
    "Szenario": ["Alt", "Neu"],
    "Wert": [E_alt, E_neu],
})
df_energy["Wert"] = pd.to_numeric(df_energy["Wert"], errors="coerce").fillna(0.0)
st.bar_chart(df_energy, x="Szenario", y="Wert")

# CO²
st.divider()
st.subheader("CO₂")

CO2_alt = _f(alt_metrics["CO2_kg"])
CO2_neu = _f(neu_metrics["CO2_kg"])

c3, c4 = st.columns(2)
with c3:
    st.metric("CO₂ Alt [kg/J]", f"{CO2_alt:,.0f}")
with c4:
    st.metric("CO₂ Neu [kg/J]", f"{CO2_neu:,.0f}",
              delta=f"{dCO2:,.0f} kg", delta_color="inverse")

df_co2 = pd.DataFrame({
    "Szenario": ["Alt", "Neu"],
    "Wert": [CO2_alt, CO2_neu],
})
df_co2["Wert"] = pd.to_numeric(df_co2["Wert"], errors="coerce").fillna(0.0)
st.bar_chart(df_co2, x="Szenario", y="Wert")

#Kosten
st.divider()
st.subheader("Kosten")

EUR_alt = _f(alt_metrics["Kosten_EUR"])
EUR_neu = _f(neu_metrics["Kosten_EUR"])

c5, c6 = st.columns(2)
with c5:
    st.metric("Kosten Alt [€/J]", f"{EUR_alt:,.0f}")
with c6:
    st.metric("Kosten Neu [€/J]", f"{EUR_neu:,.0f}",
              delta=f"{dEUR:,.0f} €", delta_color="inverse")

df_cost = pd.DataFrame({
    "Szenario": ["Alt", "Neu"],
    "Wert": [EUR_alt, EUR_neu],
})
df_cost["Wert"] = pd.to_numeric(df_cost["Wert"], errors="coerce").fillna(0.0)
st.bar_chart(df_cost, x="Szenario", y="Wert")

st.write("## Hier könnte die Amortisierung stehen.")
