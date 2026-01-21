# Flask URL Shortener

Simple URL shortener using Flask, MySQL, Redis.

## Run
docker compose up --build

## Create short URL
curl -X POST http://localhost:5000 \
 -H "X-API-KEY: my-secret-api-key" \
 -H "Content-Type: application/json" \
 -d '{"url":"https://google.com"}'
