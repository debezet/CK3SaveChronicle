from __future__ import annotations

import unicodedata

# Conservative map for CK3/Paradox escaped first_name values observed in saves.
PDS_ESCAPED_CHARS: dict[str, str] = {
    "A_": "ą", "C_": "ć", "E_": "ę", "L_": "ł", "N_": "ń",
    "O_": "ó", "S_": "ś", "Z_": "ż", "X_": "ź",
    "a_": "ą", "c_": "ć", "e_": "ę", "l_": "ł", "n_": "ń",
    "o_": "ó", "s_": "ś", "z_": "ż", "x_": "ź",
}

MOJIBAKE_REPAIRS: dict[str, str] = {
    "Å‚": "ł", "Å›": "ś", "Å¼": "ż", "Åº": "ź",
    "Ä…": "ą", "Ä‡": "ć", "Ä™": "ę", "Å„": "ń", "Ã³": "ó",
}

def normalize_name(value: str | None) -> str | None:
    """Return display-safe version of a CK3 name.

    Raw names should still be kept in data structures for debugging.
    """
    if value is None:
        return None

    out = value
    for escaped, decoded in PDS_ESCAPED_CHARS.items():
        out = out.replace(escaped, decoded)
    for bad, good in MOJIBAKE_REPAIRS.items():
        out = out.replace(bad, good)

    return unicodedata.normalize("NFC", out)

def normalize_text(value: str | None) -> str | None:
    return normalize_name(value)
