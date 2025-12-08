import re
from typing import Dict, Optional


SIZE_PATTERN = re.compile(r"\b(XXS|XS|S|M|L|XL|XXL|2XL|3XL)\b", re.IGNORECASE)


RAB_MODELS = [
    "microlight alpine",
    "microlight",
    "valiance",
    "cirrus",
    "electron",
    "positron",
    "nebula",
]


def _normalise_size(raw: str) -> str:
    raw = raw.upper()
    # Normalise 2XL/XXL etc however you like
    if raw == "2XL":
        return "XXL"
    return raw


def detect_model(title_lower: str) -> Optional[str]:
    for m in RAB_MODELS:
        if m in title_lower:
            return m.title()
    return None


def detect_gender(title_lower: str) -> Optional[str]:
    if "women" in title_lower or "womens" in title_lower or "woman" in title_lower or "ladies" in title_lower:
        return "Women"
    if "men" in title_lower or "mens" in title_lower or "man" in title_lower:
        return "Men"
    return None


def detect_variant(title_lower: str) -> Optional[str]:
    # Very rough: hood vs vest/gilet
    if "vest" in title_lower or "gilet" in title_lower:
        return "Vest"
    if "hood" in title_lower or "hooded" in title_lower:
        return "Hooded"
    return None


def detect_size(title: str) -> Optional[str]:
    match = SIZE_PATTERN.search(title)
    if not match:
        return None
    return _normalise_size(match.group(1))


def parse_rab_jacket(title: str) -> Dict[str, Optional[str]]:
    """
    Very simple heuristic parser for Rab jacket titles.
    Returns dict with keys: brand, model, variant, gender, size, colour (colour left for later).
    """
    t = title.lower()
    brand = "Rab" if "rab" in t else None

    model = detect_model(t)
    gender = detect_gender(t)
    variant = detect_variant(t)
    size = detect_size(title)

    # Colour parsing is messy – leave for later
    colour = None

    return {
        "brand": brand,
        "model": model,
        "variant": variant,
        "gender": gender,
        "size": size,
        "colour": colour,
    }

