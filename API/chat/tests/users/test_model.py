from chat.tests.users.common import *

class TingUserModelTests(ChatTests):
    def test_user_create_with_password(self):
        user = create_user('guest', 'pass')

        users = User.objects.all().select_related('tinguser').filter(pk=user.id)
        self.assertTrue(users.exists())
        self.assertEqual(users.count(), 1)

        dbmessage = users[0]
        self.assertEqual(dbmessage.username, user.username)
        self.assertEqual(dbmessage.password, user.password)
        self.assertEqual(dbmessage.email, user.email)
        self.assertEqual(dbmessage.tinguser.gender, user.tinguser.gender)
        self.assertEqual(dbmessage.tinguser.birthday, user.tinguser.birthday)
        self.assertEqual(dbmessage.tinguser.last_used, user.tinguser.last_used)

    def test_user_create_without_password(self):
        user = create_user('guest')

        users = User.objects.all().select_related('tinguser').filter(pk=user.id)
        self.assertTrue(users.exists())
        self.assertEqual(users.count(), 1)

        dbmessage = users[0]
        self.assertEqual(dbmessage.username, user.username)
        self.assertEqual(dbmessage.password, user.password)
        self.assertEqual(dbmessage.email, user.email)
        self.assertEqual(dbmessage.tinguser.gender, user.tinguser.gender)
        self.assertEqual(dbmessage.tinguser.birthday, user.tinguser.birthday)
        self.assertEqual(dbmessage.tinguser.last_used, user.tinguser.last_used)
