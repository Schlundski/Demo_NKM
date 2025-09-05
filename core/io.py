import re
import pandas as pd

## Hier werden einfach die in presets.py über das zugehörige label in der UIausgewählte CSV Datei
## geladen und in floats, sowie ein session_state dictionary geladen, heißt in dem fall glaub ich jpac


def to_float(x, default=None):
    try:
        s = str(x).strip().replace(",", ".")
        return float(s)
    except Exception:
        return default


def parse_trichterwege(df: pd.DataFrame) -> list[float]:
    """
    Sucht alle Zeilen im Index, die 'Trichterweg <Nr>' enthalten,
    sortiert sie numerisch und gibt die Werte zurück.
    """
    trichter_zeilen = [
        idx for idx in df.index if str(idx).strip().lower().startswith("trichterweg")
    ]

    # nach Zahl sortieren
    trichter_zeilen.sort(
        key=lambda x: int(re.search(r"\d+", str(x)).group()) if re.search(r"\d+", str(x)) else 0
    )

    return [to_float(df.loc[idx, "Wert"], 0) for idx in trichter_zeilen]


def load_preset(csv_path: str, preset_name: str) -> dict:
    """
    CSV laden und in ein Preset-Dict umwandeln.
    """
    df = pd.read_csv(csv_path, sep=";", decimal=",", encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    df["Beschreibung"] = df["Beschreibung"].astype(str).str.strip()
    df.set_index("Beschreibung", inplace=True)
    df = df[~df.index.duplicated(keep="first")]

    def get(beschreibung: str, default=None):
        try:
            return df.loc[beschreibung, "Wert"]
        except Exception:
            return default

    return {
        "preset": preset_name,
        "allgemein": {
            "anzahl_kraene": int(to_float(get("Anzahl Kräne"), 0)),
            "anzahl_trichter": len(parse_trichterwege(df)),
            "verbrennung_pro_trichter_Mg_h": to_float(get("Verbrennung je Trichter"), 0),
        },
        "greifer": {
            "auswahl": "Manuell eingeben",
            "greiferart": str(get("Greiferart") or ""),
            "leergewicht_Mg": to_float(get("Greifer Leergewicht"), 0),
            "motorleistung_kW": to_float(get("Motorleistung Greifer in kW"), 0),
            "volumen_m3": to_float(get("Greifervolumen"), 0),
        },
        "muell": {
            "modus": "Standard",
            "gesamtmenge_Mg_a": to_float(get("Müllmenge im Jahr"), 0),
            "anliefermenge_Mg_h": to_float(get("Anliefermenge Stunde"), 0),
            "anlieferdauer_h": to_float(get("Anlieferdauer Stunden"), 0),
            "dichte_einlagerung_Mg_m3": to_float(get("Dichte Einlagerung"), 0),
            "dichte_beschickung_Mg_m3": to_float(get("Dichte Beschickung"), 0),
        },
        "referenzwege": {
            "heben_senken_m": to_float(get("Referenzweg Heben/Senken"), 0),
            "katzfahrt_m": to_float(get("Referenzweg Katzfahrt"), 0),
            "kranfahrt_m": to_float(get("Referenzweg Kranfahrt Einlagern"), 0),
            "oeffnen_schliessen_m": to_float(get("Referenzweg Öffnen/Schließen"), 0),
            "trichterwege_m": parse_trichterwege(df),
        },
        "geschwindigkeiten": {
            "heben_senken_m_min": to_float(get("Geschwindigkeit Heben/Senken"), 0),
            "katzfahrt_m_min": to_float(get("Geschwindigkeit Katzfahrt"), 0),
            "kranfahrt_m_min": to_float(get("Geschwindigkeit Kranfahrt"), 0),
            "oeffnen_schliessen_einh": to_float(get("Geschwindigkeit Öffnen/Schließen"), 0),
        },
        "beschleunigungen": {
            "heben_senken_m_s2": to_float(get("Beschleunigung Heben/Senken"), 0),
            "katzfahrt_m_s2": to_float(get("Beschleunigung Katzfahrt"), 0),
            "kranfahrt_m_s2": to_float(get("Beschleunigung Kranfahrt"), 0),
            "oeffnen_schliessen_m_s2": to_float(get("Beschleunigung Öffnen/Schließen"), 0),
        },
        "motoren": {
            "hub_kW": to_float(get("Nennleistung Hubmotor"), 0),
            "hub_wirkungsgrad_pct": to_float(get("Wirkungsgrad Hubmotor"), 0),
            "katz_kW": to_float(get("Nennleistung Katzfahrt"), 0),
            "katz_wirkungsgrad_pct": to_float(get("Wirkungsgrad Katzfahrt"), 0),
            "kran_kW": to_float(get("Nennleistung Kranfahrt"), 0),
            "kran_wirkungsgrad_pct": to_float(get("Wirkungsgrad Kranfahrt"), 0),
        },
    }
