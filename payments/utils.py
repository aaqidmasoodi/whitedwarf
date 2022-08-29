from core.settings import SECRET_KEY
from datetime import datetime, timedelta
import jwt


def generate_token(user):
    expiry = datetime.now() + timedelta(seconds=30)
    token = jwt.encode(
        {"user": user, "exp": expiry},
        SECRET_KEY,
        algorithm="HS256",
    )

    return token
