from common.input_validation import (
    extract_city_state,
    extract_name,
    extract_personal_reason,
    extract_phone_number,
    extract_postal_code,
)


def test_extract_phone_number():
    assert extract_phone_number('510501622') == None
    assert extract_phone_number('5105016227') == '15105016227'
    assert extract_phone_number('15105016227') == '15105016227'
    assert extract_phone_number('+15105016227') == '15105016227'
    assert extract_phone_number('My number is 510 501 6227') == '15105016227'
    assert extract_phone_number('My number is (510) 501-6227.') == '15105016227'


def test_extract_postal_code():
    assert extract_postal_code(' 02145.') == '02145'
    assert extract_postal_code(' 0215.') == None

def test_extract_city_state():
    assert extract_city_state('kermit, west virginia') == ('kermit', 'WV')
    assert extract_city_state('Kermit, West Virginia') == ('Kermit', 'WV')
    assert extract_city_state('Kermit, WV') == ('Kermit', 'WV')
    assert extract_city_state('Kermit WV') == ('Kermit', 'WV')
    assert extract_city_state('kermit wv') == ('kermit', 'WV')
    assert extract_city_state('Charlestown Virginia') == ('Charlestown', 'VA')
    assert extract_city_state('Charlestown VA') == ('Charlestown', 'VA')
    assert extract_city_state('urrr') == (None, None)
    assert extract_city_state('Reno, Nevad') == (None, None)
