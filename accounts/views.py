from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import lernado.accounts.models as models
import lernado.accounts.forms as forms
import mimetypes
import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404
from django.core.files.uploadedfile import SimpleUploadedFile

logger = logging.getLogger(__name__)
 
def view_profile(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = models.UserProfile.objects.get(user=user)
    ctx = {'user': user, 'user_profile': user_profile}
    return render_to_response('user_profile.html', RequestContext(request, ctx))

def edit_profile(request, user_id):
    if str(request.user.id) == user_id:
        user = User.objects.get(id=user_id)
        user_profile = models.UserProfile.objects.get(user=user)
        if request.method == 'GET':
            if user_profile.profile_picture:
                pic_file_path = settings.__getattr__('MEDIA_ROOT') + user_profile.profile_picture.url            
                pic_file = open(pic_file_path, 'rb')
                file_data = {'profile_picture': SimpleUploadedFile(user_profile.profile_picture.name, pic_file.read())}
            else:
                file_data = {'profile_picture': None}
                
            profile_form = forms.ProfileForm({'location': user_profile.location}, file_data)
            ctx = {'profile_form': profile_form, 'user_profile':user_profile}
            return render_to_response('edit_profile.html', RequestContext(request, ctx))
        elif request.method == 'POST':
            profile_form = forms.ProfileForm(request.POST, request.FILES)
            if profile_form.is_valid():            
                user_profile.location = request.POST['location']
                if 'profile_picture' in request.FILES:
                    user_profile.profile_picture = request.FILES['profile_picture']
                user_profile.save()
                return HttpResponseRedirect(reverse('lernado.accounts.views.view_profile', kwargs={'user_id':user.id}))
            else:
                return HttpResponseServerError('profile form is not valid %r ' % profile_form.errors)
        else:
            return HttpResponseServerError('This is neither a GET or POST request') 
    else:
        logger.error('Attempt to edit someone elses profile %r %r' % (request.user.id, user_id))
        raise Http404
    
def profile_pic(request, user_id):
    user = User.objects.get(id=user_id)
    user_profile = models.UserProfile.objects.get(user=user)
 
    if user_profile.profile_picture:
        fpath = settings.__getattr__('MEDIA_ROOT') + user_profile.profile_picture.url
    else:
        fpath = settings.DEFAULT_PERSON_IMAGE 

    content = open(fpath, "rb")
    # content can be a String or an iterable
    return HttpResponse(content, mimetype=mimetypes.guess_type(fpath))
    


    
