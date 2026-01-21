class Config:
    SECRET_KEY = "secret-key"

    # MySQL
    MYSQL_HOST = "mysql"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_DB = "shortener"

    # Redis
    SESSION_TYPE = "redis"
    SESSION_REDIS = "redis://redis:6379"

    # API Key
    API_KEY = "my-secret-api-key"
