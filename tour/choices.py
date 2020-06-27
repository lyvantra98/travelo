from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'((09|03|07|08|05)+([0-9]{8})\b)',
    message="The phone number you entered is not in the correct format")
