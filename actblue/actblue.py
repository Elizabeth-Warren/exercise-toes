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
import datetime
import json

from flask import (
    Blueprint,
    Response,
    jsonify,
    request,
)
from nameparser import HumanName
import dateutil
import pytz

from common.mobile_commons import (
    create_or_update_mobile_commons_profile,
    profile_exists,
)
from common.input_validation import extract_phone_number
from common.settings import settings

mod = Blueprint('actblue', __name__)

OPT_IN_PATH_ID = '279022'


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

    upload_to_mobilecommons(event)
    return ('', 204)


def upload_to_mobilecommons(event):
    """Given an incoming donation, creates new profile on Mobile Commons if appropriate.

    - Noop if donation does not have phone number.
    - Does not attempt to create/update profile if one already exists in Mobile Commons.
    - Opts the phone number in to OPT_IN_PATH_ID opt-in path on Mobile Commons.
    - Normalizes first/last name in case it comes in as all lowercase/uppercase.
    """
    # TODO: implement this method : )
    #
    # Things you can use (they're already imported):
    #
    # * extract_phone_number() from common/input_validation.py
    # * create_or_update_mobile_commons_profile() and profile_exists() from common/mobile_commons.py
    # * OPT_IN_PATH_ID
    # * HumanName (imported from nameparser module)

    print(f'upload_to_mobilecommons with event: {json.dumps(event, indent=2)}')
    raise(NotImplementedError)
