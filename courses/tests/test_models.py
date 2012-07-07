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
        
    
        
class TestCoursePage(TestCase):
    
    def setUp(self):
        super(TestCoursePage, self).setUp()
        
    
    def tearDown(self):
        super(TestCoursePage, self).tearDown()
    
    
    def test_successfull_creation(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        course_page = CoursePage.objects.create(course=effective_java, title='Sample page', contents='Contents for sample page')                
        course_page_retrieved = CoursePage.objects.get(course=effective_java, title='Sample page')
        self.assertIsNotNone(course_page_retrieved)
        
    
    def test_unsuccessfull_creation_course_required(self):        
        try:
            course_page = CoursePage.objects.create(title='Sample page', contents='Contents for sample page')
            self.fail('Expected Exception when a coursePage is created without a course')
        except Exception, e:
            pass
        

class TestQuestion(TestCase):
    
    def setUp(self):
        super(TestQuestion, self).setUp()
        
    
    def tearDown(self):
        super(TestQuestion, self).tearDown()
        
    def test_successfull_creation(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user = User.objects.create(username='joe', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user, course=effective_java, title=title, contents=contents)
        
    def test_unsuccessfull_creation_course_required(self):        
        user = User.objects.create(username='joe', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        try:
            question = Question.objects.create(user=user, title=title, contents=contents)
            self.fail('Expected Exception when a Question is created without a course')
        except:
            pass
    
        
    def test_unsuccessfull_creation_user_required(self):        
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        title = 'Sample question'
        contents='This is a sample question for testing'
        try:
            question = Question.objects.create(course=effective_java, title=title, contents=contents)
            self.fail('Expected Exception when a Question is created without a user')
        except:
            pass
        
    
    def test_can_be_liked_by_user_who_asked_the_question(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user = User.objects.create(username='joe', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user, course=effective_java, title=title, contents=contents)
        self.assertFalse(question.can_be_liked(user))
    
    
    def test_can_be_liked_for_the_first_time_by_user_who_didnt_ask_the_question(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')
        user2 = User.objects.create(username='jill', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        self.assertTrue(question.can_be_liked(user2))
        
    def test_can_be_liked_for_the_second_time_by_user_who_didnt_ask_the_question(self):
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')
        user2 = User.objects.create(username='jill', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        QuestionLike.objects.create(user=user2, question=question)
        self.assertFalse(question.can_be_liked(user2))

    def test_likes(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Like the question a few times
        user2 = User.objects.create(username='jill', password='idontknow')
        user3 = User.objects.create(username='shipa', password='idontknow')
        user4 = User.objects.create(username='manoj', password='idontknow')
        QuestionLike.objects.create(user=user2, question=question)
        QuestionLike.objects.create(user=user3, question=question)
        QuestionLike.objects.create(user=user4, question=question)
        
        #Verify
        self.assertEqual(question.likes(), 3)
        
        
    def test_answer_count_when_there_are_no_answers(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Verify answer count
        self.assertEqual(question.answer_count(), 0)
        
        
    def test_answer_count_when_there_are_answers(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        answer1 = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        answer2 = Answer.objects.create(user=user1, question=question, contents='This is my answer 2')
        answer3 = Answer.objects.create(user=user1, question=question, contents='This is my answer 3')
        
        #Verify answer count
        self.assertEqual(question.answer_count(), 3)
        
        
    def test_visit_by_user_for_the_first_time_who_did_not_post_question(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Visit
        user2 = User.objects.create(username='jill', password='idontknow')
        question.visit(user2)
        question_visit = QuestionVisit.objects.all()
        self.assertIsNotNone(question_visit)
        self.assertEqual(question_visit.count(), 1)
        
        
    def test_subsequent_visit_by_user_who_did_not_post_question(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Visit
        user2 = User.objects.create(username='jill', password='idontknow')
        question.visit(user2)
        question_visit = QuestionVisit.objects.all()        
        self.assertEqual(question_visit.count(), 1)
        
        question.visit(user2)
        question_visit = QuestionVisit.objects.all()        
        self.assertEqual(question_visit.count(), 1)
        
        
    def test_visit_by_user_who_posted_the_question(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Visit        
        question.visit(user1)
        question_visit = QuestionVisit.objects.all()        
        self.assertEqual(question_visit.count(), 0)        
        
        

class TestAnswer(TestCase):
    
    def setUp(self):
        super(TestAnswer, self).setUp()
        
        
    def tearDown(self):
        super(TestAnswer, self).tearDown()
        
        
    def test_successfull_creation(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
    
    
    def test_unsuccessfull_creation_question_required(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'        
        
        #Add some answers
        try:
            Answer.objects.create(user=user1, contents='This is my answer 1')
            self.fail('Expected Exception when an Answer is created without a Question')
        except:
            pass
        
        
    def test_unsuccessfull_creation_user_required(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        try:
            Answer.objects.create(contents='This is my answer 1')
            self.fail('Expected Exception when an Answer is created without a User')
        except:
            pass
    
    
    def test_can_be_liked_by_user_who_has_answered(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Verify
        self.assertFalse(answer.can_be_liked(user1))
        
    
    def test_can_be_liked_by_user_who_has_not_answered(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        user2 = User.objects.create(username='jill', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Verify
        self.assertTrue(answer.can_be_liked(user2))
        
        
    def test_can_be_liked_again_by_user_who_has_not_answered(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        user2 = User.objects.create(username='jill', password='idontknow')
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        AnswerLike.objects.create(user=user2, answer=answer)
        #Verify
        self.assertFalse(answer.can_be_liked(user2))
        
    
    def test_likes(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')                
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Add some answers
        user2 = User.objects.create(username='jill', password='idontknow')
        user3 = User.objects.create(username='shilpi', password='idontknow')
        user4 = User.objects.create(username='anil', password='idontknow')
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        AnswerLike.objects.create(user=user2, answer=answer)
        AnswerLike.objects.create(user=user3, answer=answer)
        AnswerLike.objects.create(user=user4, answer=answer)
        
        #Verify
        self.assertEqual(answer.likes(), 3)
    
    
    
class TestQuestionVisit(TestCase):
    
    def setUp(self):
        super(TestQuestionVisit, self).setUp()
        
    
    def tearDown(self):
        super(TestQuestionVisit, self).tearDown()
        
    
    def test_successfull_creation(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')                
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Create visit
        user2 = User.objects.create(username='jill', password='idontknow')
        QuestionVisit.objects.create(user=user2, question=question)
        
    
    def test_unsuccessfull_creation_user_required(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')                
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Create visit        
        try:
            QuestionVisit.objects.create(question=question)
            self.fail('Expecting Exception when a QuestionVisit is created without a user')
        except:
            pass
        
    
    def test_unsuccessfull_creation_question_required(self):
        #Create Question 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')                
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        
        #Create visit
        user2 = User.objects.create(username='jill', password='idontknow')
        try:
            QuestionVisit.objects.create(user=user2)
            self.fail('Expecting Exception when a QuestionVisit is created without a question')
        except:
            pass
        
        
class TestActivity(TestCase):
    
    def setUp(self):
        super(TestActivity, self).setUp()
        
        
    def tearDown(self):
        super(TestActivity, self).tearDown()
        
        
    def test_successfull_creation(self):
        #Create 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        
        #Verify
        activity_retrieved = Activity.objects.get()
        self.assertIsNotNone(activity_retrieved)
        
        
    def test_unsuccessfull_creation_course_required(self):         
        try:
            Activity.objects.create(placement=1, title='Activity 1', contents='Contents for activity 1')
            self.fail('Expected Exception when an Activity is created without a course')
        except:
            pass

        
    def test_unsuccessfull_creation_title_required(self): 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        try:
            Activity.objects.create(course=effective_java, placement=1, contents='Contents for activity 1')
            self.fail('Expected Exception when an Activity is created without a title')
        except:
            pass
        
        
    def test_unsuccessfull_creation_contents_required(self): 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        try:
            Activity.objects.create(course=effective_java, placement=1, title='Activity 1')
            self.fail('Expected Exception when an Activity is created without a contents')
        except:
            pass


class TestActivityResponse(TestCase):
    
    def setUp(self):
        super(TestActivityResponse, self).setUp()
        
        
    def tearDown(self):
        super(TestActivityResponse, self).tearDown()
        
    
    def test_successfull_creation(self):
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        
        
    def test_unsuccessfull_creation_activity_required(self):
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')            
        try:
            ActivityResponse.objects.create(user=user1, contents='this is my response')
            self.fail('Expected Exception when an ActivityResponse is created without an activity')
        except:
            pass
        
    
    def test_unsuccessfull_creation_user_required(self):
        #Create                 
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        try:
            ActivityResponse.objects.create(activity=activity, contents='this is my response')
            self.fail('Expected Exception when an ActivityResponse is created without a user')
        except:
            pass
        
        
    def test_unsuccessfull_creation_contents_required(self):
        #Create                 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        try:
            ActivityResponse.objects.create(activity=activity, user=user1)
            self.fail('Expected Exception when an ActivityResponse is created without contents')
        except:
            pass
        
    
    def test_reviewed_by_user_who_has_indeed_reviewed(self):
        #Create activity response 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        
        #Create review
        user2 = User.objects.create(username='jill', password='idontknow')        
        ActivityResponseReview.objects.create(activity_response=activity_response, user=user2, contents='great work')
        
        #Verify
        self.assertTrue(activity_response.reviewed_by(user2))
        
        
    def test_reviewed_by_user_who_has_not_reviewed(self):
        #Create activity response 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        
        #Create review
        user2 = User.objects.create(username='jill', password='idontknow')        
        ActivityResponseReview.objects.create(activity_response=activity_response, user=user2, contents='great work')
        
        #Verify
        user3 = User.objects.create(username='uday', password='idontknow')
        self.assertFalse(activity_response.reviewed_by(user3))
        
        
    def test_visit_by_user_who_did_not_submit_response(self):
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        
        #Visit
        user2 = User.objects.create(username='jill', password='idontknow')
        activity_response.visited(user2)
        self.assertEqual(1, ActivityResponseVisit.objects.filter(activity_response=activity_response).count())
        
        
    def test_visit_by_user_who_submitted_the_response(self):
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        
        #Visit        
        activity_response.visited(user1)
        self.assertEqual(0, ActivityResponseVisit.objects.filter(activity_response=activity_response).count())
    
        
    
class TestActivityResponseReview(TestCase):
    
    def setUp(self):
        super(TestActivityResponseReview, self).setUp()
        
        
    def tearDown(self):
        super(TestActivityResponseReview, self).tearDown()
        
        
    def test_successfull_creation(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        ActivityResponseReview.objects.create(user=user1, activity_response=activity_response, contents='this is my response')
        
    
    def test_unsuccessfull_creation_activity_response_required(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        try:
            ActivityResponseReview.objects.create(user=user1, contents='this is my response')
            self.fail('Expecting Exception when an ActivityResponseReview is created when an ActivityResponseReview is created without an ActivityResponse')
        except:
            pass
            
    
    def test_unsuccessfull_creation_user_required(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        try:
            ActivityResponseReview.objects.create(activity_response=activity_response, contents='this is my response')
            self.fail('Expecting Exception when an ActivityResponseReview is created when an ActivityResponseReview is created without a User')
        except:
            pass
        

class TestActivityResponseVisit(TestCase):
    
    def setUp(self):
        super(TestActivityResponseVisit, self).setUp()
        
        
    def tearDown(self):
        super(TestActivityResponseVisit, self).tearDown()
        
        
    def test_successfull_creation(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        ActivityResponseVisit.objects.create(user=user1, activity_response=activity_response)
        
        
    def test_unsuccessfull_creation_activity_response_required(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        try:
            ActivityResponseVisit.objects.create(user=user1)
            self.fail('Expected Exception when ActivityResponseVisit is created without ActivityResponse')
        except:
            pass
        
        
    def test_unsuccessfull_creation_user_required(self):    
        #Create 
        user1 = User.objects.create(username='joe', password='idontknow')
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        activity = Activity.objects.create(course=effective_java, placement=1, title='Activity 1', contents='Contents for activity 1')
        activity_response = ActivityResponse.objects.create(user=user1, activity=activity, contents='this is my response')
        try:
            ActivityResponseVisit.objects.create(activity_response=activity_response)
            self.fail('Expected Exception when ActivityResponseVisit is created without user')
        except:
            pass
    
        
        
class TestCreditableAction(TestCase):
    
    def setUp(self):
        super(TestCreditableAction, self).setUp()
        
        
    def tearDown(self):
        super(TestCreditableAction, self).tearDown()
        
        
    def test_successfull_creation(self):
        CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        creditable_action_retrieved = CreditableAction.objects.get()
        self.assertIsNotNone(creditable_action_retrieved)
        
        
    def test_unsuccessfull_creation_title_required(self):
        try:
            CreditableAction.objects.create(description='Credits for great answer', creditss=10)
            self.fail('Expected Exception when creating CreditableAction without title')
        except:
            pass
        
        
    def test_unsuccessfull_creation_description_required(self):
        try:
            CreditableAction.objects.create(title='great answer', creditss=10)
            self.fail('Expected Exception when creating CreditableAction without description')
        except:
            pass
        
        
    def test_unsuccessfull_creation_creditss_required(self):
        try:
            CreditableAction.objects.create(description='Credits for great answer', title='great answer')
            self.fail('Expected Exception when creating CreditableAction without creditss')
        except:
            pass
                
                
class TestCredit(TestCase):
    
    def setUp(self):
        super(TestCredit, self).setUp()
        
        
    def tearDown(self):
        super(TestCredit, self).tearDown()
        
        
    def test_successfull_creation(self):
        #Create
        creditable_action = CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Create Credit
        Credit.objects.create(user=user1, action=creditable_action, mname=type(answer), mid=answer.id)
        
    def test_unsuccessfull_creation_user_required(self):
        #Create
        creditable_action = CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Create Credit
        try:
            Credit.objects.create(action=creditable_action, mname=type(answer), mid=answer.id)
            self.fail('Expected Exception when creating a Credit without a user')
        except:
            pass
        
        
    def test_unsuccessfull_creation_action_required(self):
        #Create
        #creditable_action = CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Create Credit
        try:
            Credit.objects.create(user=user1, mname=type(answer), mid=answer.id)
            self.fail('Expected Exception when creating a Credit without a CreditableAction')
        except:
            pass
        
        
    def test_unsuccessfull_creation_mname_required(self):
        #Create
        creditable_action = CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Create Credit
        try:
            Credit.objects.create(user=user1, action=creditable_action, mid=answer.id)
            self.fail('Expected Exception when creating a Credit without mname')
        except:
            pass
        
        
    def test_unsuccessfull_creation_mid_required(self):
        #Create
        creditable_action = CreditableAction.objects.create(title='great answer', description='Credits for great answer', creditss=10)
        effective_java = Course.objects.create(title='Effective Java', contents='Effective Java contents', status='O')
        user1 = User.objects.create(username='joe', password='idontknow')        
        title = 'Sample question'
        contents='This is a sample question for testing'
        question = Question.objects.create(user=user1, course=effective_java, title=title, contents=contents)
        answer = Answer.objects.create(user=user1, question=question, contents='This is my answer 1')
        
        #Create Credit
        try:
            Credit.objects.create(user=user1, action=creditable_action, mname=type(answer))
            self.fail('Expected Exception when creating a Credit without mid')
        except:
            pass