from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect
import six



class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
        def _make_hash_value(self, user, timestamp):
            return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)
account_activation_token = AccountActivationTokenGenerator()


class AccountResetTokenGenerator(PasswordResetTokenGenerator):
        def _make_hash_value(self, user, timestamp):
            return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)
account_reset_token = AccountResetTokenGenerator()


def redirect_authenticated_user(function):
    def _function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')  # Change 'index' to the desired URL name if needed
        return function(request, *args, **kwargs)
    return _function