from threading import Lock

_LOCK = Lock()
_COUNTERS = {
    "analyze_requests": 0,
    "chat_requests": 0,
    "chat_refusals": 0,
}


def record_analyze() -> None:
    # TODO[PERSON-3]: Replace in-memory counters with production metrics if deployed.
    with _LOCK:
        _COUNTERS["analyze_requests"] += 1


def record_chat(refused: bool) -> None:
    with _LOCK:
        _COUNTERS["chat_requests"] += 1
        if refused:
            _COUNTERS["chat_refusals"] += 1


def snapshot() -> dict[str, int]:
    with _LOCK:
        return dict(_COUNTERS)
