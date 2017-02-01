import requests

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class TooManyUsersError(Exception):
    pass


class Command(BaseCommand):
    help = 'populate db with fake users'

    def add_arguments(self, parser):
        parser.add_argument('num_users', type=int)

    def handle(self, *args, **options):
        num_users = options['num_users']
        if num_users == 0:
            self.stdout.write(self.style.SUCCESS('No users created!'))
            return

        try:
            create_fake_users(num_users)
            self.stdout.write(self.style.SUCCESS(
                'Successfully added %s fake users!' % num_users))
        except TooManyUsersError:
            raise CommandError('You asked to make too many users! 5000 is the '
                               'most you can make each time you run this '
                               'command')


def create_fake_users(num_users):
    if num_users > 5000:
        raise TooManyUsersError

    full_url = 'https://randomuser.me/api/?results=' + str(num_users)
    r = requests.get(full_url)

    if r.status_code == 200:
        results = r.json()['results']
        for user_json in results:
            User.objects.create_user(
                first_name=user_json['name']['first'],
                last_name=user_json['name']['last'],
                username=user_json['login']['username'],
                email=user_json['email'],
                password=user_json['login']['password'],
                date_joined=user_json['registered']
            )
