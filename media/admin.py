from django.contrib import admin

from media.models import FollowUpReport, Story, StoryReview, StoryTask

admin.site.register(FollowUpReport)
admin.site.register(Story)

admin.site.register(StoryReview)

admin.site.register(StoryTask)
