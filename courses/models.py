from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import datetime
import logging
import lernado.utils as lutils


logger = logging.getLogger(__name__)

# Create your models here.
class Course(models.Model):    
    
    STATUS_CHOICES = (
        ('O', 'Open'),
        ('S', 'Started'),
        ('C', 'Closed'),
    )
    users = models.ManyToManyField(User, null=True, blank=True)
    title = models.CharField(max_length=128)
    contents = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    completed_by = models.ManyToManyField(User, related_name='course_completed_by', blank=True)
    faciliators = models.ManyToManyField(User, related_name='faciliators', blank=True)
    forum_faciliators = models.ManyToManyField(User, related_name='forum_faciliators', blank=True)
    activity_faciliators = models.ManyToManyField(User, related_name='activity_faciliators', blank=True)
    send_forum_notification = models.BooleanField(default=False)
    send_activity_notification = models.BooleanField(default=False)
    facilitator_notification_strategy = models.IntegerField(default=0)
    verify_enrollment = models.BooleanField(default=False)
    
    def has_completed(self, user):        
        completed = Course.objects.filter(completed_by__id=user.id, id=self.id)
        return completed and True or False
        
    def is_enrolled(self, user):        
        enrolled_course = Course.objects.filter(users__id=user.id, id=self.id)        
        return enrolled_course and True or False

    def is_enrollment_pending(self, user):        
        pending_applications = CourseEnrollApplication.objects.filter(user=user, course=self, status='P')
        return pending_applications and True or False
        
    def __unicode__(self):
        #TODO: Change to reflect the time period 
        return self.title

class CourseEnrollApplication(models.Model):
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('A', 'Approved'),
        ('R', 'Rejected'),
    )
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    when = models.DateTimeField(default=datetime.datetime.now)
    comment = models.TextField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    changed_by = models.ForeignKey(User, null=True, related_name='changed_by')
    
    def __unicode__(self):
        return "%s : %s : %s" % (self.user.username, self.course.title, self.when.utcnow().strftime('%Y/%m/%d/ %H:%M'))
    
class CourseDropApplication(models.Model):
    user = models.ForeignKey(User)
    course = models.ForeignKey(Course)
    when = models.DateTimeField(default=datetime.datetime.now)
    comment = models.TextField()
    
class CoursePage(models.Model):
    title = models.CharField(max_length=128)
    contents = models.TextField()
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.title


class Question(models.Model):
    user = models.ForeignKey(User)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    when = models.DateTimeField(default=datetime.datetime.now)
    course = models.ForeignKey(Course)
    title = models.CharField(max_length=256)
    contents = models.TextField()
    
    def can_be_liked(self, user):
        question_already_liked = QuestionLike.objects.filter(user__id=user.id, question__id=self.id)
        return self.user != user and not question_already_liked
        
    def likes(self):
        return QuestionLike.objects.filter(question=self).count()
    
    def answer_count(self):
        return Answer.objects.filter(question=self).count()
        
    def visit(self, user):
        try:
            already_visited = QuestionVisit.objects.get(user=user, question=self)
        except ObjectDoesNotExist:
            visit = QuestionVisit(user=user, question=self)
            visit.save()
        
    def humanized_when(self):
        #TODO: This method may not be used
        h = lutils.humanizeTimeDiff(self.when)
        return h

    def __unicode__(self):
        return self.title

class QuestionLike(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    when = models.DateTimeField(default=datetime.datetime.now)
    
class Answer(models.Model):
    user = models.ForeignKey(User)
    when = models.DateTimeField(default=datetime.datetime.now)
    question = models.ForeignKey(Question)
    contents = models.TextField()

    def can_be_liked(self, user):
        answer_already_liked = AnswerLike.objects.filter(user__id=user.id, answer__id=self.id)
        return self.user != user and not answer_already_liked
    
    def likes(self):
        return AnswerLike.objects.filter(answer=self).count()
    
    def __unicode__(self):
        return self.question.title

class AnswerLike(models.Model):
    user = models.ForeignKey(User)
    answer = models.ForeignKey(Answer)
    when = models.DateTimeField(default=datetime.datetime.now)
    
class QuestionVisit(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    when = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return "question '%s' visited by %s at %r" % (self.question.title, self.user.username, self.when)
    
class Activity(models.Model):
    course = models.ForeignKey(Course)
    placement = models.IntegerField()
    title = models.CharField(max_length=128)
    contents = models.TextField()

    def __unicode__(self):
        return "%s - %s" % (self.course.title, self.title)

class ActivityResponse(models.Model):
    user = models.ForeignKey(User)
    activity = models.ForeignKey(Activity)
    when = models.DateTimeField(default=datetime.datetime.now)
    contents = models.TextField()

    def visited(self, user):
        try:
            already_visited = ActivityResponseVisit.objects.get(user=user, activity_response=self)
        except ObjectDoesNotExist:
            visit = ActivityResponseVisit(user=user, activity_response=self)
            visit.save()
    
    def reviewed_by(self, user):
        reviews_by_user = ActivityResponseReview.objects.filter(activity_response__id=self.id, user__id=user.id).count()
        if(reviews_by_user > 0):
            return True
        else:
            return False
        
    def reviews(self):
            return ActivityResponseReview.objects.filter(activity_response__id=self.id).count()
        
    def __unicode__(self):
        return "Response for '%s' by '%s' at '%r" % (self.activity.title, self.user.username, self.when)

class ActivityResponseReview(models.Model):
    user = models.ForeignKey(User)
    activity_response = models.ForeignKey(ActivityResponse)
    when = models.DateTimeField(default=datetime.datetime.now)
    contents = models.TextField()
    
    def __unicode__(self):
        return "Review for Response of activity '%s' submitted by '%s' reviewed by '%s' at '%r" % (self.activity_response.activity.title, self.activity.user.username, self.user.username, self.when)
    
class ActivityResponseVisit(models.Model):
    user = models.ForeignKey(User)
    activity_response = models.ForeignKey(ActivityResponse)
    when = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        return " %s 's response for activity '%s' visited by %s at %r" % (self.activity_response.user.username, self.activity_response.activity.title, self.user.username, self.when)

class CreditableAction(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField()
    creditss = models.IntegerField()
    
class Credit(models.Model):
    user = models.ForeignKey(User)
    action = models.ForeignKey(CreditableAction)
    when = models.DateTimeField(default=datetime.datetime.now)
    mname = models.CharField(max_length=256, blank=True)
    mid = models.BigIntegerField(default=0)
    
    