import time


def expire(sessions:dict, expire_in:int, refresh_rate:int=300):
    """
    @params:
        expire_in: will expire in x minutes 
        refresh_rate: in seconds
    """
    while True:
        now = time.time()
        expired_ids = [
            sid for sid, sess in sessions.items()
            if now - sess["last_activity"] > (expire_in * 60)
        ]
        for sid in expired_ids:
            del sessions[sid]
        time.sleep(refresh_rate)