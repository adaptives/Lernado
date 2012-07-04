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
        self.assertFalse(effective_java.is_enrollment_pending(user2))
        
        
        
class TestCourseEnrollApplication(TestCase):
    
    
    def setUp(self):
        super(TestCourseEnrollApplication, self).setUp()
        
    
    def tearDown(self):
        super(TestCourseEnrollApplication, self).tearDown()
        
    
    def test_successfull_instantiation(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        course_enroll_application = CourseEnrollApplication.objects.create(user=user1, course=effective_java, comment='no comments', status='P')
        self.assertEqual(CourseEnrollApplication.objects.count(), 1)            
        
    
    def test_instantiation_user_required(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        try:
            course_enroll_application = CourseEnrollApplication.objects.create(course=effective_java, comment='no comments', status='P')
            self.fail('Was expecting an Exception to be raised when we create a CourseEnrollApplication without any fields')
        except:
            pass
        
    
    def test_instantiation_course_required(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        try:
            course_enroll_application = CourseEnrollApplication.objects.create(user=user1, comment='no comments', status='P')
            self.fail('Was expecting an Exception to be raised when we create a CourseEnrollApplication without any fields')
        except:
            pass
        
    
    def test_instantiation_status_required(self):
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        try:
            course_enroll_application = CourseEnrollApplication.objects.create(course=effective_java, comment='no comments')
            self.fail('Was expecting an Exception to be raised when we create a CourseEnrollApplication without any fields')
        except:
            pass
    
    def test_approving_course_enroll_application(self):
        #create object
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        course_enroll_application = CourseEnrollApplication.objects.create(user=user1, course=effective_java, comment='no comments', status='P')
        #change status
        course_enroll_application_retreived = CourseEnrollApplication.objects.get(user=user1)
        self.assertIsNotNone(course_enroll_application_retreived)
        course_enroll_application_retreived.status = 'A'
        course_enroll_application_retreived.save()
        
        #retrieve and verify new status
        course_enroll_application_retreived_1 = CourseEnrollApplication.objects.get(user=user1, status='A')
        self.assertIsNotNone(course_enroll_application_retreived_1)
        
        
class TestCourseDropApplication(TestCase):
    
    
    def setUp(self):
        super(TestCourseDropApplication, self).setUp()
        
    
    def tearDown(self):
        super(TestCourseDropApplication, self).tearDown()
        
    
    def test_successfull_creation(self):
        #create
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        course_drop_application = CourseDropApplication.objects.create(user=user1, course=effective_java)
        #retrieve
        course_drop_application_retrieved = CourseDropApplication.objects.get(user=user1, course=effective_java)
        self.assertIsNotNone(course_drop_application)
    
    
    def test_creation_user_required(self):
        #create
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        try:
            course_drop_application = CourseDropApplication.objects.create(course=effective_java)
            self.fail('Expected Exception when adding a CourseDropApplication without a user')
        except:
            pass
        
    
    def test_creation_course_required(self):
        #create
        user1 = User.objects.create(username='joe', password='idontknow')        
        try:
            course_drop_application = CourseDropApplication.objects.create(user=user1)
            self.fail('Expected Exception when adding a CourseDropApplication without a user')
        except:
            pass
        
    
        