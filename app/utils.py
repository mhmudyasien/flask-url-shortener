import random
import string
import time
from flask import request, current_app

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def check_api_key():
    return request.headers.get("X-API-KEY") == current_app.config["API_KEY"]
