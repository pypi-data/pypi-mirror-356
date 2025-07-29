# my-package

A lightweight Python library
to [brief description of what your package does, e.g., "validate structured strings", "simplify data formatting", etc.].

---

## 🚀 Installation

You can install the latest version using `pip`:

```bash
pip install validator-for-postcodes


## 🚀 Usage

from validate_postcode import parse_postcode, postcode_factory

if __name__ == '__main__':
    postcode_class = postcode_factory("uk")
    print(parse_postcode("ASDKJF", country="uk"))
    obj = postcode_class("KLAJSOID")
    print(obj.postcode)
