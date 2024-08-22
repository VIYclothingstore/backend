import re

from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    def __init__(self, pattern=None):
        self.pattern = pattern or r"^(\S){6,}$"

    def validate(self, password, user=None):
        if not re.match(self.pattern, password):
            raise ValidationError(
                "The password must consist of any characters and have a length of at least 6"
            )


class CustomFullNameValidator:
    def __init__(self, pattern=None):
        self.pattern = pattern or r"^[^\d^Ы^ы^Ё^ё^Э^э\W]+$"

    def validate(self, first_name, last_name, surname):
        if not re.match(self.pattern, first_name):
            raise ValidationError(
                "The first name can only contain letters and must be at least 1 character long"
            )
        if not re.match(self.pattern, last_name):
            raise ValidationError(
                "The last name can only contain letters and must be at least 1 character long"
            )
        if not re.match(self.pattern, surname):
            raise ValidationError(
                "The surname can only contain letters and must be at least 1 character long"
            )
