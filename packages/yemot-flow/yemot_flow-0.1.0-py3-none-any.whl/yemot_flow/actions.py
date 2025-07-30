# -----------------------------
# File: yemot_router/call.py
# -----------------------------
"""Represents a single IVR call; collects actions until response is rendered."""
from __future__ import annotations

from typing import List, Tuple

from .actions import build_go_to_folder, build_id_list_message, build_read
from .utils import now_ms

Message = Tuple[str, str]


class Call:
    """A live call bound to one `ApiCallId`."""

    def __init__(self, params: dict, *, flow: "Flow"):
        from .flow import Flow  # local to avoid circular import at top level

        self.params = params.copy()
        self.flow = flow
        self.call_id: str = params.get("ApiCallId", "")
        self.response_parts: List[str] = []
        self.last_activity_ms = now_ms()

    # -------- lifecycle --------
    def update_params(self, new_params: dict):
        self.params.update(new_params)
        self.last_activity_ms = now_ms()

    # -------- Developer API ----
    def read(self, messages: List[Message], *, mode: str = "tap", **options):
        self.response_parts.append(build_read(messages, mode=mode, **options))

    def play_message(self, messages: List[Message], **options):
        self.response_parts.append(build_id_list_message(messages, **options))

    def goto(self, folder: str):
        self.response_parts.append(build_go_to_folder(folder))

    def hangup(self):
        self.goto("hangup")

    # -------- finalise ---------
    def render_response(self) -> str:
        if not self.response_parts:
            return "noop"
        resp = "\n".join(self.response_parts)
        self.response_parts.clear()
        return resp