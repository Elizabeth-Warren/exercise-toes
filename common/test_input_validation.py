from common.input_validation import (
    extract_phone_number,
)


def test_extract_phone_number():
    assert extract_phone_number('510501622') is None
    assert extract_phone_number('5105016227') == '15105016227'
    assert extract_phone_number('15105016227') == '15105016227'
    assert extract_phone_number('+15105016227') == '15105016227'
    assert extract_phone_number('My number is 510 501 6227') == '15105016227'
    assert extract_phone_number('My number is (510) 501-6227.') == '15105016227'
