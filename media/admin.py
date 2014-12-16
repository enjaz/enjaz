from django.contrib import admin

from media.models import FollowUpReport, Story, StoryReview, StoryTask, Article, ArticleReview, Poll, PollChoice

admin.site.register(FollowUpReport)

admin.site.register(Story)
admin.site.register(StoryReview)
admin.site.register(StoryTask)

admin.site.register(Article)
admin.site.register(ArticleReview)


class PollChoiceAdmin(admin.TabularInline):
    model = PollChoice


class PollAdmin(admin.ModelAdmin):
    inlines = (PollChoiceAdmin, )

admin.site.register(Poll, PollAdmin)
