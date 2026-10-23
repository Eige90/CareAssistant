from pathlib import Path
from urllib.request import Request, urlopen

from core.paths import BACKGROUND_DIR


STARRY_NIGHT_URL = (
    "https://upload.wikimedia.org/wikipedia/commons/6/69/"
    "VanGogh-starry_night_edit.jpg"
)


def ensure_starry_night(fallback_path: str) -> str:
    """
    Cache Van Gogh's The Starry Night locally on first launch.
    If the computer is offline, use the bundled fallback until a later start.
    """
    target = BACKGROUND_DIR / "van_gogh_starry_night.jpg"
    if target.exists() and target.stat().st_size > 100_000:
        return str(target)

    try:
        request = Request(
            STARRY_NIGHT_URL,
            headers={"User-Agent": "CareAssistant/0.5"}
        )
        with urlopen(request, timeout=6) as response:
            data = response.read()
        if len(data) > 100_000:
            target.write_bytes(data)
            return str(target)
    except Exception:
        pass

    return fallback_path
