from flask import Flask, request, redirect, render_template_string
from flask_session import Session
import redis
import mysql.connector
import os
import random
import string

app = Flask(__name__)

# ---------- Flask Session config with Redis ----------
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = redis.Redis(
    host=os.environ.get('REDIS_HOST', 'redis'), 
    port=int(os.environ.get('REDIS_PORT', 6379))
)
Session(app)

# ---------- MySQL config ----------
db = mysql.connector.connect(
    host=os.environ.get('MYSQL_HOST', 'mysql'),
    user=os.environ.get('MYSQL_USER', 'root'),
    password=os.environ.get('MYSQL_PASSWORD', 'password'),
    database=os.environ.get('MYSQL_DATABASE', 'url_shortener')
)

cursor = db.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS urls (
    id INT AUTO_INCREMENT PRIMARY KEY,
    short VARCHAR(10) UNIQUE NOT NULL,
    original TEXT NOT NULL
)
""")
db.commit()

# ---------- Flask routes ----------
HTML = """
<h2>Flask URL Shortener</h2>
<form method="POST">
    URL: <input type="text" name="url">
    <input type="submit" value="Shorten">
</form>
<ul>
{% for short, original in urls %}
    <li><a href="{{ original }}">{{ short }}</a></li>
{% endfor %}
</ul>
"""

def generate_short():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        original_url = request.form['url']
        short = generate_short()
        try:
            cursor.execute("INSERT INTO urls (short, original) VALUES (%s, %s)", (short, original_url))
            db.commit()
        except:
            db.rollback()
            short = generate_short()  # retry if duplicate
            cursor.execute("INSERT INTO urls (short, original) VALUES (%s, %s)", (short, original_url))
            db.commit()
    cursor.execute("SELECT short, original FROM urls")
    urls = cursor.fetchall()
    return render_template_string(HTML, urls=urls)

@app.route("/<short>")
def redirect_short(short):
    cursor.execute("SELECT original FROM urls WHERE short=%s", (short,))
    result = cursor.fetchone()
    if result:
        return redirect(result[0])
    return "URL not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
