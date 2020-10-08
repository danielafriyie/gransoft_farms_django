from django.test import SimpleTestCase
from django.urls import reverse, resolve

from user_accounts import views, urls


class TestUrls(SimpleTestCase):

    def test_create_account_url_is_resolved(self):
        url = reverse('user_accounts:create_user_account')
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.CreateUserAccount)
        self.assertEqual(res.app_name, urls.app_name)
        self.assertEqual(res.route, url.lstrip('/'))

    def test_manage_users_url_is_resolved(self):
        url = reverse('user_accounts:manage_users')
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.ManageUserAccount)
        self.assertEqual(res.app_name, urls.app_name)
        self.assertEqual(res.route, url.lstrip('/'))

    def test_toggle_user_status_url_is_resolved(self):
        url = reverse('user_accounts:toggle_user_status')
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.ToggleUserStatus)
        self.assertEqual(res.app_name, urls.app_name)
        self.assertEqual(res.route, url.lstrip('/'))

    def test_delete_user_url_is_resolved(self):
        url = reverse('user_accounts:delete_user', args=(9999,))
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.DeleteUser)
        self.assertEqual(res.app_name, urls.app_name)

    def test_update_user_url_is_resolved(self):
        url = reverse('user_accounts:update_user', args=(9999,))
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.UpdateUserAccount)
        self.assertEqual(res.app_name, urls.app_name)

    def test_set_user_password_url_is_resolved(self):
        url = reverse('user_accounts:set_user_password')
        res = resolve(url)
        self.assertEqual(res.func.view_class, views.SetUserPassword)
        self.assertEqual(res.app_name, urls.app_name)
        self.assertEqual(res.route, url.lstrip('/'))
