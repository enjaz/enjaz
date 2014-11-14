from django.contrib import admin

from media.models import FollowUpReport, Story, StoryReview, StoryTask, Article, ArticleReview, Poll

admin.site.register(FollowUpReport)

admin.site.register(Story)
admin.site.register(StoryReview)
admin.site.register(StoryTask)

admin.site.register(Article)
admin.site.register(ArticleReview)

admin.site.register(Poll)
