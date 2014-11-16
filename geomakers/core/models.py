from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from django.template.defaultfilters import slugify
import os, re




class Image(models.Model):
    image = models.ImageField(upload_to="images", null=True, blank=True)
    caption = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return os.path.split(self.image.name)[1]

class Link(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class MakerSpace(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    state = models.CharField(max_length=200, null=True, blank=True)
    lat = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    lon = models.DecimalField(max_digits=8, decimal_places=5, null=True, blank=True)
    url = models.URLField(default="", null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

class Project(models.Model):
    owner = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    abstract = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    links = models.ManyToManyField('Link', blank=True)
    videos = models.ManyToManyField('Video', blank=True)
    images = models.ManyToManyField('Image', blank=True)
    rating = models.IntegerField(default='3',null=True, blank=True)
    ratingAsString = models.TextField(null=True, blank=True)
    typeOfProject = models.CharField(max_length=200,null=True, blank=True, choices=(("GeoDream","GeoDream"),("GeoRecipe","GeoRecipe"),("GeoBoost","GeoBoost")))
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, editable=True)
    related = models.ManyToManyField('self', blank=True)
    def __str__(self):
        if self.owner is None:
            return self.title
        elif self.owner.username != "":
            return self.title + " by " + self.owner.username



class Tag(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)

class UserProfile(models.Model):
    # This line is required.  Links UserProfile to a User model instance.
    user = models.OneToOneField(User, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    linkedin = models.CharField(max_length=200, null=True, blank=True)
    picture = models.ImageField(upload_to="images", null=True, blank=True, default=settings.STATIC_URL+"geomakers/img/user/default.jpg")
    def __str__(self):
        return self.user.username

class Video(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    embed = models.TextField(default="",null=True,blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

class Resource(models.Model):
    typeOfResource = models.CharField(max_length=200,null=True, blank=True, choices=(("Mapping_and_Software","Mapping and Software"),("Hardware_and_Software","Hardware and Software"),("Maker_Resources","Maker Resources"), ("Licensing_Resources", "Licensing Resources")))
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['title']

# the bios that apear on the geomakers.org/team page
class TeamMember(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to="images", null=True, blank=True, default=settings.STATIC_URL+"geomakers/img/user/default.jpg")
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['name']

def updateVideoEmbed(sender, instance, **kwargs):
    instance_url = str(instance.url)
    if 'youtube' in instance_url:
        idOfYoutubeVideo = re.search('(?<=v=)\w+', instance_url).group(0)
        instance.embed = '<iframe width="100%" height="315" src="//www.youtube.com/embed/' + idOfYoutubeVideo + '" frameborder="0" allowfullscreen></iframe>'
    elif 'vimeo' in instance.url:
        idOfVimeoVideo = re.search('(?<=com/)\w+', instance_url).group(0)
        instance.embed = '<iframe src="//player.vimeo.com/video/' + idOfVimeoVideo + '" width="500" height="281" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'
    post_save.disconnect(updateVideoEmbed, sender=Video)
    instance.save()
    post_save.connect(updateVideoEmbed, sender=Video)

# creates a user profile if a new user exists without one
def createProfile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

def updateProject(sender, instance, **kwargs):
    # add slug if doesn't exist    
    if instance.slug == "":
        print "slug is '', so we're going to add a new one"
        instance.slug = slugify(instance.title)

    # update rating
    ratingAsString = ""
    for i in range(0,instance.rating):
        ratingAsString += "<span class='star starFilled'>&#9733;</span>"
    for i in range(0,5-instance.rating):
        ratingAsString += "<span class='star starUnfilled'>&#9734;</span>"
    instance.ratingAsString = ratingAsString

    post_save.disconnect(updateProject, sender=Project)
    instance.save()
    post_save.connect(updateProject, sender=Project)

def updateImage(sender, instance, **kwargs):
    # add caption if doesn't exist
    if instance.caption == "":
        print "caption is '', so we're going to add a new one"
        instance.caption = os.path.split(instance.image.url)[1].split('.')[0].split('_')[0]
    post_save.disconnect(updateImage, sender=Image)
    instance.save()
    post_save.connect(updateImage, sender=Image)

# register the signal
post_save.connect(updateVideoEmbed, sender=Video)
post_save.connect(updateProject, sender=Project)
post_save.connect(updateImage, sender=Image)
post_save.connect(createProfile, sender=User)
