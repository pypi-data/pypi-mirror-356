# -----------------------------
# File: yemot_router/utils.py
# -----------------------------
"""Utility helpers (time, encoding, sanitising)."""
from __future__ import annotations

import time
import urllib.parse


FORBIDDEN = ".-'\"&"


def now_ms() -> int:
    return int(time.time() * 1000)


def urlencode(txt: str) -> str:
    return urllib.parse.quote_plus(txt, encoding="utf-8")


def sanitize_text(txt: str) -> str:
    for ch in FORBIDDEN:
        txt = txt.replace(ch, "")
    return txt