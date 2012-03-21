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
        
