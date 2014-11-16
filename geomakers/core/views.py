from .models import Image, Link, MakerSpace, Project, Resource, Tag, TeamMember, Video, UserProfile, createProfile
from .forms import UserForm, UserProfileForm, ContributeForm, ImageForm

from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
import json, re, requests
from bs4 import BeautifulSoup
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save


def community(request):
    return render(request, 'core/community-guidelines.html')


@login_required
def contribute(request):
    print 'starting view: contribute'
    context = RequestContext(request)

    if request.method == 'POST':
        print "request.method == 'POST'"
        dataDict = dict(request.POST.iterlists())
        print "dataDict is", dataDict
        typeOfProject = str(unicode(dataDict[unicode('typeOfProject')][0]))
        abstract = str(unicode(dataDict[unicode('abstract')][0]))
        titleOfProject = str(unicode(dataDict[unicode('title')][0]))
        slug = slugify(titleOfProject)
        location = str(unicode(dataDict[unicode('location')][0]))
        project = Project.objects.create(owner_id=request.user.id, title=titleOfProject, slug=slug, abstract=abstract, location=location, rating=3, typeOfProject=typeOfProject)


        # add videos
        videos = []
        for video in str(unicode(dataDict[unicode('videos')][0])).split(","):
            videoStripped = video.strip()
            if videoStripped != "":
                videos.append(videoStripped)
        print "videos are", videos
        print "len(videos) is ", len(videos)
        for url in videos:
            titleOfVideo = ""
            if 'youtube' in url:
                idOfYoutubeVideo = re.search('(?<=v=)\w+', url).group(0)
                #videoData = yt_service.GetYouTubeVideoEntry(video_id=idOfYoutubeVideo)
                titleOfVideo = ""
            elif 'vimeo' in url:
                idOfVimeoVideo = re.search('(?<=com/)\w+', url).group(0)
                titleOfVideo = ""
            project.videos.create(title=titleOfVideo, url=url, embed="")

        # add links
        links = []
        for link in str(unicode(dataDict[unicode('links')][0])).split(","):
            linkStripped = link.strip()
            if linkStripped != "":
                links.append(linkStripped)
        print "links is ", links
        print "len(links) is ", len(links)
        for url in links:
            print "url is ", url
            titleOfLink = BeautifulSoup(requests.get(url).content).title.string
            project.links.create(title=titleOfLink, url=url)

        # add pictures
        if 'image' in request.FILES:
            project.images.create(image=request.FILES['image'], caption=request.FILES['image'].name[:-4])

        print "created objects"
#        returnrequest.META.get('HTTP_REFERER') HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return HttpResponseRedirect("/projects/"+slug)

    elif request.method =='GET':
        print "request.method == 'GET'"
        projects = Project.objects.all()
        contribute_form = ContributeForm()
        image_form = ImageForm()

    print 'finishing view: contribute'
    return render(request, 'core/contribute.html', {'projects': projects})

def donate(request):
    return render(request, 'core/donate.html')

def geoboosts(request):
    geoboosts = Project.objects.filter(typeOfProject="GeoBoost")
    return render(request, 'core/geoboosts.html', {'geoboosts': geoboosts})

def geodreams(request):
    geodreams = Project.objects.filter(typeOfProject="GeoDream")
    return render(request, 'core/geodreams.html', {'geodreams': geodreams})

def georecipes(request):
    georecipes = Project.objects.filter(typeOfProject="GeoRecipe")
    return render(request, 'core/georecipes.html', {'georecipes': georecipes})


def index(request):
    return render(request, 'core/index.html')

def makerspaces(request):
    states_makerspaces = []
    for state in MakerSpace.objects.order_by("state").values_list('state', flat=True).distinct():
        if state != "":
            states_makerspaces.append([str(unicode(state)).encode('utf-8'),MakerSpace.objects.filter(state=state)])

    return render(request, 'core/makerspaces.html', {'lsm': states_makerspaces})

def profile(request, slug):
    user = get_object_or_404(User, username=slug)
    userProfile = UserProfile.objects.get(user=user)
    if userProfile is None:
        if user.username == slug:
            userProfile = UserProfile.objects.create(user=user)
    return render(request, 'core/profile.html', {'user': user, 'userProfile': userProfile})

def profileEdit(request, slug):
    user = get_object_or_404(User, username=slug)
    userProfile = UserProfile.objects.get(user=user)
    return render(request, 'core/profile.html', {'user': user, 'userProfile': userProfile})

def project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'core/project.html', {'project': project})

def projectEdit(request, slug):
    print 'starting projectEdit with slug ' + slug 
    context = RequestContext(request)
    project = get_object_or_404(Project, slug=slug)
    print "project is ", project

    if request.user.id == project.owner.id:
        if request.method == 'POST':
            print "request.method == 'POST'"
            dataDict = dict(request.POST.iterlists())
            print "dataDict is", dataDict
            project.owner = User.objects.get(pk=str(unicode(dataDict[unicode('owner')][0])))
            project.typeOfProject = str(unicode(dataDict[unicode('typeOfProject')][0]))
            project.title = str(unicode(dataDict[unicode('title')][0]))
            project.slug = str(unicode(dataDict[unicode('slug')][0]))
            project.abstract = str(unicode(dataDict[unicode('abstract')][0]))
            project.location = str(unicode(dataDict[unicode('location')][0]))
            project.save()
        
            # add videos
            titlesOfVideos = [str(unicode(v)) for v in dataDict[unicode('video_title')]]
            print "titlesOfVideos are", titlesOfVideos
            print "len(titlesOfVideos) is ", len(titlesOfVideos)

            urlsOfVideos = [str(unicode(v)) for v in dataDict[unicode('video_url')]]
            print "urlsOfVideos are", urlsOfVideos
            print "len(urlsOfVideos) is ", len(urlsOfVideos)

            numberOfNewVideos = max(len(titlesOfVideos), len(urlsOfVideos))

            # delete all current videos
            project.videos.all().delete()

            # add in videos got from page
            for i in range(0,numberOfNewVideos):
                project.videos.create(title=titlesOfVideos[i], url=urlsOfVideos[i], embed="")

            # add links
            titlesOfLinks = [str(unicode(l)) for l in dataDict[unicode('link_title')]]
            print "titlesOfLinks are", titlesOfLinks
            print "len(titlesOfLinks) is ", len(titlesOfLinks)

            urlsOfLinks = [str(unicode(l)) for l in dataDict[unicode('link_url')]]
            print "urlsOfLinks are", urlsOfLinks
            print "len(urlsOfLinks) is ", len(urlsOfLinks)

            numberOfNewLinks = max(len(titlesOfLinks), len(urlsOfLinks))

            # delete all current videos
            project.links.all().delete()

            # add in videos got from page
            for i in range(0,numberOfNewLinks):
                project.links.create(title=titlesOfLinks[i], url=urlsOfLinks[i])


            # do pictures
            captions = [str(unicode(l)) for l in dataDict[unicode('image_caption')]]
            print "captions is ", captions
            numberOfCaptions = len(captions)
            numberOfNewImageObjects = numberOfCaptions
            print "numberOfNewImageObjects is", numberOfNewImageObjects

            requestFILES = request.FILES
            print "requestFILES is", requestFILES
            projectImages = project.images.all()
            numberOfOldImageObjects = len(projectImages)


            # udpate or create images
            for i in range(0, numberOfNewImageObjects):
                print "for i ", i

                # we got a new image!
                if i > numberOfOldImageObjects-1:
                    print "i > numberOfOldImageObjects, which is", i,">", numberOfOldImageObjects
                    project.images.create(image=requestFILES["imageInput_"+str(i)], caption=captions[i])
                else:
                    print "i <= numberOfOldImageObjects, which is", i,"<=", numberOfOldImageObjects
                    # check if uploaded a new image
                    if "imageInput_"+str(i) in requestFILES:
                        print "uploaded a new image for image ", i
                        projectImages[i].image = requestFILES["imageInput_"+str(i)]
                    projectImages[i].caption = captions[i]
                    projectImages[i].save()

            print "edited objects"
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        elif request.method =='GET':
            print "request.method == 'GET'"
            projects = Project.objects.all()
            users = User.objects.all()    
            print 'finishing view: projectEdit'
            return render(request, 'core/edit-project.html', {'project': project, 'projects': projects, 'users': users})

    elif request.user.id != project.owner.id:
        project = get_object_or_404(Project, slug=slug)
        return HttpResponseRedirect("/projects/"+slug)

def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        post_save.disconnect(createProfile, sender=User)

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

            # Now auto-login after registering
            new_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, new_user)

            post_save.connect(createProfile, sender=User)

            # Now, redirect to main page
            return HttpResponseRedirect("/")

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            post_save.connect(createProfile, sender=User)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'core/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def resources(request):
    resources = Resource.objects.all()
    return render(request, 'core/resources.html', {'resources': resources})

def search(request):
    projects = Project.objects.all()
    json = serializers.serialize('json', projects)
    return render(request, 'core/search.html', {'projects': projects, 'json': json})

def team(request):
    teamMembers = TeamMember.objects.all()
    return render(request, 'core/team.html', {'teamMembers': teamMembers})

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
                return HttpResponseRedirect('/core/')
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
        return render_to_response('core/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
