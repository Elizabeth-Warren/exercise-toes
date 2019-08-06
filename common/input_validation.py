import re

import phonenumbers


def extract_phone_number(t):
    """Given string containing a phone #, returns string with phone # in canonical format.

    Format returned is e.g. '15105016227', which is Mobile Commons canonical format.

    Returns None if there no phone number in the input.
    """
    matcher = phonenumbers.PhoneNumberMatcher(t, 'US')
    if matcher.has_next():
        return phonenumbers.format_number(matcher.next().number, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
