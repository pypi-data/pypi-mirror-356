# -----------------------------
# File: yemot_router/call.py
# -----------------------------
"""Represents a live IVR call; accumulates actions until `render_response()` is called."""
from __future__ import annotations

from typing import List, Tuple

from .actions import build_go_to_folder, build_id_list_message, build_read
from .utils import now_ms

Message = Tuple[str, str]


class Call:
    """A single IVR call instance bound to one `ApiCallId`."""

    def __init__(self, params: dict, *, flow: "Flow"):
        from .flow import Flow  # local import to avoid circular

        self.params = params.copy()
        self.flow = flow
        self.call_id: str = params.get("ApiCallId", "")
        self.response_parts: List[str] = []
        self.last_activity_ms = now_ms()

    # --------------------------------------------------------------
    # Runtime helpers
    # --------------------------------------------------------------
    def update_params(self, new_params: dict):
        self.params.update(new_params)
        self.last_activity_ms = now_ms()

    # --------------------------------------------------------------
    # Developer‑facing API (what you’ll use inside route functions)
    # --------------------------------------------------------------
    def read(self, messages: List[Message], *, mode: str = "tap", **options):
        self.response_parts.append(build_read(messages, mode=mode, **options))

    def play_message(self, messages: List[Message], **options):
        self.response_parts.append(build_id_list_message(messages, **options))

    def goto(self, folder: str):
        self.response_parts.append(build_go_to_folder(folder))

    def hangup(self):
        self.goto("hangup")

    # --------------------------------------------------------------
    # Finalise
    # --------------------------------------------------------------
    def render_response(self) -> str:
        if not self.response_parts:
            return "noop"
        result = "\n".join(self.response_parts)
        self.response_parts.clear()
        return result
