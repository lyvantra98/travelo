from django.core.validators import RegexValidator

GENDER_CHOICES = (
  (0, 'Male'), (1, 'Female')
)
STATUS_E_CHOICES = (
  (0, 'do_not'),
  (1, 'done')
)
STATUS_B_CHOICES = (
  (0, 'waiting'),
  (1, 'done')
)

phone_regex = RegexValidator(regex=r'^0(1\d{9}|9\d{8})$',
    message="The phone number you entered is not in the correct format")
