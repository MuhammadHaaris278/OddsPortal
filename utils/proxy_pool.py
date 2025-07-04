# utils/proxy_pool.py

import random

# Sample free proxies (rotate often or expand from proxy list APIs)
FREE_PROXIES = [
    "http://103.152.112.147:80",
    "http://51.79.50.22:9300",
    "http://34.91.135.38:3128",
    "http://45.167.125.97:9991",
    "http://103.155.54.26:84"
]

def get_random_proxy():
    return random.choice(FREE_PROXIES)
