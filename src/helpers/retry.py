import time
from dataclasses import dataclass
from typing import Callable, Optional

import requests

RETRYABLE_STATUS = {502, 503, 504}

@dataclass
class ResponseLike:
    status_code: int
    error: Optional[str] = None
    attempts: int = 1

    def json(self):
        return {"error": self.error, "attempts": self.attempts}

def request_with_retry(
    call: Callable[[], object],
    retries: int = 5,
    sleep_s: float = 0.8,
):
    """Retry wrapper for flaky gateway/proxy errors and timeouts."""
    last = None
    for attempt in range(1, retries + 1):
        try:
            last = call()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            last = ResponseLike(status_code=504, error=str(e), attempts=attempt)
        except requests.exceptions.RequestException as e:
            last = ResponseLike(status_code=504, error=str(e), attempts=attempt)

        status = getattr(last, "status_code", None)
        if status not in RETRYABLE_STATUS:
            return last

        time.sleep(sleep_s)

    if isinstance(last, ResponseLike):
        last.attempts = retries
    return last
