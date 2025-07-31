class Task:
    CONN: str | None = None
    POOL: str | None = None
    RETRIES: int | None = None
    DEPLOY: bool = True
    RETRY_DELAY = None
    EXECUTION_TIMEOUT = None