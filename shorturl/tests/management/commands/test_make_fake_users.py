from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.utils.six import StringIO



class TestFakeUsersAreCreatedCorrectly(TestCase):

    def test_correct_number_of_users_created(self):
        command_output = StringIO()
        call_command('make_fake_users', 30, stdout=command_output)

        self.assertIn(
            'Successfully added 30 fake users!', command_output.getvalue())
        self.assertEqual(User.objects.count(), 30)

    def test_zero_number_users_made_when_0_passed_as_command_argument(self):
        command_output = StringIO()
        call_command('make_fake_users', 0, stdout=command_output)

        self.assertIn(
            'No users created!', command_output.getvalue())
        self.assertEqual(User.objects.count(), 0)

    def test_more_than_5000_users_throws_error(self):
        self.assertRaises(
            CommandError, call_command, 'make_fake_users', 5001)
        self.assertEqual(User.objects.count(), 0)
