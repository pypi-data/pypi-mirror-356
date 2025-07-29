import argparse
from typing import Literal

from validator_for_postcodes.countries_ import postcode_factory


def parse_postcode(postcode: str, country: Literal["uk"]):
    postcode_class = postcode_factory(country)
    post_code_obj = postcode_class(postcode)
    errors = post_code_obj.validate()
    if errors:
        print(errors)
        return
    print(f"VALID POSTCODE: '{post_code_obj.postcode}'")


def main():
    parser = argparse.ArgumentParser(prog='postcode')
    parser.add_argument('--country', help='Country', default="uk")
    parser.add_argument('--postcode', help='Postcode')
    args = parser.parse_args()

    parse_postcode(postcode=args.postcode, country=args.country)


if __name__ == '__main__':
    main()
