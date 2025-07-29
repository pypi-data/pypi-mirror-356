from validator_for_postcodes.countries.uk.data import (
    MAX_POSTCODE_LENGTH,
    MIN_POSTCODE_LENGTH,
    MIN_OUTWARD_LENGTH,
    MAX_OUTWARD_LENGTH,
    ONLY_FOURTH_CHAR,
    ONLY_DOUBLE_DIGIT,
    NEVER_IN_INWARD,
    ONLY_SINGLE_DIGIT,
    NEVER_SECOND,
    NEVER_FIRST,
)
from validator_for_postcodes.countries.uk.regex_ import (
    A9A,
    AA9A,
    double_digit_district,
    ONLY_THIRD_CHAR_PATTERN,
    ONLY_FOURTH_CHAR_PATTERN,
    NEVER_SECOND_PATTERN,
    single_digit_district,
    ONLY_THIRD_CHAR,
    NEVER_FIRST_PATTERN,
    NEVER_IN_INWARD_PATTERN,
)
from validator_for_postcodes.countries.uk.utils import strip_postcode, is_inward_valid, is_outward_valid
from validator_for_postcodes.utils import validate_allowed, validate_length
from validator_for_postcodes.validator import Validator


class UKValidator(Validator):

    @staticmethod
    def to_validate(value):
        pass


class ValidateLength(UKValidator):

    @staticmethod
    def to_validate(value: str):
        if not validate_length(value, min_value=MIN_POSTCODE_LENGTH, max_value=MAX_POSTCODE_LENGTH):
            return f"Wrong postcode length: {len(value)}. Min: {MIN_POSTCODE_LENGTH}, Min: {MAX_POSTCODE_LENGTH}"


class ValidateInward(UKValidator):

    @staticmethod
    def to_validate(value: str):
        _, inward = strip_postcode(value)
        if not is_inward_valid(inward):
            return f"Postcode is INVALID: '{value}'. Allowed inward format '9AA'"


class ValidateNeverInInward(UKValidator):

    @staticmethod
    def to_validate(value: str):
        _, inward = strip_postcode(value)
        if validate_allowed(inward, NEVER_IN_INWARD_PATTERN):
            return f"Inward is INVALID: '{value}'. Characters never used in Inward: {NEVER_IN_INWARD}"


class ValidateOutward(UKValidator):

    @staticmethod
    def to_validate(value: str):
        outward, _ = strip_postcode(value)
        if not is_outward_valid(outward):
            return f"Outward is invalid: '{value}' allowed formats A9, AA9, A99, A9A, AA9A"


class ValidateOutward3(UKValidator):

    @staticmethod
    def to_validate(value: str):
        outward, _ = strip_postcode(value)
        if validate_allowed(outward, A9A):
            if not validate_allowed(outward, ONLY_THIRD_CHAR_PATTERN):
                return f"Postcode is INVALID. In format A9A last/3rd character only allowed: {ONLY_THIRD_CHAR}"


class ValidateOutwardLength(UKValidator):

    @staticmethod
    def to_validate(value: str):
        outward, _ = strip_postcode(value)
        if not validate_length(outward, min_value=MIN_OUTWARD_LENGTH, max_value=MAX_OUTWARD_LENGTH):
            return f"Outward length is invalid. Min: {MIN_OUTWARD_LENGTH}, Max: {MAX_OUTWARD_LENGTH}"


class ValidateOutward4(UKValidator):

    @staticmethod
    def to_validate(value: str):
        outward, _ = strip_postcode(value)
        if validate_allowed(outward, AA9A):
            if not validate_allowed(outward, ONLY_FOURTH_CHAR_PATTERN):
                return f"Postcode is INVALID. In format AA9A 4th/last character only allowed: {ONLY_FOURTH_CHAR}"


class ValidateFirstRestricted(UKValidator):

    @staticmethod
    def to_validate(value: str):
        if validate_allowed(value, NEVER_FIRST_PATTERN):
            return f"Postcode is invalid. Never first character in outward: {NEVER_FIRST}"


class ValidateSecondRestricted(UKValidator):

    @staticmethod
    def to_validate(value: str):
        if validate_allowed(value, NEVER_SECOND_PATTERN):
            return f"Postcode is invalid. Never second character in outward: {NEVER_SECOND}"


class ValidateOnlySingleDigit(UKValidator):

    @staticmethod
    def to_validate(value: str):
        if validate_allowed(value, single_digit_district):
            return f"Postcode is INVALID. Only single digits allowed with districts: {ONLY_SINGLE_DIGIT}"


class ValidateOnlyDoubleDigit(UKValidator):

    @staticmethod
    def to_validate(value: str):
        if validate_allowed(value, double_digit_district):
            return f"Postcode is INVALID. Only 2 digits allowed with districts: {ONLY_DOUBLE_DIGIT}"
