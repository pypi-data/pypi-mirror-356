# my-package

A lightweight Python library
to [brief description of what your package does, e.g., "validate structured strings", "simplify data formatting", etc.].

---

## 🚀 Installation

You can install the latest version using `pip`:

```bash
pip install validator-for-postcodes


## 🚀 Usage

from validator_for_postcodes import parse_postcode, postcode_factory
from validator_for_postcodes.countries.uk.postcode import UKPostcode


if __name__ == '__main__':
    parse_postcode("ASDKJF", country="uk")

    postcode_class = postcode_factory("uk")
    obj = postcode_class("KLAJSOID")
    print(obj.postcode)
    print(obj.validate())

    postcode_obj = UKPostcode("QK23AC")
    print(postcode_obj.postcode)
    print(postcode_obj.validate())
