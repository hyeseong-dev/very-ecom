'''
./magepy test appname.tests.modulename
'''
from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse

from store.models import Category, Product
from store.views import all_products


@skip('demonstrating.skipping')
class TestSkip(TestCase):
    def test_skip_example(self):
        pass

class TestViewResponses(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        User.objects.create(username='admin')
        Category.objects.create(name='django', slug='django')
        Product.objects.create(category_id=1, title='django beginners', created_by_id=1,
                                slug='django-beginners', price='20000.00', image='django')

    def test_url_allowed_hosts(self):
        '''
        Test allowed hosts
        '''
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='127.0.0.1')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/', HTTP_HOST='localhost')
        self.assertEqual(response.status_code, 200)
        
    def test_homepage_url(self):
        '''
        Test homepage response status
        '''
        request = HttpRequest()
        response = self.c.get('/')
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_url(self):
        response = self.c.get(reverse('store:product_detail', args=['django-beginner']))
        self.assertEqual(response.status_code, 404)

    def test_view_function(self):
        request = self.factory.get('/item/django-beginners')
        response = all_products(request)
        html = response.content.decode('utf8')
        self.assertIn('<title>Home</title>', html)
        self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))
        self.assertEqual(response.status_code, 200)