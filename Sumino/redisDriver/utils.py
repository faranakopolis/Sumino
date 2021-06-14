import redis
import Sumino.redisDriver.conf as conf

r = redis.Redis(host=conf.HOST,
                port=conf.PORT,
                db=conf.DB,
                charset="utf-8",
                decode_responses=True)


def check_user_block_status(user_ip):
    """Get the wrong request counts based on user_ip from Redis db
        and if it's reached its limit(15) then return True, otherwise return False.
       Call this function for all APIs
    """


def update_user_request_count(user_ip, expires_at, request_type):
    """Recognize the request type and update its request's counts
        the data will be stored in the Redis db like: user_ip -> (sum_request_count, wrong_request_count).

    Wrong requests include not allowed methods (405) and mal format inputs (400).

    If any of these counts exceeds its limit (100,15) user will be blocked for a whole time period.

    In order to make it simple, I've considered time periods like this: 1-2, 2-3, 3-4, ...
    """
    result = eval(str(r.get(user_ip)))  # Convert redis result into tuple

    if request_type == "sum":
        """My assumption: 
                    If the user's sum requests count exceeds the limit (100)
                    then his access will be blocked just for the sum API (not the rest of them).
        
        Result: -1 means the user is blocked and 1 means the count is added to one and it's okay.
        """
        if result is None:
            r.set(user_ip, str((1, 0)), ex=expires_at)
            r.save()  # It's not good to use save in production...
            return 1  # Saved successfully

        elif result[0] <= conf.SUM_REQUEST_LIMIT:  # Count is less than the limit
            r.set(user_ip, str((result[0] + 1, result[1])), ex=expires_at)
            r.save()
            return 1  # Updated successfully

        elif result[0] > conf.SUM_REQUEST_LIMIT:
            # User exceeded the request limit for sum API
            r.set(user_ip, str((result[0] + 1, result[1])), ex=expires_at)
            r.save()
            return -1

    elif request_type == "wrong":
        """My assumption: 
            If the user's wrong requests count exceeds the limit (15)
                then his access will be blocked for all of the APIs (sum, total and history).
        
        Result: -1 means the user is blocked and 1 means the count is added to one and it's okay.
        """
        if result is None:
            r.set(user_ip, str((0, 1)), ex=expires_at)
            r.save()  # It's not good to use save in production...
            return 1  # Saved successfully

        elif result[1] <= conf.WRONG_REQUEST_LIMIT:  # Count is less than the limit
            r.set(user_ip, str((result[0], result[1] + 1)), ex=expires_at)
            r.save()
            return 1  # Updated successfully

        elif result[1] > conf.WRONG_REQUEST_LIMIT:
            # User exceeded the limit for Wrong requests
            r.set(user_ip, str((result[0], result[1] + 1)), ex=expires_at)
            r.save()
            return -1
