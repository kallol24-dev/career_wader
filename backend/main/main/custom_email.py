# foodie_email.py

import requests
import time
from .applogger import AppLogger #type: ignore

logger = AppLogger.get_logger("FoodieEmail")

class CareerWaderEmail:
    api_url = "https://api.zeptomail.in/v1.1/email"
    api_token = "Zoho-enczapikey PHtE6r0LFLziiWItoREI5//rEsb1Pdl8+LxvKVQWuNtLX6IEHE1VqNsvmmSxoh14UKJFEPHIyt1t5bPIsrrRd2m+ZGcZX2qyqK3sx/VYSPOZsbq6x00ct14ScEHUXY7tddBq3SbVs97eNA=="

    def __init__(self, to_email=None, subject=None, html_body=None, from_email="support@careerwader.in"):
        self.to_email = to_email
        self.subject = subject
        self.html_body = html_body
        self.from_email = from_email

    def send_email(self, to_email=None, subject=None, html_body=None, from_email=None, retries=3, timeout=10):
        to_email = to_email or self.to_email
        subject = subject or self.subject
        html_body = html_body or self.html_body
        from_email = from_email or self.from_email

        if not all([to_email, subject, html_body]):
            raise ValueError("Missing email fields (to_email, subject, html_body).")

        headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }

        data = {
            "from": {
                "address": from_email,
                "name": "Career Wader"
            },
            "to": [
                {
                    "email_address": {
                        "address": to_email,
                        "name": ""
                    }
                }
            ],
            "subject": subject,
            "htmlbody": html_body
        }

        attempt = 0
        while attempt < retries:
            try:
                logger.info(f"Sending email to {to_email} (attempt {attempt + 1})")
                response = requests.post(self.api_url, json=data, headers=headers, timeout=timeout)

                if response.status_code == 201:
                    logger.info("Email sent successfully.")
                    return True, "Email sent successfully!"
                else:
                    logger.warning(f"Failed with status {response.status_code}: {response.text}")
                    return False, response.text

            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed: {e}")
                attempt += 1
                if attempt < retries:
                    sleep_time = 2 ** attempt
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                else:
                    logger.error("Max retries reached. Giving up.")
                    return False, str(e)
