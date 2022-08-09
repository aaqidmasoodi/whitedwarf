import random
import requests
import os
from dotenv import load_dotenv


load_dotenv()
OTP_2FACTOR_API_KEY = os.getenv("OTP_2FACTOR_API_KEY")


def send_otp(phone: str) -> int or None:
    if phone:
        otp = random.randint(1000, 9999)
        print(f"{otp} is your OTP for {phone}.")
        try:
            requests.get(
                f"https://2factor.in/API/V1/{OTP_2FACTOR_API_KEY}/SMS/{phone}/{otp}/cusbrs_template"
            )
            return otp
        except:
            return None
