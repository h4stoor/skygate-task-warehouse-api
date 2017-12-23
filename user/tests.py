from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import User as UserModel


class UserModelTestCase(TestCase):
    def setUp(self):
        self.User = get_user_model()
        
    def test_get_user_model(self):
        self.assertIs(self.User, UserModel)
    
    def test_user_model(self):
        user = self.User.objects.create_user(
            username='test',
            password='test'
        )
        self.assertEqual(user.username, 'test')
        
        users = self.User.objects.all()
        
        self.assertEqual(users.count(), 1)
