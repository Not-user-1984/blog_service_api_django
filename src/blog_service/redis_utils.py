import redis


redis_client = redis.StrictRedis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True)


def mark_post_as_read(user_id, post_id):
    redis_key = f'user:{user_id}:read_posts'
    redis_client.sadd(redis_key, post_id)


def check_post_read(user_id, post_id):
    redis_key = f'user:{user_id}:read_posts'
    return redis_client.sismember(redis_key, post_id)
