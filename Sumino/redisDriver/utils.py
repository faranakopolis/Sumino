import redis
import Sumino.redisDriver.conf as conf

r = redis.Redis(host=conf.HOST,
                port=conf.PORT,
                db=conf.DB,
                charset="utf-8",
                decode_responses=True)


def update_sum_limit(user_ip, expires_at, limit):
    """Expires at is the duration(seconds) which in,
        the user_ip request will be added in this format: ip -> (count, is_blocked)
        I considered time periods like this: 1-2, 2,3, ...
    """
    result = eval(str(r.get(user_ip)))  # Convert redis result into tuple

    if result is None:
        r.set(user_ip, str((1, False)), ex=expires_at)
        r.save()  # It's not good to use save in production...
        return 1  # Saved successfully

    elif result[0] <= limit:  # Count is less than the limit
        r.set(user_ip, str((result[0] + 1, False)), ex=expires_at)
        r.save()
        return 1  # Updated successfully

    elif result[0] > limit:
        # User exceeded the request limit for sum API
        # Update is_blocked value to True for the rest of the expires_at time
        r.set(user_ip, str((result[0] + 1, True)), ex=expires_at)
        r.save()
        return -1
