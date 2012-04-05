from django import template
import lernado.utils as lutils

register = template.Library()

def natural_time(value):
    return lutils.humanizeTimeDiff(value)

register.filter("natural_time", natural_time)

@register.simple_tag
def question_like(user, question):
    if not question.can_be_liked(user):
        return """
        <img src="/static/images/vote-arrow-up.png"
             alt="voteup image" height="24" width="24"
             border="0">
        """
    else:
        return """
        <a id="upvote-question-1"
           title="I like this question"
           class="post"
           href="/course/%s/question/%s/like/" rel="nofollow">
               <img src="/static/images/vote-arrow-up-on.png"
                    alt="voteup image" height="24" width="24"
                    border="0">
        </a>
        """ % (str(question.course.id), str(question.id))
        
@register.simple_tag
def answer_like(user, answer):
    if not answer.can_be_liked(user):
        return """
        <img src="/static/images/vote-arrow-up.png"
             alt="voteup image" height="24" width="24"
             border="0">
        """
    else:
        return """
        <a id="upvote-question-1"
           title="I like this question"
           class="post"
           href="/course/%s/question/%s/answer/%s/like/" rel="nofollow">
               <img src="/static/images/vote-arrow-up-on.png"
                    alt="voteup image" height="24" width="24"
                    border="0">
        </a>
        """ % (str(answer.question.course.id), str(answer.question.id), str(answer.id))

@register.simple_tag
def review_done_class(activity_response, user):
    if activity_response.reviewed_by(user):
        return "reviewed"
    else:
        return ""

@register.simple_tag
def enrollment_status(course, user, url):
    if url.find('enroll') != -1 or url.find('drop') != -1:
        return '' 
    #TODO: Use reverse instead of hardcoding
    html = '<a class="%s" href="/course/%s/%s">%s</a>'
    if course.is_enrolled(user):
        return html % ('course-drop', 'drop', str(course.id), 'Drop Course')
    elif course.is_enrollment_pending(user):
        return "Your application is pending approval"
    else:
        return html % ('course-enrollment', 'enroll', str(course.id), 'Enroll')
