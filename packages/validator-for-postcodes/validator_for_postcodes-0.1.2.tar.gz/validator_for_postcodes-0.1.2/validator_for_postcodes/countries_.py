from validator_for_postcodes.countries.uk.postcode import UKPostcode

POSTCODES = {
    "uk": UKPostcode,
}


class Countries:
    UK = "UK"


def postcode_factory(country):
    if (postcode := POSTCODES.get(country)) is not None:
        return postcode
    raise KeyError(f"Unsupported country: {country}")
