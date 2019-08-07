import re

import phonenumbers


<<<<<<< HEAD
STATE_TO_ABBREV = {
    'alabama': 'AL',
    'alaska': 'AK',
    'arizona': 'AZ',
    'arkansas': 'AR',
    'california': 'CA',
    'colorado': 'CO',
    'connecticut': 'CT',
    'delaware': 'DE',
    'district of columbia': 'DC',
    'florida': 'FL',
    'georgia': 'GA',
    'hawaii': 'HI',
    'idaho': 'ID',
    'illinois': 'IL',
    'indiana': 'IN',
    'iowa': 'IA',
    'kansas': 'KS',
    'kentucky': 'KY',
    'louisiana': 'LA',
    'maine': 'ME',
    'maryland': 'MD',
    'massachusetts': 'MA',
    'michigan': 'MI',
    'minnesota': 'MN',
    'mississippi': 'MS',
    'missouri': 'MO',
    'montana': 'MT',
    'nebraska': 'NE',
    'nevada': 'NV',
    'new hampshire': 'NH',
    'new jersey': 'NJ',
    'new mexico': 'NM',
    'new york': 'NY',
    'north carolina': 'NC',
    'north dakota': 'ND',
    'ohio': 'OH',
    'oklahoma': 'OK',
    'oregon': 'OR',
    'pennsylvania': 'PA',
    'puerto rico': 'PR',
    'rhode island': 'RI',
    'south carolina': 'SC',
    'south dakota': 'SD',
    'tennessee': 'TN',
    'texas': 'TX',
    'utah': 'UT',
    'vermont': 'VT',
    'virginia': 'VA',
    'washington': 'WA',
    'west virginia': 'WV',
    'wisconsin': 'WI',
    'wyoming': 'WY',
}

STATE_ABBREVS = set(STATE_TO_ABBREV.values())

### add country abbrev
COUNTRYS_TO_ABBREV = {
    'United States': 'US',
}

def extract_postal_code(t):
    match = POSTAL_CODE_RE.search(t)
    if match:
        return match.group(0)
=======
def extract_phone_number(t):
    """Given string containing a phone #, returns string with phone # in canonical format.
>>>>>>> 3dcf57239bb2bb96ba696e930f9061d07cdb93a1

    Format returned is e.g. '15105016227', which is Mobile Commons canonical format.

    Returns None if there no phone number in the input.
    """
    matcher = phonenumbers.PhoneNumberMatcher(t, 'US')
    if matcher.has_next():
        return phonenumbers.format_number(matcher.next().number, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
