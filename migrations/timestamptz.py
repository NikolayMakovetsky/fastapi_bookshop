from datetime import datetime, timezone

dt_utc_now = datetime.now(timezone.utc)
dt_str = datetime.now(timezone.utc).isoformat()
dt = datetime.fromisoformat(dt_str)


if __name__ == '__main__':
    print(dt_utc_now, type(dt_utc_now))
    print(dt_str, type(dt_str))
    print(dt, type(dt))
