import random


# link = f"https://2factor.in/API/V1/{api_key}/SMS/{phone_number}/{otp}/{template_name}"


def send_otp(phone: str) -> int or None:
    if phone:
        otp = random.randint(1000, 9999)
        print(f"{otp} is your OTP for {phone}.")
        return otp

    return None
