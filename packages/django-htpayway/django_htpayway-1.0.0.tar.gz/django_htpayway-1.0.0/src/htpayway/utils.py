from django.http import HttpRequest
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from decimal import Decimal

from .models import Transaction
from .config import get_payway_class
from .forms import PaymentForm


def begin_transaction(request: HttpRequest, pgw_data, htpayway_class=None):
    """This should be called from your view
    to create Transaction object.
    """

    user = request.user if request.user.is_authenticated else None
    amount = pgw_data["amount"]

    tx = Transaction()
    tx.status = "created"
    tx.user = user

    """
    result.pgw_shop_id = pgw_data['pgw_shop_id']
    result.pgw_authorization_type = pgw_data['pgw_authorization_type']
    result.pgw_order_id = pgw_data['pgw_order_id']

    result.pgw_first_name = pgw_data.get('pgw_first_name', ''),
    result.pgw_last_name = pgw_data.get('pgw_last_name', ''),
    result.pgw_street = pgw_data.get('pgw_street', ''),
    result.pgw_city = pgw_data.get('pgw_city', ''),
    result.pgw_post_code = pgw_data.get('pgw_post_code', ''),
    result.pgw_country = pgw_data.get('pgw_country', ''),
    result.pgw_email = pgw_data.get('pgw_email', ''),
    """

    PayWayClass = get_payway_class(htpayway_class)()
    payway_data = PayWayClass.pgw_data()

    # every property that starts with `pgw_` should
    # be set as an attribute of a Transaction instance
    for x in payway_data:
        setattr(tx, x, payway_data[x])

    # and then we do the same for the `pgw_data` that was passed in
    for x in pgw_data:
        if x.startswith("pgw_"):
            setattr(tx, x, pgw_data[x])

    # setting success_url and failure_url if they were not passed in
    domain = request.get_host()
    protocol = request.scheme
    if tx.pgw_success_url is None:
        success_path = reverse("htpayway:success")
        tx.pgw_success_url = f"{protocol}://{domain}{success_path}"
    if tx.pgw_failure_url is None:
        failure_path = reverse("htpayway:failure")
        tx.pgw_failure_url = f"{protocol}://{domain}{failure_path}"

    # amount must be formatted according to the spec
    tx.amount = amount
    tx.pgw_amount = format_amount(amount)

    tx.pgw_signature = tx.calc_outgoing_signature()

    tx.save()
    return tx


def format_amount(amount):
    a = Decimal(amount).quantize(Decimal("0.01"))
    return str(a).replace(".", "")


def render_payway_form(request, transaction_id):
    transaction = get_object_or_404(
        Transaction, pk=int(transaction_id), status="created"
    )
    payway = get_payway_class()(
        request=request, transaction=transaction, **transaction.pgw_data()
    )

    form = PaymentForm(initial=payway.pgw_data())
    return render(
        request,
        "htpayway/payway-form.html",
        {"form": form, "form_url": payway.pgw_form_url},
    )
