import time
from dataclasses import dataclass
from typing import Callable, Optional

import requests

RETRYABLE_STATUS = {502, 503, 504}

@dataclass
class ResponseLike:
    status_code: int
    error: Optional[str] = None

    def json(self):
        return {"error": self.error} if self.error else {}

def request_with_retry(call: Callable[[], object], retries: int = 3, sleep_s: float = 0.7):
    last = None
    for _ in range(retries):
        try:
            last = call()
        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout) as e:
            last = ResponseLike(status_code=504, error=str(e))
        except requests.exceptions.RequestException as e:
            last = ResponseLike(status_code=504, error=str(e))

        status = getattr(last, "status_code", None)
        if status not in RETRYABLE_STATUS:
            return last

        time.sleep(sleep_s)
    return last
