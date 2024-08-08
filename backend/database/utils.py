from datetime import datetime, timezone


def utctime():
    return datetime.now(timezone.utc)
