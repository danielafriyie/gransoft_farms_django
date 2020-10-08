from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from django.urls import reverse
import json

from user_accounts.models import UserAccountsModel

auth_user = get_object_or_404(UserAccountsModel, pk=1)


class TestViews(TestCase):

    def setUp(self):
        pass

    def test_create_user_account_GET(self):
        s_user_details = {
            'username': 'test_super_user',
            'password': 'test',
            'name': 'Test User',
            'phone_no': '1111111111',
            'gender': 'Male',
            'date_of_birth': '1990-01-01',
            'auth_user': auth_user
        }
        s_user = UserAccountsModel.objects.create_superuser(**s_user_details)
        client = Client()
        client.login(username=s_user_details['username'], password=s_user_details['password'])
        response = client.get(reverse('user_accounts:create_user_account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_accounts/create_account.html')
