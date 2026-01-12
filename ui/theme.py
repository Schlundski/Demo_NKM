import base64
from pathlib import Path
import streamlit as st

# Hintergrund hinzufügen, schaut professioneller aus

def _img_to_data_uri(path: str) -> str:
    p = Path(path)
    ext = p.suffix.lower().lstrip(".")
    if ext == "jpg":
        ext = "jpeg"

    data = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:image/{ext};base64,{data}"


def set_background_auto_theme(
    bg_light_path: str,
    bg_dark_path: str,
    *,
    # Content-Box, damit Text lesbar bleibt
    content_bg_light: str = "rgba(255, 255, 255, 0.78)",
    content_bg_dark: str = "rgba(0, 0, 0, 0.55)",
    border_radius_px: int = 14,
    padding_rem: float = 2.0,
):
    light_uri = _img_to_data_uri(bg_light_path)
    dark_uri = _img_to_data_uri(bg_dark_path)

    st.markdown(
        f"""
        <style>
        /* Default: Light */
        .stApp {{
            background-image: url("{light_uri}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Dark Mode */
        @media (prefers-color-scheme: dark) {{
            .stApp {{
                background-image: url("{dark_uri}");
            }}
        }}

        /* Content Container: Light */
        .block-container {{
            background: {content_bg_light};
            padding: {padding_rem}rem;
            border-radius: {border_radius_px}px;
        }}

        /* Content Container: Dark */
        @media (prefers-color-scheme: dark) {{
            .block-container {{
                background: {content_bg_dark};
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
