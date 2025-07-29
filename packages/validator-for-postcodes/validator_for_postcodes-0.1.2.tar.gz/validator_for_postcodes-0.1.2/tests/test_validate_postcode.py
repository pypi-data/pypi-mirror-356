import pytest

from validator_for_postcodes.countries.uk.data import (
    ONLY_THIRD_CHAR,
    ONLY_FOURTH_CHAR,
    ONLY_SINGLE_DIGIT,
    ONLY_DOUBLE_DIGIT,
    NEVER_IN_INWARD,
    NEVER_SECOND,
    NEVER_FIRST,
)
from validator_for_postcodes.countries.uk.postcode import UKPostcode
from validator_for_postcodes.countries.uk.utils import format_postcode


@pytest.mark.parametrize("postcode, message", [
    ("K1 3B", "Wrong postcode length: 5. Min: 6, Min: 8"),
    ("KT1 3B", "Postcode is INVALID: 'KT1 3B'. Allowed inward format '9AA'"),
    ("BR44 3BB", f"Postcode is INVALID. Only single digits allowed with districts: {ONLY_SINGLE_DIGIT}"),
    ("AB2 3BA", f"Postcode is INVALID. Only 2 digits allowed with districts: {ONLY_DOUBLE_DIGIT}"),
    ("QK7 9AA", f"Postcode is invalid. Never first character in outward: {NEVER_FIRST}"),
    ("KI2 9AA", f"Postcode is invalid. Never second character in outward: {NEVER_SECOND}"),
    ("PPP9 9AA", "Outward is invalid: 'PPP9 9AA' allowed formats A9, AA9, A99, A9A, AA9A"),
    ("P9I 9AA", f"Postcode is INVALID. In format A9A last/3rd character only allowed: {ONLY_THIRD_CHAR}"),
    ("PA9C 9AA", f"Postcode is INVALID. In format AA9A 4th/last character only allowed: {ONLY_FOURTH_CHAR}"),
    ("P9A 9CA", f"Inward is INVALID: 'P9A 9CA'. Characters never used in Inward: {NEVER_IN_INWARD}"),
])
def test_postcode_validation(postcode, message):
    assert message in UKPostcode(postcode).validate()


def test_postcode_formatting():
    postcode = format_postcode("vv3a5ba")
    assert postcode == "VV3A 5BA"


@pytest.fixture(scope="session")
def postcode():
    yield UKPostcode("VV3 7AL")


def test_postcode_outward(postcode):
    assert postcode.outward == "VV3"


def test_postcode_inward(postcode):
    assert postcode.inward == "7AL"


def test_postcode_area(postcode):
    assert postcode.area == "VV"


def test_postcode_district(postcode):
    assert postcode.district == "3"


def test_postcode_sector(postcode):
    assert postcode.sector == "7"


def test_postcode_unit(postcode):
    assert postcode.unit == "AL"
