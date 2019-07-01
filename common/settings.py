from common.parameter_store import get_parameter

class Settings:
    _mobile_commons_username = None
    _mobile_commons_password = None

    _actblue_webhook_username = None
    _actblue_webhook_password = None

    def mobile_commons_username(self):
        if not self._mobile_commons_username:
            self._mobile_commons_username = get_parameter('MOBILE_COMMONS_USERNAME')
        return self._mobile_commons_username

    def mobile_commons_password(self):
        if not self._mobile_commons_password:
            self._mobile_commons_password = get_parameter('MOBILE_COMMONS_PASSWORD', with_decryption=True)
        return self._mobile_commons_password

    def actblue_webhook_username(self):
        if not self._actblue_webhook_username:
            self._actblue_webhook_username = get_parameter('actblue_webhook_username')
        return self._actblue_webhook_username

    def actblue_webhook_password(self):
        if not self._actblue_webhook_password:
            self._actblue_webhook_password = get_parameter('actblue_webhook_password', with_decryption=True)
        return self._actblue_webhook_password


settings = Settings()
