from base64 import b64encode
import json
import os

from flask import url_for
import boto3
import freezegun
import pytest
import responses

from common.settings import settings

# In the sample, the donation was made at 2019-06-07T15:49:32-04:00.
DAYTIME_WEBHOOK_NOTIFICATION_TIME = '2019-06-07T20:32:24Z'

MOBILE_COMMONS_PROFILE_RESPONSE = """
<response success="true">
  <profile id="338948442">
    <first_name>Jason</first_name>
    <last_name>Katz-Brown</last_name>
    <phone_number>15105016227</phone_number>
  </profile>
</response>
"""

MOBILE_COMMONS_PROFILE_NOT_EXIST_RESPONSE = """
<response success="false">
  <error id="5" message="Invalid phone number"/>
</response>
"""

MOBILE_COMMONS_PROFILE_UPDATE_RESPONSE = """
<response success="true">
  <profile id="345304097">
    <first_name>Mary</first_name>
    <last_name>Smith</last_name>
    <phone_number>15105016227</phone_number>
    <email>example@example.com</email>
    <status>Active Subscriber</status>
    <created_at>2019-06-06 19:33:03 UTC</created_at>
    <updated_at>2019-06-06 19:33:03 UTC</updated_at>
    <opted_out_at/>
    <opted_out_source/>
    <source type="API" name="Civis Sync" email="jkatzbrown+mcommonsapi@elizabethwarren.com"/>
    <address>
      <street1>20 Belvedere Ave.</street1>
      <street2/>
      <city>Richmond</city>
      <state>CA</state>
      <postal_code>94801</postal_code>
      <country>US</country>
    </address>
    <location>
      <latitude>45.507856</latitude>
      <longitude>-122.690794</longitude>
      <precision>place</precision>
      <city>Richmond</city>
      <state>CA</state>
      <postal_code>94801</postal_code>
      <country>US</country>
    </location>
    <districts></districts>
    <custom_columns></custom_columns>
    <subscriptions>
      <subscription campaign_id="189358" campaign_name="National" campaign_description="" opt_in_path_id="279022" status="Active" opt_in_source="Civis Sync" created_at="2019-06-06T19:33:03Z" activated_at="2019-06-06T19:33:03Z" opted_out_at="" opt_out_source=""/>
    </subscriptions>
    <integrations></integrations>
    <clicks></clicks>
  </profile>
</response>
"""


@pytest.fixture
def sample_donation():
    with open(os.path.join(os.path.dirname(__file__), 'sample_donation.json')) as f:
        return f.read()


@pytest.fixture
def mock_actblue_webhook_auth():
    settings._actblue_webhook_username = 'test_user'
    settings._actblue_webhook_password = 'test_password'
    settings._mobile_commons_username = 'test_mc_user'
    settings._mobile_commons_password = 'test_mc_password'
    return f'Basic {b64encode(b"test_user:test_password").decode("ascii")}'


def check_mobile_commons_request_body(request):
    body = json.loads(request.body)
    print('request body is', json.dumps(body, indent=2))
    expected = {
        "phone_number": "15105016227",
        "email": "example@example.com",
        "postal_code": "94801",
        "first_name": "Mary",
        "last_name": "Smith",
        "street1": "20 Belvedere Ave.",
        "city": "Richmond",
        "state": "CA",
        "country": "US",
        "opt_in_path_id": "279022",
    }
    for k, v in expected.items():
        assert body[k] == v
    return (200, {}, MOBILE_COMMONS_PROFILE_UPDATE_RESPONSE)

def run_mock_actblue_webhook_auth(client, sample_donation, mock_actblue_webhook_auth):
    try:
        res = client.post(
            url_for('actblue.donation'),
            headers={ 'Authorization': mock_actblue_webhook_auth },
            data=sample_donation,
        )
        return res
    except NotImplementedError:
        print(f'Waiting for implementation of upload_to_mobilecommons() : )')
        return

@responses.activate
@freezegun.freeze_time(DAYTIME_WEBHOOK_NOTIFICATION_TIME)
def test_invalid_auth(client, sample_donation, mock_actblue_webhook_auth):
    res = client.post(
        url_for('actblue.donation'),
        headers={ 'Authorization': f'Basic {b64encode(b"wrong_user:wrong_password").decode("ascii")}' },
        data=sample_donation,
    )
    assert res.status_code == 401


@responses.activate
@freezegun.freeze_time(DAYTIME_WEBHOOK_NOTIFICATION_TIME)
def test_valid_auth_no_phone(client, sample_donation, mock_actblue_webhook_auth):
    d = json.loads(sample_donation)
    d['donor']['phone'] = None
    sample_donation_no_phone = json.dumps(d)
    try:
        res = client.post(
            url_for('actblue.donation'),
            headers={ 'Authorization': mock_actblue_webhook_auth },
            data=sample_donation_no_phone,
        )
        assert res.status_code == 204
    except NotImplementedError:
        print(f'Waiting for implementation of upload_to_mobilecommons() : )')

    assert len(responses.calls) == 0  # No Mobile Commons requests because no incoming phone number


@responses.activate
@freezegun.freeze_time(DAYTIME_WEBHOOK_NOTIFICATION_TIME)
def test_mobile_commons_profile_already_exists(client, sample_donation, mock_actblue_webhook_auth):
    responses.add(
        responses.POST,
        'https://secure.mcommons.com/api/profile',
        body=MOBILE_COMMONS_PROFILE_RESPONSE,
        match_querystring=True,
    )

    try:
        res = client.post(
            url_for('actblue.donation'),
            headers={ 'Authorization': mock_actblue_webhook_auth },
            data=sample_donation,
        )
    except NotImplementedError:
        print(f'Waiting for implementation of upload_to_mobilecommons() : )')
        return

    assert len(responses.calls) == 1  # No profile_update request because one already exists.
    assert res.status_code == 204

@responses.activate
@freezegun.freeze_time(DAYTIME_WEBHOOK_NOTIFICATION_TIME)
def test_mobile_commons_profile_upload(client, sample_donation, mock_actblue_webhook_auth):
    responses.add(
        responses.POST,
        'https://secure.mcommons.com/api/profile',
        body=MOBILE_COMMONS_PROFILE_NOT_EXIST_RESPONSE,
        match_querystring=True,
    )

    responses.add_callback(
        responses.POST,
        'https://secure.mcommons.com/api/profile_update',
        callback=check_mobile_commons_request_body,
        match_querystring=True,
    )

    res = run_mock_actblue_webhook_auth(client, sample_donation, mock_actblue_webhook_auth)

    assert len(responses.calls) == 2
    assert res.status_code == 204


from datetime import datetime
from freezegun import freeze_time
@responses.activate
@freezegun.freeze_time('2019-06-17T04:32:24Z') #midnight
def test_mobile_commons_profile_upload_midnight_delayed(client, sample_donation, mock_actblue_webhook_auth):
    responses.add(
        responses.POST,
        'https://secure.mcommons.com/api/profile',
        body=MOBILE_COMMONS_PROFILE_NOT_EXIST_RESPONSE,
        match_querystring=True,
    )

    res = run_mock_actblue_webhook_auth(client, sample_donation, mock_actblue_webhook_auth)

    assert len(responses.calls) == 1
    return


@responses.activate
@freezegun.freeze_time('2019-06-17T04:32:24Z') #midnight
def test_mobile_commons_profile_upload_midnight_nodelayed(client, sample_donation, mock_actblue_webhook_auth):
    responses.add(
        responses.POST,
        'https://secure.mcommons.com/api/profile',
        body=MOBILE_COMMONS_PROFILE_NOT_EXIST_RESPONSE,
        match_querystring=True,
    )

    responses.add_callback(
        responses.POST,
        'https://secure.mcommons.com/api/profile_update',
        callback=check_mobile_commons_request_body,
        match_querystring=True,
    )

    #update sample_donation
    sample_donation = json.loads(sample_donation)
    sample_donation['contribution']['createdAt'] = "2019-06-17T03:49:32Z"
    sample_donation = json.dumps(sample_donation)

    res = run_mock_actblue_webhook_auth(client, sample_donation, mock_actblue_webhook_auth)

    assert len(responses.calls) == 2
    assert res.status_code == 204
    return
