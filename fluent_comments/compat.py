"""Compatibility fixes that can't be resolved with an simple ``except ImportError``"""
import django


if django.VERSION >= (1, 10):
    def is_authenticated(user):
        assert isinstance(user.is_authenticated, bool)
        return user.is_authenticated
else:
    def is_authenticated(user):
        assert not isinstance(user.is_authenticated, bool)
        return user.is_authenticated


