from datetime import datetime


def get_timezone_name() -> str | None:
    now = datetime.now()
    local_now = now.astimezone()
    local_tz = local_now.tzinfo

    if local_tz is not None:
        return local_tz.tzname(local_now)
