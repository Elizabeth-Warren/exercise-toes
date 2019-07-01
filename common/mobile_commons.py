import json
import os

import requests
import xmltodict

from common.settings import settings

MOBILE_COMMONS_API_BASE = mobileCommonsApiBase = 'https://secure.mcommons.com/api/'


def post_to_mobile_commons(api_method, payload):
    url = mobileCommonsApiBase + api_method
    resp = requests.post(
        url,
        auth=(settings.mobile_commons_username(), settings.mobile_commons_password()),
        json=payload,
    )
    print(f'Response from MC {api_method}', resp.text[0:400])
    return resp


def send_sms(campaign_id, phone_number, message):
    try:
        payload = {
          'campaign_id': campaign_id,
          'phone_number': phone_number,
          'body': message,
        }
        mobile_commons_response = post_to_mobile_commons('send_message', payload)
    except RuntimeError as e:
        print('Error posting to MC', e)


def profile_exists(phone_number):
    try:
        payload = {
          'phone_number': phone_number,
        }
        mobile_commons_response = post_to_mobile_commons('profile', payload)
        d = xmltodict.parse(mobile_commons_response.text, attr_prefix='', cdata_key='value')
        return 'response' in d and 'success' in d['response'] and d['response']['success'] == 'true'
    except RuntimeError as e:
        print('Error posting to MC', e)


def create_or_update_mobile_commons_profile(payload):
    try:
        mobile_commons_response = post_to_mobile_commons('profile_update', payload)
    except RuntimeError as e:
        print('Error posting to MC creating profile', e)
