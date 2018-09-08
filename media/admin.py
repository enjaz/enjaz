from django.contrib import admin

from media.models import FollowUpReport, Story, StoryReview, StoryTask, Article, ArticleReview, Poll, PollChoice, Post, SnapchatReservation

admin.site.register(FollowUpReport)

admin.site.register(Story)
admin.site.register(StoryReview)
admin.site.register(StoryTask)

admin.site.register(Article)
admin.site.register(ArticleReview)

admin.site.register(SnapchatReservation)

class PollChoiceAdmin(admin.TabularInline):
    model = PollChoice


class PollAdmin(admin.ModelAdmin):
    inlines = (PollChoiceAdmin, )

class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['submitter']
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.submitter = request.user
        super(PostAdmin, self).save_model(request, obj, form, change)

admin.site.register(Poll, PollAdmin)
admin.site.register(Post, PostAdmin)
