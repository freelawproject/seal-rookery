import glob
import json
import os
from enum import Enum
from pathlib import Path
from typing import Literal, Optional


ROOT = os.path.dirname(os.path.abspath(__file__))

with Path(ROOT, "seals", "seals.json").open() as f:
    seals = json.load(f)


class ImageSizes(Enum):
    TINY = 128
    SMALL = 256
    MEDIUM = 512
    LARGE = 1024
    ORIGINAL = "orig"


SIZES = Literal[
    ImageSizes.TINY,
    ImageSizes.SMALL,
    ImageSizes.MEDIUM,
    ImageSizes.LARGE,
    ImageSizes.ORIGINAL,
]


def seal(court: str, size: SIZES = ImageSizes.MEDIUM) -> Optional[str]:
    """Get URL for seals on free.law"""

    if court not in seals.keys():
        return None
    if size == ImageSizes.ORIGINAL:
        if glob.glob(f"{ROOT}/seals/orig/{court}.*"):
            file = glob.glob(f"{ROOT}/seals/orig/{court}.*")[0].split("/")[-1]
            return f"https://seals.free.law/v2.1/{size.value}/{file}"
        return None
    else:
        return f"https://seals.free.law/v2.1/{size.value}/{court}.png"
