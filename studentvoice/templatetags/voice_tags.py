from django import template

register = template.Library()

@register.simple_tag
def has_voted(user, voice, vote_type, css_class='on'):
    "Mark previously voted voices as such."
    user_votes = user.vote_set.all()
    for voice_vote in voice.vote_set.filter(vote_type=vote_type):
        if voice_vote in user_votes:
            return css_class
