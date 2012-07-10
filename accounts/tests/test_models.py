from accounts.models import *
from django.test import TestCase
from django.contrib.auth.models import User

class TestUserProfile(TestCase):
    
    def setUp(self):
        super(TestUserProfile, self).setUp()
        
      
    def tearDown(self):
        super(TestUserProfile, self).tearDown()
        
    
    def test_successfull_creation(self):
        #Create
        user = User.objects.create(username='joe', password='idontknow')        
        
        #Retrieve
        user_profiles = UserProfile.objects.filter(user=user)
        self.assertEqual(len(user_profiles), 1)
        
        
        
        