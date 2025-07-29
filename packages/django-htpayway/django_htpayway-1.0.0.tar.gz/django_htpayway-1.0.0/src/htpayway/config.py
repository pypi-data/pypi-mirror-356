from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse
from django.utils.module_loading import import_string
from django.conf import settings

import hashlib


class PayWay:
    pgw_language = ""
    pgw_authorization_type = "1"
    pgw_disable_installments = "1"
    pgw_return_method = "POST"
    pgw_success_url = None
    pgw_failure_url = None

    def __init__(self, request=None, **pgw_data):
        skip = ["pgw_shop_id"]
        self.request = request
        for x in pgw_data:
            if x.startswith("pgw_"):
                if x in skip:
                    continue
                setattr(self, x, pgw_data[x])

    def pgw_data(self):
        return {x: getattr(self, x) for x in dir(self) if x.startswith("pgw_")}

    def calc_incoming_signature(self, data):
        """Calculates hash signature based on incoming request data"""
        signature_string = ""
        for item in data:
            signature_string += item
            signature_string += self.pgw_secret_key
        return hashlib.sha512(signature_string.encode("utf-8")).hexdigest()

    def on_success(self, transaction) -> HttpResponse | None:
        raise NotImplementedError

    def on_failure(self, transaction) -> HttpResponse | None:
        raise NotImplementedError

    @property
    def pgw_shop_id(self) -> str:
        return settings.HTPAYWAY_SHOP_ID

    @property
    def pgw_secret_key(self) -> str:
        return settings.HTPAYWAY_SECRET_KEY

    @property
    def pgw_form_url(self) -> str:
        return settings.HTPAYWAY_FORM_URL


def get_payway_class(htpayway_class=None):
    if htpayway_class is None:
        htpayway_class = settings.HTPAYWAY_CLASS

    if isinstance(htpayway_class, str):
        try:
            return import_string(htpayway_class)
        except AttributeError as e:
            raise ImproperlyConfigured(e)
    else:
        return htpayway_class
