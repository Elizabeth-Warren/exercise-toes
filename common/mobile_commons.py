import json
import os

import requests
import xmltodict
from datetime import datetime
import json,os
from pytz import timezone
import dateutil


from common.settings import settings

MOBILE_COMMONS_API_BASE = mobileCommonsApiBase = 'https://secure.mcommons.com/api/'
MOBILE_COMMONS_TIMEZONE = "US/Eastern"
MOBILE_COMMONS_ACTBLUE_MAX_DELAY = 3600 # actblue delayed by more than 1 hour or 3600 seconds
MOBILE_COMMONS_NIGHT_BEGIN = 21 # night beginning in 9pm
MOBILE_COMMONS_NIGHT_END = 9 # night ends in 9am

def send_sms(campaign_id, phone_number, message):
    """Sends given message to given phone number in given campaign."""
    try:
        payload = {
          'campaign_id': campaign_id,
          'phone_number': phone_number,
          'body': message,
        }
        mobile_commons_response = post_to_mobile_commons('send_message', payload)
    except RuntimeError as e:
        print('Error posting to MC', e)

def send_update(event):
    contribution_time = dateutil.parser.parse(event['contribution']['createdAt'])
    eastern = timezone('US/Eastern')
    current = datetime.now(eastern)
    diff = current - contribution_time
    if diff.total_seconds()>MOBILE_COMMONS_ACTBLUE_MAX_DELAY: #s
        if current.hour<MOBILE_COMMONS_NIGHT_END or current.hour>MOBILE_COMMONS_NIGHT_BEGIN: #before 9am or after 9pm Eastern time
            return False # don't send if difference is more than 1 hour or night time
    return True

def profile_exists(phone_number):
    """Returns whether or not a Mobile Commons profile exists with given phone number."""
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
    """Makes POST to Mobile Commons profile_update endpoint with given payload.

    This endpoint creates a profile with specified phone number if it
    doesn't already exist; it also opts the number in to the given
    opt-in path and sends the initial message of the opt-in path, if
    appropriate.
    """
    try:
        mobile_commons_response = post_to_mobile_commons('profile_update', payload)
    except RuntimeError as e:
        print('Error posting to MC creating profile', e)


def post_to_mobile_commons(api_method, payload):
    url = mobileCommonsApiBase + api_method
    resp = requests.post(
        url,
        auth=(settings.mobile_commons_username(), settings.mobile_commons_password()),
        json=payload,
    )
    print(f'Response from MC {api_method}', resp.text[0:400])
    return resp
