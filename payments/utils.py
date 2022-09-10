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


def generate_reservation_token(payment_date):
    expiry = payment_date + timedelta(days=5)
    token = jwt.encode(
        {"exp": expiry},
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
        user = User.objects.get(id=metadata["userID"])

        Payment.objects.create(
            user=user, bus=user.bus, payment_date=payment_date, amount=amount
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
