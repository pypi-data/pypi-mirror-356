# -----------------------------
# File: yemot_router/flow.py
# -----------------------------
"""`Flow` – manager that routes Yemot HTTP requests to `Call` objects.
Framework‑agnostic: use `flow.handle_request(params)` inside Flask/FastAPI.
"""
from __future__ import annotations

import logging
from typing import Callable, Dict

from .call import Call
from .utils import now_ms

_LOG = logging.getLogger("yemot_flow")
Handler = Callable[[Call], None]


class Flow:
    """In‑memory manager keeping active calls by `ApiCallId`."""

    def __init__(self, *, timeout: int | float = 30_000, print_log: bool = False):
        self.active_calls: Dict[str, Call] = {}
        self.routes: Dict[str, Handler] = {}
        self.timeout_ms = timeout
        if print_log:
            logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # ---------------- Registration ----------------
    def add_route(self, extension: str, handler: Handler):
        self.routes[extension.strip("/")] = handler
        _LOG.debug("Route registered: %s -> %s", extension, handler)

    get = add_route  # alias

    # ---------------- Entry‑point -----------------
    def handle_request(self, params: dict) -> str:
        call_id = params.get("ApiCallId", "")
        if not call_id:
            _LOG.error("Missing ApiCallId – cannot continue")
            return "noop"

        self._cleanup_expired()

        call = self.active_calls.get(call_id)
        if call is None:
            call = Call(params, flow=self)
            self.active_calls[call_id] = call
            _LOG.debug("New call %s", call_id)
        else:
            call.update_params(params)
            _LOG.debug("Resume call %s", call_id)

        if params.get("hangup") == "yes":
            self._on_hangup(call)
            return "noop"

        ext = params.get("ApiExtension", "").strip("/")
        handler = self.routes.get(ext)
        if handler is None:
            _LOG.warning("No route for extension %s", ext)
            return "id_list_message=t-שלוחה לא קיימת"

        try:
            handler(call)
            return call.render_response()
        except Exception as exc:  # noqa: BLE001
            _LOG.exception("Unhandled error: %s", exc)
            return "id_list_message=t-תקלה זמנית"

    # ---------------- Internal helpers ------------
    def delete_call(self, call_id: str):
        self.active_calls.pop(call_id, None)
        _LOG.debug("Call %s deleted", call_id)

    def _on_hangup(self, call: Call):
        _LOG.info("Hang‑up for %s", call.call_id)
        self.delete_call(call.call_id)

    def _cleanup_expired(self):
        now = now_ms()
        for cid, c in list(self.active_calls.items()):
            if now - c.last_activity_ms > self.timeout_ms:
                _LOG.debug("Timeout cleaning %s", cid)
                self.delete_call(cid)