import itertools

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from shorturl.models import ShortURLCombination


class Command(BaseCommand):
    help = 'generate short URL combinations'

    def handle(self, *args, **options):
        start = settings.SHORT_URL_LENGTH_BOUND[0]
        end = settings.SHORT_URL_LENGTH_BOUND[1]

        if end < start:
            raise CommandError(
                'Upper bound cannot be smaller than the lower bound!'
                'Fix SHORT_URL_LENGTH_BOUND in settings.py'
            )

        for length in range(start, end+1):
            self.stdout.write(
                'Generating components of length %s ...' % length)
            generate_combinations_with_length(length=length)

        self.stdout.write(self.style.SUCCESS(
            'Successfully populated the db with short URL path components.'))


def generate_combinations_with_length(length):
    for perm in itertools.product(settings.PATH_COMPONENT_CHARSET, repeat=length):
        ShortURLCombination.objects.create(combination=''.join(perm))
