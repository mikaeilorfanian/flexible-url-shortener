from django.conf import settings
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

from shorturl.models import ShortURLCombination



class TestGeneratePathComponentCombinations(TestCase):

    def test_correct_number_of_combinations_created(self):
        settings.SHORT_URL_LENGTH_BOUND = (3, 8)
        settings.PATH_COMPONENT_CHARSET = '1A'

        call_command('generate_path_component_combinations')
        self.assertEqual(ShortURLCombination.objects.count(), 504)

    def test_uppper_bound_equal_to_lower_bound(self):
        settings.SHORT_URL_LENGTH_BOUND = (3, 3)
        settings.PATH_COMPONENT_CHARSET = '1A'

        call_command('generate_path_component_combinations')
        self.assertEqual(ShortURLCombination.objects.count(), 8)


    def test_upper_bound_smaller_than_lower_bound_raises_exception(self):
        settings.SHORT_URL_LENGTH_BOUND = (3, 2)

        self.assertRaises(
            CommandError, call_command, 'generate_path_component_combinations')
        self.assertEqual(ShortURLCombination.objects.count(), 0)
