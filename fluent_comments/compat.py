"""Compatibility fixes that can't be resolved with an simple ``except ImportError``"""
import django


if django.VERSION >= (1, 10):
    def is_authenticated(user):
        return user.is_authenticated  # CallableBool or bool
else:
    def is_authenticated(user):
        return user.is_authenticated()  # Method

