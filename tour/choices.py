from django.core.validators import RegexValidator

phone_regex = RegexValidator(regex=r'((09|03|07|08|05)+([0-9]{8})\b)',
    message="Số điện thoại không đúng định dạng")
