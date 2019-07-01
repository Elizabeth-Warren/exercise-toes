from functools import wraps
import datetime
import json

from flask import (
    Blueprint,
    Response,
    jsonify,
    request,
)
from nameparser import HumanName
import boto3
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
#WHITELIST_ONLY_PHONE = ['15105016227', '18287138291', '17862830447']  # (11 digits with leading 1)
WHITELIST_ONLY_PHONE = []  # Empty whitelist allows all numbers.

LATEST_SEND_HOUR_UTC = 1  # 9pm EDT
EARLIEST_SEND_HOUR_UTC = 13  # 9am EDT

S3_BUCKET = 'ew-actblue-donations-incoming'

# If there is more lag than this between donation creation and webhook
# invocation, we'll limit sending to 9am-9pm Eastern.
LOTS_OF_LAG_THRESHOLD_SECONDS = 5 * 60


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
    upload_to_mobilecommons(event)
    write_to_s3(event)


def upload_to_mobilecommons(event):
    donor = event['donor']
    if 'phone' not in donor or not donor['phone']:
        return
    phone_number = extract_phone_number(donor['phone'])
    if not phone_number:
        return

    print(f'ActBlue webhook with phone number. Donation at {event["contribution"]["createdAt"]} by {json.dumps(donor, indent=2)}')

    if WHITELIST_ONLY_PHONE and phone_number not in WHITELIST_ONLY_PHONE:
        return

    if webhook_notification_was_significantly_lagged(event['contribution']['createdAt']) and not allowed_sending_time():
        print(f'Webhook notification was lagged and now we are not in allowed sending time. Not creating profile for {phone_number}.')
        return

    profile_already_exists = profile_exists(phone_number)
    if profile_already_exists:
        print(f'Profile already exists for number {phone_number}')
    else:
        create_or_update_mobile_commons_profile(profile_payload(donor))


def write_to_s3(event):
    created_at = dateutil.parser.parse(event['contribution']['createdAt'])
    time_now = datetime.datetime.now(datetime.timezone.utc)

    key = f"{time_now.strftime('%Y-%m-%d_%H:%M:%S')}_{created_at.strftime('%Y-%m-%d_%H:%M:%S')}_{event['contribution']['orderNumber']}.json"
    s3 = boto3.resource('s3')
    body = json.dumps(event)
    s3.Bucket(S3_BUCKET).put_object(Key=key, Body=body)


def webhook_notification_was_significantly_lagged(created_at_str):
    created_at = dateutil.parser.parse(created_at_str)
    webhook_invoked_at = datetime.datetime.now(datetime.timezone.utc)
    lag_in_seconds = (webhook_invoked_at - created_at).seconds
    print(f'Lag between donation creation {created_at_str} (parsed to {created_at}) and webhook invocation {webhook_invoked_at}: {lag_in_seconds} seconds')
    return lag_in_seconds > LOTS_OF_LAG_THRESHOLD_SECONDS


def allowed_sending_time():
    """Returns true if the time of day is roughly sane for sending text messages in the US.

    Ideally ActBlue would hit our webhook immediately after a donation
    is sent; but in reality, there can be a significant lag between
    donation and webhook. So we double check that it's not the middle of
    the night and allow sending only between 9am EDT and 11pm EDT.
    """
    hour_utc = datetime.datetime.utcnow().time().hour
    return hour_utc >= EARLIEST_SEND_HOUR_UTC or hour_utc < LATEST_SEND_HOUR_UTC


def profile_payload(donor):
    """Prepares payload for profile_update Mobile Commons API endpoint.

    As described in
      https://community.uplandsoftware.com/hc/en-us/articles/204494185-REST-API#ProfileUpdate
    """
    first_name, last_name = normalize_name(donor.get('firstname', ''), donor.get('lastname', ''))
    payload = {
        'phone_number': donor['phone'],
        'email': donor.get('email', ''),
        'postal_code': donor.get('zip', ''),
        'first_name': first_name,
        'last_name': last_name,
        'street1': donor.get('addr1', ''),
        'city': donor.get('city',  ''),
        'state': donor.get('state', ''),
        'country': 'US',
        'opt_in_path_id': OPT_IN_PATH_ID,
    }

    # Don't upload null or empty fields.
    keys_to_delete = [k for k, v in payload.items() if not v]
    for k in keys_to_delete:
        del payload[k]

    return payload


def normalize_name(first_name, last_name):
    """Normalizes capitalization of first and last name."""
    name = HumanName()
    name.first = first_name
    name.last = last_name
    name.capitalize()
    return (name.first, name.last)
