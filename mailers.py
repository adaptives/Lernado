from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from smtplib import SMTPException
from lernado import settings

def question_answered(host, question):
    subject = "%s - Your question titled %s has a new answer" % (question.course.title, question.title)
    from_email = settings.EMAIL_HOST_USER
    to = [question.user.email, settings.DEFAULT_BCC]
    fail_silently = False
    #TODO: In the line below, we are hard-coding http... remove the hard coding
    message = """
    Dear %s,
    Your question '%s', has a new answer. 
    Please visit %s to view the answer.
    --
    Team Lernado
    """ % (name(question.user), question.title, "http://" + host + reverse('lernado.views.question', kwargs={'course_id':question.course.id, 'question_id':question.id}))
    try:
        send_mail(subject, message, from_email, to, fail_silently=fail_silently)
    except Exception:
        pass
        

def activity_response_reviewed(host, activity_response):
    subject = "%s - Your response for activity '%s' has a new review" % (activity_response.activity.course.title, activity_response.activity.title)
    from_email = settings.EMAIL_HOST_USER
    to = [activity_response.user.email, settings.DEFAULT_BCC]
    fail_silently = False
    #TODO: In the line below, we are hard-coding http... remove the hard coding
    message = """
    Dear %s,
    Your response for activity '%s', has a new review. 
    Please visit %s to see the review.
    --
    Team Lernado
    """ % (name(activity_response.user), activity_response.activity.title, "http://" + host + reverse('lernado.views.activity_response', kwargs={'course_id':activity_response.activity.course.id, 'activity_id':activity_response.activity.id, 'activity_response_id':activity_response.id}))
    try:
        send_mail(subject, message, from_email, to, fail_silently=fail_silently)
    except Exception:
        pass    


def name(user):
    ret_val = ""
    if user.first_name:
        ret_val =+ user.first_name
    if user.last_name:
        ret_val += "" + user.last_name
    if not ret_val:
        ret_val = user.username
    return ret_val

    