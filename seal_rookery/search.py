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
    SMALL = 128
    MEDIUM = 256
    LARGE = 512
    XLARGE = 1024
    ORIGINAL = "orig"


SIZES = Literal[
    ImageSizes.SMALL,
    ImageSizes.MEDIUM,
    ImageSizes.LARGE,
    ImageSizes.XLARGE,
    ImageSizes.ORIGINAL,
]


def seal(court: str, size: SIZES = ImageSizes.MEDIUM) -> Optional[str]:
    """Get URL for seals on free.law

    :param court: The CL court ID to get. E.g., ca9 for Ninth Circuit of
    Appeals.
    :param size: The size of the seal you want a URL for..
    :return A URL to the image.
    """
    if court not in seals.keys():
        return None
    if size == ImageSizes.ORIGINAL:
        if glob.glob(f"{ROOT}/seals/orig/{court}.*"):
            file = glob.glob(f"{ROOT}/seals/orig/{court}.*")[0].split("/")[-1]
            return f"https://seals.free.law/v2/{size.value}/{file}"
        return None
    else:
        return f"https://seals.free.law/v2/{size.value}/{court}.png"
