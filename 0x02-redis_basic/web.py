#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import requests
import redis
import time


def get_page(url: str) -> str:
    # Connect to Redis
    r = redis.Redis()

    # Create a key to track the access count for the URL
    count_key = f"count:{url}"

    # Check if the URL content is already cached
    cached_content = r.get(url)
    if cached_content:
        # URL content is cached, return it
        r.incr(count_key)  # Increment the access count
        return cached_content.decode("utf-8")

    # URL content is not cached, fetch it from the web
    response = requests.get(url)
    if response.status_code == 200:
        # Cache the content with a 10-second expiration time
        r.setex(url, 10, response.content)

        # Increment the access count
        r.incr(count_key)

        return response.text

    return ""  # Return an empty string if the request was unsuccessful

# Test the get_page function
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.example.com"
print(get_page(url))
print(get_page(url))  # Cached response should be returned this time
