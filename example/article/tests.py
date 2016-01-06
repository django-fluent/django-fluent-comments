# -*- coding: utf-8 -*-

# Author: Petr Dlouhý <petr.dlouhy@auto-mat.cz>
#
# Copyright (C) 2015 o.s. Auto*Mat
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from freezegun import freeze_time


class CommentsTests(TestCase):
    fixtures = ["data", ]

    def setUp(self):
        self.admin = User.objects.create_superuser('superuser', 'myemail@test.com', 'secret')

    def test_admin_comments_access(self):
        self.client.login(username=self.admin.username, password='secret')
        response = self.client.get(reverse('admin:fluent_comments_fluentcomment_changelist'))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    def test_get_article_with_comment(self):
        response = self.client.get(reverse('article-details', kwargs={"slug": "testing-article"}))
        self.assertContains(response, "Comment", status_code=200)

    @freeze_time("2016-01-04 17:00:00")
    def test_comment_post(self):
        post_data = {
            "content_type": "article.article",
            "object_pk": 1,
            "name": "Testing name",
            "email": "test@email.com",
            "comment": "Testing comment",
            "timestamp": "1451919617",
            "security_hash": "040d5412fd16c32983860e8796591a05a6856eb2",
        }
        response = self.client.post(reverse("comments-post-comment-ajax"), post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(response, "Testing comment", status_code=200)
        self.assertEqual(response.status_code, 200, response.content.decode("utf-8"))
