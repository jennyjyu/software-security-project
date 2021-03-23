from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordNumberValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError("Passwords must contain at least on characher that is a digit.")
        
    def get_help_text(self):
        return _("Passwords must contain at least on characher that is a digit.")

class PasswordUppdercaseValidator:
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError("Passwords must contain at least on characher that is uppercase.")
        
    def get_help_text(self):
        return _("Passwords must contain at least on characher that is uppercase.")

class PasswordLowercaseValidator:
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError("Passwords must contain at least on characher that is lowercase.")
        
    def get_help_text(self):
        return _("Passwords must contain at least on characher that is lowercase.")

