from PIL import Image
import io
import requests


IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
DEFAULT_RAMP = "@%#*+=-:. "


def fetch_poster_image(poster_path):
    if not poster_path:
        return None
    poster_url = f"{IMAGE_BASE_URL}{poster_path}"
    response = requests.get(poster_url, timeout=20)
    response.raise_for_status()
    img = Image.open(io.BytesIO(response.content))
    return img


def image_to_ascii(poster_path, width=80, ramp=DEFAULT_RAMP):
    img = fetch_poster_image(poster_path)
    if img is None:
        return ""
    img = img.convert("L")
    aspect_ratio = img.height / img.width
    height = max(1, int(aspect_ratio * width * 0.55))
    img = img.resize((width, height))
    pixels = img.getdata()
    ramp_len = len(ramp) - 1
    chars = [ramp[int(pixel / 255 * ramp_len)] for pixel in pixels]
    lines = ["".join(chars[i : i + width]) for i in range(0, len(chars), width)]
    return "\n".join(lines)
