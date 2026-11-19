import json
import logging
import sys
import time
from contextlib import contextmanager


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        for attr in ("session_id", "intent", "route", "product_ids",
                      "validation_failures", "tokens_used", "time_ms", "node"):
            val = getattr(record, attr, None)
            if val is not None:
                log_entry[attr] = val

        return json.dumps(log_entry)


def setup_logging():
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root = logging.getLogger("pickr")
    root.setLevel(logging.INFO)
    root.addHandler(handler)
    root.propagate = False

    return root


logger = setup_logging()


@contextmanager
def log_node_timing(node_name: str, session_id: str = ""):
    start = time.perf_counter()
    yield
    elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
    logger.info(
        "Node completed",
        extra={"node": node_name, "session_id": session_id, "time_ms": elapsed_ms},
    )
