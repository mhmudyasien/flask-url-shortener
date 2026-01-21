FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Update pip and install dependencies
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]
