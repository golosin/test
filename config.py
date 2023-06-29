from starlette.config import Config

config = Config(".env")

try:
    _pg_h = config("POSTGRES_HOST")
    _pg_d = config("POSTGRES_DB")
    _pg_u = config("POSTGRES_USER")
    _pg_p = config("POSTGRES_PASSWORD")
    POSTGRES_URL: str = f"postgres://{_pg_u}:{_pg_p}@{_pg_h}/{_pg_d}"

except Exception as e:
    print(f"Config error: {e}")
