# ActBlue webhook handler.
#
# Fulfils two main roles:
# 1. Uploads incoming donation payloads to power some realtime
#    dashboards.
# 2. Uploads new phone numbers to Mobile Common profiles, to opt them
#    into our text message list.
#
# For reference, ActBlue webhook documentation is here:
#   https://secure.actblue.com/docs/webhooks

from functools import wraps
from datetime import datetime, time, timedelta
import pytz
import json

from flask import (
    Blueprint,
    Response,
    jsonify,
    request,
)
from nameparser import HumanName
# import boto3
import dateutil
from zappa.asynchronous import task

from common.mobile_commons import (
    create_or_update_mobile_commons_profile,
    profile_exists,
)
from common.input_validation import extract_phone_number
from common.settings import settings

mod = Blueprint('actblue', __name__)

OPT_IN_PATH_ID = '279022'

S3_BUCKET = 'ew-actblue-donations-incoming'

# This is naive, we may not want a lag this large
LAG_RANGE_HOURS = 1

EASTERN_TIMEZONE = 'US/Eastern'

EARLIER_TEXT_TIME_RANGE = 9

LATER_TEXT_TIME_RANGE = 21

def check_auth(username, password):
    return (username == settings.actblue_webhook_username() and
            password == settings.actblue_webhook_password())


def authenticate():
    return Response(
        'Could not verify your access level for that URL. You have to login with proper credentials',
        401,
        { 'WWW-Authenticate': 'Basic realm="Login Required"' }
    )


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


@mod.route('/donation', methods=['POST'])
@requires_auth
def donation():
    req_body = request.data
    try:
        event = json.loads(req_body)
    except ValueError:
        print(f'ActBlue - Bad Request - data: {req_body}')
        return ('Bad Request', 400)

    process_donation(event)
    return ('', 204)


@task
def process_donation(event):
    # write_to_s3(event)
    upload_to_mobilecommons(event)

# Note: we are also making the dt objects UTC offset-aware,
# which will help create timedelta objects
def tz_to_utc(dt):
    return dt.astimezone(pytz.utc)

def tz_to_eastern(dt):
    return dt.astimezone(pytz.timezone(EASTERN_TIMEZONE))

def lag_exists(dt_1, dt_2):
    delta = dt_1 - dt_2
    return True if delta > timedelta(hours=LAG_RANGE_HOURS) else False

def is_nighttime(dt):
    earlier = time(hour=EARLIER_TEXT_TIME_RANGE)
    later = time(hour=LATER_TEXT_TIME_RANGE)
    # If the time we pass in is between acceptable hours
    return False if earlier < tz_to_eastern(dt).time() < later else True

# def write_to_s3(event):
#     created_at = dateutil.parser.parse(event['contribution']['createdAt'])
#     time_now = datetime.datetime.now(datetime.timezone.utc)

#     key = f"{time_now.strftime('%Y-%m-%d_%H:%M:%S')}_{created_at.strftime('%Y-%m-%d_%H:%M:%S')}_{event['contribution']['orderNumber']}.json"
#     s3 = boto3.resource('s3')
#     body = json.dumps(event)
#     s3.Bucket(S3_BUCKET).put_object(Key=key, Body=body)


def upload_to_mobilecommons(event):
    """Given an incoming donation, creates new profile on Mobile Commons if appropriate.

    - Noop if donation does not have phone number.
    - Noop if webhook is hit during nighttime on the East coast after lag between donation and POST.
    - Does not attempt to create/update profile if one already exists in Mobile Commons.
    - Opts the phone number in to OPT_IN_PATH_ID opt-in path on Mobile Commons.
    - Normalizes first/last name in case it comes in as all lowercase/uppercase.
    """
    # Naive implementation: if it's nighttime on the East coast, don't send
    # any messages, unless the lag between contribution
    # creation time and now is less than a const (hardcoded).
    # The pytz package should handle DST for us.
    utc_now = tz_to_utc(datetime.now())
    contribution_string = event['contribution']['createdAt']
    # From ActBlue webhook documentation:
    # "createdAt": "ISO 8601 timestamp for the contribution (e.g. 2017-10-03T13:48:26-04:00)",
    # https://secure.actblue.com/docs/webhooks
    utc_contribution_dt = tz_to_utc(datetime.strptime(contribution_string, "%Y-%m-%dT%H:%M:%S%z"))
    if is_nighttime(utc_now) and lag_exists(utc_now, utc_contribution_dt):
        return

    donor_phone = event['donor']['phone']
    if extract_phone_number(donor_phone) == None or profile_exists(donor_phone):
        return

    print(f'upload_to_mobilecommons with event: {json.dumps(event, indent=2)}')
    human_name = HumanName(event['donor']['firstname'] + " " + event['donor']['lastname'])
    human_name.capitalize()
    data = {
        "phone_number" : donor_phone,
        "email" : event['donor']['email'],
        "postal_code" : event['donor']['zip'],
        "first_name" : human_name['first'],
        "last_name" : human_name['last'],
        "street1" : event['donor']['addr1'],
        "city" : event['donor']['city'],
        "state" : event['donor']['state'],
        "country" : "US",
        "opt_in_path_id" : OPT_IN_PATH_ID,
    }
    create_or_update_mobile_commons_profile(data)
