from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from lernado.courses.models import Course
from lernado.courses.models import CoursePage
from lernado.courses.models import Question
from lernado.courses.models import QuestionLike
from lernado.courses.models import QuestionVisit
from lernado.courses.models import Answer 
from lernado.courses.models import AnswerLike
from lernado.courses.models import Activity
from lernado.courses.models import ActivityResponse
from lernado.courses.models import ActivityResponseVisit
from lernado.courses.models import ActivityResponseReview
import lernado.forms as forms
from django.template import RequestContext
from django.contrib.flatpages.views import flatpage
from django.contrib.flatpages.models import FlatPage
import datetime
import logging
import lernado.mailers as mailers

logger = logging.getLogger(__name__)

@login_required
def home(request):
    flat_pages = FlatPage.objects.filter(url='/home/')
    ctx = {}
    if flat_pages:
        ctx = {'content': flat_pages[0].content}
    return render_to_response('home.html', RequestContext(request, ctx))

@login_required
def courses(request):
    courses = Course.objects.all()
    ctx = {'courses':courses}
    return render_to_response('courses.html', RequestContext(request, ctx))

@login_required
def course(request, course_id):
    course = Course.objects.get(id=course_id)
    #logger.info("Is user %r enrolled in course %r - %r" % (request.user.username, course.title, course.is_enrolled(request.user)))
    questions = Question.objects.filter(course=course.id).order_by('-when')
    activities = Activity.objects.filter(course=course.id).order_by('placement')
    question_form = forms.QuestionForm()
    ctx = {'course': course, 'questions':questions, 'question_form': question_form, 'activities':activities, 'now':datetime.datetime.now}
    return render_to_response('course.html', RequestContext(request, ctx))

@login_required
def course_participants(request, course_id):
    course = Course.objects.get(id=course_id)
    ctx = {'course': course}
    return render_to_response('participants.html', RequestContext(request, ctx))

@login_required
def course_page(request, course_id, page_id):
    course = Course.objects.get(id=course_id)
    page = CoursePage.objects.get(id=page_id)
    # verify that this page belongs to this course
    return render_to_response('course_page.html', RequestContext(request, {'course': course, 'page':page}))

@login_required
def question(request, course_id, question_id):
    course = Course.objects.get(id=course_id)
    question = Question.objects.get(id=question_id)

    if request.method == 'GET':        
        answers = Answer.objects.filter(question=question.id)
        answer_form = forms.AnswerForm()
        question.visit(request.user)
    elif request.method == 'POST':
        answer_form = forms.AnswerForm(request.POST)
        if answer_form.is_valid():
            cd = answer_form.cleaned_data
            answer = Answer(user=request.user, question=question, contents=cd['contents'])
            answer.save()
            mailers.question_answered(request.get_host(), question)
            # Clear the answer form so we do not pre-populate it with the old answer
            answer_form = forms.AnswerForm()
        answers = Answer.objects.filter(question=question.id)
    else:
        raise Http404
    
    ctx = {'course': course, 'question': question, 'answers': answers, 'answer_form': answer_form}
    return render_to_response('question.html', RequestContext(request, ctx))

@login_required
def ask_question(request, course_id):
    course = Course.objects.get(id=course_id)
    
    if request.method == 'GET':
        question_form = forms.QuestionForm()
        ctx = {'course': course, 'question_form': question_form}
        return render_to_response('ask_question.html', RequestContext(request, ctx))
        
    elif request.method == 'POST':
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            cd = question_form.cleaned_data
            question = Question(title=cd['title'], contents=cd['contents'], user=request.user, course=course)
            question.save()
            mailers.question_asked(request.get_host(), question)
            return HttpResponseRedirect('/course/%d/' % course.id)
        else:
            ctx = {'course': course, 'question_form': question_form}
            return render_to_response('ask_question.html', RequestContext(request, ctx))
    else:
        raise Http404

@login_required
def edit_question(request, course_id, question_id):
    course = Course.objects.get(id=course_id)
    question = Question.objects.get(id=question_id)

    if request.method == 'GET':        
        question_form = forms.QuestionForm({'title': question.title, 'contents': question.contents})
        ctx = {'course': course, 'question_id': question.id, 'question_form': question_form}
        return render_to_response('edit_question.html', RequestContext(request, ctx))
    elif request.method == 'POST':
        question_form = forms.QuestionForm(request.POST)
        if question_form.is_valid():
            cd = question_form.cleaned_data
            question.title  = cd['title']
            question.contents = cd['contents']
            question.save()
            return HttpResponseRedirect('/course/%d/question/%d/' % (course.id, question.id))
        else:
            ctx = {'course': course, 'question_form': question_form}
            return render_to_response('edit_question.html', RequestContext(request, ctx))
    else:
        raise Http404
   

@login_required
def like_question(request, course_id, question_id):
    course = Course.objects.get(id=course_id)
    question = Question.objects.get(id=question_id)
    if not question.user == request.user:    
        try:
            alread_liked = QuestionLike.objects.get(user__id=request.user.id, question__id=question.id)
        except ObjectDoesNotExist:
            question_like = QuestionLike(user=request.user, question=question)
            question_like.save()
    
    return HttpResponseRedirect(reverse('lernado.views.question', kwargs={'course_id':course.id, 'question_id':question.id}))


@login_required
def like_answer(request, course_id, question_id, answer_id):
    print "attempting to like the answer"
    course = Course.objects.get(id=course_id)
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.get(id=answer_id)
    if not answer.user == request.user:
        print "Being liked by a valid user"   
        try:
            alread_liked = AnswerLike.objects.get(user__id=request.user.id, answer__id=question.id)
        except ObjectDoesNotExist:
            print "liking the answer"
            answer_like = AnswerLike(user=request.user, answer=answer)
            answer_like.save()
    
    return HttpResponseRedirect(reverse('lernado.views.question', kwargs={'course_id':course.id, 'question_id':question.id}))


@login_required
def activity(request, course_id, activity_id):
    course = Course.objects.get(id=course_id)
    activity = Activity.objects.get(id=activity_id)
    
    if request.method == 'GET':
        activity_responses = ActivityResponse.objects.filter(activity=activity).order_by('-when')
        activity_form = forms.ActivityForm()
        ctx = {'course': course, 'activity': activity, 'activity_responses': activity_responses, 'activity_form': activity_form}
        return render_to_response('activity.html', RequestContext(request, ctx))
    elif request.method == 'POST':
        activity_form = forms.ActivityForm(request.POST)
        if activity_form.is_valid():
            cd = activity_form.cleaned_data
            activity_response = ActivityResponse(user=request.user, activity=activity, contents=cd['contents'])
            activity_response.save()
            mailers.activity_response(request.get_host(), activity_response)
            return HttpResponseRedirect('/course/%d/activity/%d/' % (course.id, activity.id))
        else:
            ctx = {'course': course, 'activity': activity, 'activity_form': activity_form}
            return render_to_response('activity.html', RequestContext(ctx))
    else:
        raise Http404
    
@login_required
def activity_response(request, course_id, activity_id, activity_response_id):
    course = Course.objects.get(id=course_id)
    activity = Activity.objects.get(id=activity_id)
    activity_response = ActivityResponse.objects.get(id=activity_response_id)
    activity_response_reviews = ActivityResponseReview.objects.filter(activity_response=activity_response)
    
    if request.method == 'GET':
        if activity_response:
            activity_response.visited(request.user)
            visitors = ActivityResponseVisit.objects.filter(activity_response=activity_response)
        
            activity_response_review_form = forms.ActivityResponseReviewForm()
            ctx = {'course': course, 'activity': activity, 'activity_response': activity_response, 'activity_response_reviews': activity_response_reviews, 'visitors': visitors, 'activity_response_review_form': activity_response_review_form}
            return render_to_response('activity_response.html', RequestContext(request, ctx))
        else:
            raise Http404
        
    elif request.method == 'POST':
        activity_response_review_form = forms.ActivityResponseReviewForm(request.POST)
        if activity_response_review_form.is_valid():
            cd = activity_response_review_form.cleaned_data
            activity_response_review = ActivityResponseReview(user=request.user, activity_response=activity_response, contents=cd['contents'])
            activity_response_review.save()
            mailers.activity_response_reviewed(request.get_host(), activity_response)
            return HttpResponseRedirect('/course/%d/activity/%d/response/%d/' % (course.id, activity.id, activity_response.id))
        else:
            ctx = {'course': course, 'activity': activity, 'activity_response': activity_response, 'activity_response_review_form': activity_response_review_form}
            return render_to_response('activity_response.html', RequestContext(request, ctx))
    else:
        raise Http404

@login_required
def all_activity_submissions(request, course_id):
    course = Course.objects.get(id=course_id)
    #TODO: Can we send only the course object to the template ?
    #TODO: We should sort the activities by placement and responses by timestamp
    activities = Activity.objects.filter(course__id=course.id).order_by('placement')
    activity_and_responses = []
    for activity in activities:
        responses = ActivityResponse.objects.filter(activity__id=activity.id).order_by('-when')
        activity_and_responses.append({'activity': activity, 'responses': responses})
    ctx = {'course': course, 'activity_and_responses': activity_and_responses}
    return render_to_response('all_activity_submissions.html', RequestContext(request, ctx))

@login_required
def page(request, page):
    return flatpage(request, '/page/%s/' % page)

    
