#!/usr/bin/env python3
"""Storing lists"""

import redis
import uuid
from typing import Union, Optional, Callable
import functools


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def get_key(method_name: str, key_type: str) -> str:
        return f"{method_name}:{key_type}"

    @functools.wraps
    def call_history(method: Callable) -> Callable:
        def wrapper(self, *args, **kwargs):
            inputs_key = Cache.get_key(method.__qualname__, "inputs")
            outputs_key = Cache.get_key(method.__qualname__, "outputs")

            # Store input arguments as a string in Redis
            self._redis.rpush(inputs_key, str(args))

            # Execute the wrapped function to get the output
            output = method(self, *args, **kwargs)

            # Store the output as a string in Redis
            self._redis.rpush(outputs_key, str(output))

            return output
        return wrapper

    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        if isinstance(data, (str, bytes)):
            self._redis.set(key, data)
        elif isinstance(data, (int, float)):
            self._redis.set(key, str(data))
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> \
            Union[str, bytes, int, float, None]:
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        return self.get(key, fn=lambda d: int(d))
