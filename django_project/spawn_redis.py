"""
This module spawns Redis instance to reuse it across other modules like this:

from django_project.spawn_redis import redis
total_views = redis.incr(f"image:{image.id}:views")
"""
import redis as _redis
from django.conf import settings

redis = _redis.Redis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
)
