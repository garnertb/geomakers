from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from skyshaker.models import Image, Link, Project, Tag, Video, UserProfile
from skyshaker.forms import UserForm, UserProfileForm, ContributeForm, ImageForm
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
import json

def index(request):
    return render(request, 'skyshaker/index.html')

def donate(request):
    return render(request, 'skyshaker/donate.html')

def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'skyshaker/project.html', {'project': project})

def profile(request, slug):
    user = get_object_or_404(User, username=slug)
    userProfile = get_object_or_404(UserProfile, user=user)
    return render(request, 'skyshaker/profile.html', {'user': user, 'userProfile': userProfile})

def search(request):
    projects = Project.objects.all()
    json = serializers.serialize('json', projects)
    return render(request, 'skyshaker/search.html', {'projects': projects, 'json': json})

def contribute(request):
    print 'starting view: contribute'
    context = RequestContext(request)

    if request.method == 'POST':
        print "request.method == 'POST'"
        dataDict = dict(request.POST.iterlists())
        print "dataDict is", dataDict
        typeOfProject = str(unicode(dataDict[unicode('typeOfProject')][0]))
        title = str(unicode(dataDict[unicode('title')][0]))
        abstract = str(unicode(dataDict[unicode('abstract')][0]))
        videos = [video.strip() for video in str(unicode(dataDict[unicode('videos')][0])).split(",")]
        print "videos are", videos
        for url in videos:
            if 'youtube' in url:
                idOfYoutubeVideo = re.search('(?<=v=)\w+', url).group(0)
                videoData = yt_service.GetYouTubeVideoEntry(video_id=idOfYoutubeVideo)
#                title = videoData...
            elif 'vimeo' in instance.url:
                idOfVimeoVideo = re.search('(?<=com/)\w+', url).group(0)
#                title = some vimeo API
        Video.objects.create(title=title, url=url, embed="")

        links = [link.strip() for link in str(unicode(dataDict[unicode('links')][0])).split(",")]
        for url in links:
            Video.objects.create(title="", url=url)

#        Project.objects.create(title=title, abstract=abstract, rating=3)

        print "created objects"
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    elif request.method =='GET':
        print "request.method == 'GET'"
        contribute_form = ContributeForm()
        image_form = ImageForm()

    print 'finishing view: contribute'
    return render(request, 'skyshaker/contribute.html', {'contribute_form': contribute_form, 'image_form': image_form})

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'skyshaker/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/skyshaker/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your GeoMakers account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('skyshaker/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
