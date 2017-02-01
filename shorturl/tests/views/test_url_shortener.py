from django.contrib.auth.models import User
from django.test import TestCase

from shorturl.models import ShortURLCombination, URL


class TestSuccessView(TestCase):

    def setUp(self):
        User.objects.create_user(username='abcd')
        User.objects.create_user(username='xyzh')
        User.objects.create_user(username='0123')
        ShortURLCombination.objects.create(combination='a')
        ShortURLCombination.objects.create(combination='ab')
        ShortURLCombination.objects.create(combination='abc')

    def test_new_long_url_shortened_correctly(self):
        response = self.client.post('/', {'long_url': 'http://www.google.com'})

        self.assertEqual(URL.objects.count(), 1)
        self.assertIn(b'href="/a"', response.content)

    def test_duplicate_long_url_shortened_only_once(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        response = self.client.post('/', {'long_url': 'http://www.google.com'})

        self.assertEqual(URL.objects.count(), 1)
        self.assertIn(b'href="/a"', response.content)


class TestShortURLView(TestCase):

    def setUp(self):
        User.objects.create_user(username='abcd')
        User.objects.create_user(username='xyzh')
        User.objects.create_user(username='0123')
        ShortURLCombination.objects.create(combination='a')
        ShortURLCombination.objects.create(combination='ab')
        ShortURLCombination.objects.create(combination='abc')

    def test_non_existing_short_url_invokes_error_message(self):
        response = self.client.get('/z')

        self.assertIn(b"Invalid", response.content)

    def test_existing_short_url_redirects_increases_count(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        response = self.client.get('/a')

        self.assertEqual(response.status_code, 302)

        url_obj = URL.objects.filter(converted_url__combination='a').first()
        self.assertEqual(url_obj.visit_count, 1)

    def test_visiting_short_url_twice_increases_count_twice(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        self.client.get('/a')
        self.client.get('/a')

        url_obj = URL.objects.filter(converted_url__combination='a').first()
        self.assertEqual(url_obj.visit_count, 2)


class TestURLDetailView(TestCase):

    def setUp(self):
        User.objects.create_user(username='abcd')
        User.objects.create_user(username='xyzh')
        User.objects.create_user(username='0123')
        ShortURLCombination.objects.create(combination='a')
        ShortURLCombination.objects.create(combination='ab')
        ShortURLCombination.objects.create(combination='abc')

    def test_non_existing_short_url_details_invokes_error_message(self):
        response = self.client.get('/!z')

        self.assertIn(b"Invalid", response.content)

    def test_unvisited_short_url_has_count_zero(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        response = self.client.get('/!a')

        self.assertIn(b"Count: 0", response.content)

    def test_visited_short_url_has_count_one(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        self.client.get('/a')
        response = self.client.get('/!a')

        self.assertIn(b"Count: 1", response.content)

    def test_visiting_details_view_doesnt_increase_visit_count(self):
        self.client.post('/', {'long_url': 'http://www.google.com'})
        self.client.get('/a')
        self.client.get('/!a')
        response = self.client.get('/!a')

        self.assertIn(b"Count: 1", response.content)
