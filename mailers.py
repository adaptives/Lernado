from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from smtplib import SMTPException
from lernado import settings

def question_asked(host, question):
    if not question.course.send_forum_notification:
        print "not required to send email for new question"
        return
    
    subject = "%s - A new question has been asked - '%s'" % (question.course.title, question.title)
    message = """
    %s
    """ % ("http://" + host + reverse('lernado.views.question', kwargs={'course_id':question.course.id, 'question_id':question.id}))
    from_email = settings.EMAIL_HOST_USER
    bcc = [settings.DEFAULT_BCC]
    to_users = question.course.forum_faciliators.all()
    fail_silently = False
    for to_user in to_users:
        print "sending email to user %r" % to_user.email
        #TODO: In the line below, we are hard-coding http... remove the hard coding  
        try:
            email_msg = EmailMessage(subject=subject, body=message, from_email=from_email, to=[to_user.email], bcc=bcc)
            email_msg.content_subtype = "html"  # Main content is now text/html
            email_msg.send(fail_silently=fail_silently)
            #send_mail(subject, message, from_email, to, fail_silently=fail_silently)
        except Exception:
            pass    
    
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
        

def activity_response(host, activity_response):
    subject = "%s - New response submitted for '%s'" % (activity_response.activity.course.title, activity_response.activity.title)
    from_email = settings.EMAIL_HOST_USER
    to = [settings.DEFAULT_BCC]
    fail_silently = False
    #TODO: In the line below, we are hard-coding http... remove the hard coding
    message = """ 
    %s
    """ % ("http://" + host + reverse('lernado.views.activity_response', kwargs={'course_id':activity_response.activity.course.id, 'activity_id':activity_response.activity.id, 'activity_response_id':activity_response.id}))
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
        ret_val += user.first_name
    if user.last_name:
        ret_val += " " + user.last_name
    if not ret_val:
        ret_val = user.username
    return ret_val

    