from django.core.validators import RegexValidator

GENDER_CHOICES = (
  (0, 'Male'), (1, 'Female')
)
STATUS_E_CHOICES = (
  (0, 'Do not'),
  (1, 'Done')
)
STATUS_B_CHOICES = (
  (0, 'Waiting'),
  (1, 'Done')
)

phone_regex = RegexValidator(regex=r'((09|03|07|08|05)+([0-9]{8})\b)',
    message="The phone number you entered is not in the correct format")
