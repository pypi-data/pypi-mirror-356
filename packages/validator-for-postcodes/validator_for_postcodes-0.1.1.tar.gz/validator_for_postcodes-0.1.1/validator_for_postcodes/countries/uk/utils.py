import re

from validator_for_postcodes.countries.uk.regex_ import VALID_OUTWARD_PATTERN, VALID_INWARD_PATTERN


def clean_postcode(postcode: str) -> str:
    return re.sub(r"\s+", " ", postcode).strip()


def format_postcode(postcode: str) -> str:
    if not isinstance(postcode, str):
        raise TypeError(f"Invalid postcode type: {type(postcode)}, required String")

    postcode = clean_postcode(postcode)
    postcode = postcode.upper()
    if " " not in postcode:
        postcode = postcode[:-3] + " " + postcode[-3:]
    return postcode


def strip_postcode(postcode: str):
    outward, inward = postcode.split(" ")
    return outward, inward


def is_inward_valid(inward: str) -> bool:
    return bool(re.match(VALID_INWARD_PATTERN, inward))


def is_outward_valid(inward: str) -> bool:
    return bool(re.match(VALID_OUTWARD_PATTERN, inward))
