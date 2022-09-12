from core.settings import SECRET_KEY
from datetime import datetime, timedelta
import jwt
from payments.models import Payment, SeatReservationStatus
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_token(user):
    expiry = datetime.now() + timedelta(seconds=30)
    token = jwt.encode(
        {"user": user, "exp": expiry},
        SECRET_KEY,
        algorithm="HS256",
    )

    return token


def generate_reservation_token():
    expiry = datetime.now() + timedelta(seconds=300)
    token = jwt.encode(
        {"Token": "CUKBRSPAYMENT", "exp": expiry},
        SECRET_KEY,
        algorithm="HS256",
    )

    return token


def handle_payment(payment_intent):
    try:

        amount = payment_intent["amount"] / 100
        metadata = payment_intent["metadata"]
        epoch = payment_intent["created"]
        payment_date = datetime.fromtimestamp(epoch)
        transaction_id = payment_intent["charges"]["data"][0]["balance_transaction"]
        card_brand = payment_intent["charges"]["data"][0]["payment_method_details"][
            "card"
        ]["brand"]
        card_brand_last_4_digits = payment_intent["charges"]["data"][0][
            "payment_method_details"
        ]["card"]["last4"]

        user = User.objects.get(id=metadata["userID"])

        Payment.objects.create(
            user=user,
            bus=user.bus,
            payment_date=payment_date,
            amount=amount,
            transaction_id=transaction_id,
            payment_method="card",
            card_brand=card_brand,
            card_last4=card_brand_last_4_digits,
        ).save()

        reservation_token = generate_reservation_token(payment_date)

        try:
            record = SeatReservationStatus.objects.filter(user=user).first()
            record.token = reservation_token
            record.bus = user.bus
            record.save()

        except SeatReservationStatus.DoesNotExist:
            return False

        return True
    except Exception as e:

        print(f"Handle Payment Error: {e}")
        return False
