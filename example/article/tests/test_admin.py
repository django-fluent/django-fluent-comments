from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.test import TestCase

from article.tests import factories

try:
    from django.urls import reverse
except ImportError:  # Django<2.0
    from django.core.urlresolvers import reverse


class AdminCommentsTests(TestCase):

    def test_admin_comments_access(self):
        """
        See that the admin renders
        """
        admin = User.objects.create_superuser('admin2', 'admin@example.com', 'secret')
        comment = factories.create_comment(user_name='Test-Name')

        self.client.login(username=admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, ">Test-Name<", status_code=200)
