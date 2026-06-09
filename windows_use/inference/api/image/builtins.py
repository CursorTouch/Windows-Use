from windows_use.inference.api.image.openrouter import OpenRouterImageAPI
from windows_use.inference.api.image.openai_image import OpenAIImageAPI
from windows_use.inference.api.image.gemini_image import GeminiImageAPI

IMAGE_APIS = [
    ("openrouter-image", OpenRouterImageAPI),
    ("openai-image",     OpenAIImageAPI),
    ("gemini-image",     GeminiImageAPI),
]
