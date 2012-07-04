from courses.models import *
from django.test import TestCase
from django.contrib.auth.models import User

class TestCourseModel(TestCase):
    
    
    def setUp(self):
        super(TestCourseModel, self).setUp()
        
    
    def tearDown(self):
        super(TestCourseModel, self).tearDown()
        
    
    def test_model_creation(self):
        title = 'Effective Java'
        contents='Effective Java contents'
        status='O'
        effective_java = Course.objects.create(title=title, contents=contents, status=status)
        
        self.assertEqual(effective_java.users.count(), 0)
        self.assertEqual(effective_java.title, title, 'title does not match')
        self.assertEqual(effective_java.contents, contents, 'contents do not match')
        self.assertEqual(effective_java.status, status, 'status does not match')
        self.assertEqual(effective_java.start_date, None)
        self.assertEqual(effective_java.end_date, None)
        self.assertEqual(effective_java.completed_by.count(), 0)
        self.assertFalse(effective_java.send_forum_notification, 'incorrect value for send_forum_notification')
        self.assertEqual(effective_java.faciliators.count(), 0)
        self.assertEqual(effective_java.forum_faciliators.count(), 0)
        self.assertEqual(effective_java.activity_faciliators.count(), 0)
        self.assertFalse(effective_java.send_forum_notification, 'incorrect value for send_activity_notification')
        self.assertFalse(effective_java.send_activity_notification, 'incorrect value for send_activity_notification')
        self.assertEqual(effective_java.facilitator_notification_strategy, 0, 'incorrect notification strategy')
        self.assertFalse(effective_java.verify_enrollment, 'incorrect value for verify enrollment')
        
        
    
    def test_has_completed(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        effective_java.completed_by.add(user1)
        self.assertTrue(effective_java.has_completed(user1))
        
        user2 = User.objects.create(username='jill', password='idontknow')
        self.assertFalse(effective_java.has_completed(user2))
        

    
    def test_is_enrolled(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        effective_java.users.add(user1)
        self.assertTrue(effective_java.is_enrolled(user1))
        
        user2 = User.objects.create(username='jill1', password='idontknow')
        self.assertFalse(effective_java.is_enrolled(user2))
        
    
    def test_is_enrollment_pending(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1_course_app = CourseEnrollApplication.objects.create(user=user1, course=effective_java, status='P')
        self.assertTrue(effective_java.is_enrollment_pending(user1))
        
        user2 = User.objects.create(username='jill', password='idontknow')
        effective_java.is_enrollment_pending(user2)
        
        
        
