"""
Custom Application exception
"""


class AppException(Exception):
    def __init__(
        self, status_code: int, location: list[str | int], message: str, exc_type: str
    ):
        self.status_code: int = status_code
        self._location: list[str | int] = location
        self._msg: str = message
        self._exc_type: str = exc_type

    def content(self):
        return {
            "detail": [
                {
                    "loc": self._location,
                    "msg": self._msg,
                    "type": self._exc_type,
                }
            ]
        }

    def __str__(self):
        return f"[{self._exc_type}]: {self._location} -> {self._msg}"
