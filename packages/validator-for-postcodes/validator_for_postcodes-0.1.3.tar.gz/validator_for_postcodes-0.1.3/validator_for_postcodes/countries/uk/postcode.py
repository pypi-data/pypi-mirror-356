import re

from validator_for_postcodes.countries.uk.utils import format_postcode
from validator_for_postcodes.countries.uk.validator import UKValidator


def find_district(outward: str) -> str:
    match = re.search(r"\d{1,2}[A-Z]{0,2}$", outward)
    if match:
        return match.group()
    return outward


def find_area(outward: str) -> str:
    match = re.match(r"^[A-Z]{1,2}", outward)
    if match:
        return match.group()
    return outward


class UKPostcode:
    def __init__(self, postcode: str):
        postcode = format_postcode(postcode)
        self._postcode = postcode

    @property
    def postcode(self):
        return self._postcode

    @property
    def area(self):
        return find_area(self.outward)

    @property
    def district(self):
        return find_district(self.outward)

    @property
    def inward(self):
        return self.postcode.split()[-1]

    @property
    def outward(self):
        return self.postcode.split()[0]

    @property
    def sector(self):
        return self.inward[:1]

    @property
    def unit(self):
        return self.inward[-2:]

    def validate(self) -> list:
        errors = []

        for subclass in UKValidator.__subclasses__():
            if (error := subclass.to_validate(self._postcode)) is not None:
                errors.append(error)

        print(f"Postcode is {'IN' if errors else ''}VALID!")
        return errors
