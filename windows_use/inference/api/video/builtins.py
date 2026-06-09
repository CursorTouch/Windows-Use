from operator_use.inference.api.video.base import BaseVideoAPI
from operator_use.inference.api.video.fal_video import FalVideoAPI
from operator_use.inference.api.video.openrouter_video import OpenRouterVideoAPI

VIDEO_APIS: list[tuple[str, type[BaseVideoAPI]]] = [
    ("fal-video", FalVideoAPI),
    ("openrouter-video", OpenRouterVideoAPI),
]
