from flask import Blueprint, request, redirect, jsonify, session
from datetime import datetime, timedelta
import redis

from app import mysql
from app.utils import generate_short_code, check_api_key

main = Blueprint("main", __name__)
r = redis.Redis(host="redis", port=6379, decode_responses=True)

# ---------- Rate Limit ----------
def rate_limit():
    ip = request.remote_addr
    key = f"rate:{ip}"

    count = r.get(key)
    if count and int(count) >= 5:
        return False

    r.incr(key)
    r.expire(key, 60)
    return True

# ---------- Create Short URL ----------
@main.route("/", methods=["POST"])
def shorten_url():
    if not check_api_key():
        return "Unauthorized", 401

    if not rate_limit():
        return "Too many requests", 429

    long_url = request.json.get("url")
    expires_at = datetime.utcnow() + timedelta(hours=1)

    short_code = generate_short_code()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO urls (short_code, long_url, expires_at) VALUES (%s,%s,%s)",
        (short_code, long_url, expires_at)
    )
    mysql.connection.commit()
    cur.close()

    r.set(short_code, long_url, ex=3600)

    session["last_short"] = short_code

    return jsonify({
        "short_url": f"http://localhost:5000/{short_code}",
        "expires_in": "1 hour"
    })

# ---------- Redirect ----------
@main.route("/<short_code>")
def redirect_url(short_code):
    long_url = r.get(short_code)

    if not long_url:
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT long_url, expires_at FROM urls WHERE short_code=%s",
            (short_code,)
        )
        result = cur.fetchone()
        cur.close()

        if not result or result[1] < datetime.utcnow():
            return "Link expired or not found", 404

        long_url = result[0]
        r.set(short_code, long_url, ex=3600)

    return redirect(long_url)
