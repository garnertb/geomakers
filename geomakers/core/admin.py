from django.contrib import admin
from .models import Image, Link, MakerSpace, UserProfile, Project, Resource, Tag, Video

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Link)
admin.site.register(MakerSpace)
admin.site.register(UserProfile)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Resource)
admin.site.register(Tag)
admin.site.register(Video)
admin.site.register(Image)
