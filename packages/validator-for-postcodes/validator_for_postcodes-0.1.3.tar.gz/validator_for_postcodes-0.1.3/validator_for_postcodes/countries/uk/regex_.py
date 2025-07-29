from validator_for_postcodes.countries.uk.data import (
    NEVER_FIRST,
    NEVER_SECOND,
    ONLY_THIRD_CHAR,
    ONLY_FOURTH_CHAR,
    ONLY_DOUBLE_DIGIT,
    ONLY_SINGLE_DIGIT,
    NEVER_IN_INWARD
)

NEVER_FIRST_PATTERN = f"^([{''.join(NEVER_FIRST)}].)"
NEVER_SECOND_PATTERN = f"^(.[{''.join(NEVER_SECOND)}].)"

NEVER_IN_INWARD_PATTERN = fr"\d.[{''.join(NEVER_IN_INWARD)}]$|\d[{''.join(NEVER_IN_INWARD)}].$"

single_digit_district = fr"^({'|'.join(ONLY_SINGLE_DIGIT)})(?!\d(?!\d)).*"
double_digit_district = fr"^({'|'.join(ONLY_DOUBLE_DIGIT)})(?!\d{{2}}(?!\d)).*"

ONLY_THIRD_CHAR_PATTERN = f"^(..[{''.join(ONLY_THIRD_CHAR)}])"
ONLY_FOURTH_CHAR_PATTERN = f"^(...[{''.join(ONLY_FOURTH_CHAR)}])"

A9A = "^[A-Z][0-9][A-Z]"
AA9A = "^[A-Z]{2}[0-9][A-Z]"

VALID_INWARD_PATTERN = "[0-9][A-Z]{2}"
VALID_OUTWARD_PATTERN = "^([A-Z]{1,2}[0-9]{1,2}|[A-Z]{1,2][0-9]{1}[A-Z]{1})"
