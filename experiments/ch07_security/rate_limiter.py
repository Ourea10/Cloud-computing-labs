from dataclasses import dataclass
from time import monotonic


@dataclass
class RateLimitState:
    count: int
    window_started: float


class RateLimiter:
    def __init__(
        self,
        max_requests: int,
        window_seconds: float,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._states: dict[str, RateLimitState] = {}

    def allow(self, key: str) -> bool:
        now = monotonic()

        state = self._states.get(key)

        if state is None:
            self._states[key] = RateLimitState(
                count=1,
                window_started=now,
            )
            return True

        elapsed = now - state.window_started

        if elapsed >= self.window_seconds:
            self._states[key] = RateLimitState(
                count=1,
                window_started=now,
            )
            return True

        if state.count >= self.max_requests:
            return False

        state.count += 1

        return True