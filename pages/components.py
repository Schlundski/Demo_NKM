from typing import Union
import streamlit as st

Number = Union[int, float]

def number_with_standard_row(
    label: str,
    key: str,
    default: Number,
    *,
    min_value: Number | None = None,
    max_value: Number | None = None,
    step: Number | None = None,
    fmt: str | None = None,
    help: str | None = None,
    use_default_init: bool = True,
) -> Number:
    # Zeile 1: Label + Checkbox
    c_label, c_toggle = st.columns([5, 2])
    with c_label:
        st.markdown(f"**{label}**")
    with c_toggle:
        use_default = st.checkbox(
            "Standard",
            value=use_default_init,
            key=f"{key}__use_default",
            help="Standardwert verwenden",
        )

    is_int = isinstance(default, int) and not isinstance(default, bool)
    init_val = int(default) if is_int else float(default)

    # Zeile 2: Eingabebox über volle Breite (Label ausgeblendet)
    if is_int:
        val = st.number_input(
            label,
            value=init_val,
            min_value=None if min_value is None else int(min_value),
            max_value=None if max_value is None else int(max_value),
            step=1 if step is None else int(step),
            disabled=use_default,
            key=f"{key}__value",
            help=help,
            label_visibility="collapsed",
        )
        return default if use_default else int(val)
    else:
        val = st.number_input(
            label,
            value=init_val,
            min_value=None if min_value is None else float(min_value),
            max_value=None if max_value is None else float(max_value),
            step=step,
            format=fmt if fmt else None,
            disabled=use_default,
            key=f"{key}__value",
            help=help,
            label_visibility="collapsed",
        )
        return default if use_default else float(val)
