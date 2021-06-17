import redis
import Sumino.redisDriver.conf as conf

r = redis.Redis(host=conf.HOST,
                port=conf.PORT,
                db=conf.DB,
                charset="utf-8",
                decode_responses=True)


def check_user_block_status(key, limit):
    """Get the wrong or sum request counts based on <user-ip>_<request-type> key from Redis db
        and if it's reached its limit(15 or 100) then return True, otherwise return False.
       (This function will be called in the classes in permissions.py module).
    """
    result = eval(str(r.get(key)))

    if result is None or result < limit:
        return False

    return True


def update_user_request_count(key, expires_at):
    """Update the request's counts based on it's type
        the data will be stored in the Redis db like: <user-ip>_<request-type> -> request_count

    Wrong requests include not allowed methods (405) and mal format inputs (400).
    If any of these counts exceeds its limit (100, 15) user will be blocked for a whole time period.
     (till the start of the next period)
    In order to make it simple, I've considered time periods like this: 1-2, 2-3, 3-4, ...

    My assumption:
        If the user's sum requests count exceeds the limit (100)
         then his access will be blocked "just" for the sum API (not the rest of them).
        If the user's wrong requests count exceeds the limit (15)
         then his access will be blocked for "all" of the APIs (sum, total and history).
    """
    result = eval(str(r.get(key)))

    if result is None:
        r.set(key, 1, ex=expires_at)
        r.save()  # It's not good to use save in production...

    else:
        r.set(key, result + 1, ex=expires_at)
        r.save()
