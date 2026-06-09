from dataclasses import dataclass


@dataclass
class APIResponse:
    status_code: int
    headers: dict[str, str]
