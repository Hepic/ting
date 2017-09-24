from chat.tests.sessions.common import *
from chat.tests.users.common import *


class SessionTests(ChatTests):
    def test_login_with_invalid_username(self):
        post_dict_1 = {}
        post_dict_2 = {'username': ''}

        response_1 = self.client.post(
            reverse('chat:session'),
            post_dict_1
        )

        response_2 = self.client.post(
            reverse('chat:session'),
            post_dict_2
        )

        self.assertEqual(response_1.status_code, 400)
        self.assertEqual(response_2.status_code, 400)

    def test_login_with_reserved_username_and_password_set_and_no_password(self):
        create_user(username='guest', password='pass')
        post_dict = {'username': 'guest'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 403)

    def test_login_with_reserved_username_and_password_set_and_wrong_password(self):
        create_user(username='guest', password='pass')
        post_dict = {'username': 'guest', 'password': 'wrong'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 403)

    def test_login_with_reserved_username_and_no_password_set_and_no_password(self):
        create_user(username='guest')
        post_dict = {'username': 'guest'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 403)

    def test_login_with_reserved_username_and_no_password_set_and_password(self):
        create_user(username='guest')
        post_dict = {'username': 'guest', 'password': 'whatever'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 403)

    def test_login_with_unreserved_username_and_password(self):
        post_dict = {'username': 'guest', 'password': 'whatever'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 404)

    def test_login_with_reserved_username_and_password_set_and_correct_password(self):
        create_user(username='guest', password='pass')
        post_dict = {'username': 'guest', 'password': 'pass'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 204)

    def test_login_with_unreserved_and_no_password(self):
        post_dict = {'username': 'guest'}

        response = self.client.post(
            reverse('chat:session'),
            post_dict
        )

        self.assertEqual(response.status_code, 204)
