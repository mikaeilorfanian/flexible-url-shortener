from django.core.urlresolvers import resolve, reverse
from django.test import TestCase


class TestShorTURLResolveAndReverse(TestCase):

    def test_short_url_correctly_constructed(self):
        url = reverse('short_url', args=['a'])
        self.assertEqual(url, '/a')

        url = reverse('short_url', args=['aBa'])
        self.assertEqual(url, '/aBa')

    def test_detail_url_correctly_constructed(self):
        url = reverse('url_detail', args=['a'])
        self.assertEqual(url, '/!a')

        url = reverse('url_detail', args=['aBa'])
        self.assertEqual(url, '/!aBa')

    def test_short_url_correctly_resolved(self):
        resolver = resolve('/a')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/ab')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/A')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/AA')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/01a')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/a01D')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/abcD')
        self.assertEqual(resolver.view_name, 'short_url')

        resolver = resolve('/D03f')
        self.assertEqual(resolver.view_name, 'short_url')

    def test_detail_url_correctly_resolved(self):
        resolver = resolve('/!a')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!ab')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!A')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!AA')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!01a')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!a01D')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!abcD')
        self.assertEqual(resolver.view_name, 'url_detail')

        resolver = resolve('/!D03f')
        self.assertEqual(resolver.view_name, 'url_detail')



