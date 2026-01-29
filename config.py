import os

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

class AppConfig:
    def __init__(self, token, language, region):
        self.token = token
        self.language = language
        self.region = region


def load_config(language=None, region=None):
    if load_dotenv is not None:
        load_dotenv()
    token = os.getenv("TMBD_TOKEN")
    if not token:
        raise ValueError("TMBD_TOKEN is missing. Add it to your .env or shell env.")
    return AppConfig(
        token=token,
        language=language or os.getenv("TMDB_LANGUAGE", "en-US"),
        region=region or os.getenv("TMDB_REGION", "US"),
    )
