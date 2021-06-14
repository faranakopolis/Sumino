import redis
import Sumino.redisDriver.conf as conf

r = redis.Redis(host=conf.HOST,
                port=conf.PORT,
                db=conf.DB,
                charset="utf-8",
                decode_responses=True)


def update_user_request_count(user_ip, expires_at, request_type):
    """Recognize the request type and update its request's counts
        the data will be stored in the Redis db like: user_ip -> (sum_request_count, wrong_request_count).
    Wrong requests include not allowed methods (405) and mal format inputs (400).
    If any of these counts exceeds its limit (100,15) user will be blocked for a whole time period.
    In order to make it simple, I've considered time periods like this: 1-2, 2-3, 3-4, ...
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
