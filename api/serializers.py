from rest_framework import serializers
from activities.models import Activity, Episode
from clubs.models import Club
from media.models import Buzz, BuzzView

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('pk', 'start_datetime', 'end_datetime')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('pk', 'name', 'english_name', 'email', 'coordinator', 'gender', 'city')

class ActivitySerializer(serializers.ModelSerializer):
    primary_club = ClubSerializer(read_only=True)
    secondary_clubs = ClubSerializer(many=True, read_only=True)
    episode_set = EpisodeSerializer(many=True, read_only=True)
    class Meta:
        model = Activity
        fields = ('pk', 'name', 'primary_club', 'secondary_clubs', 'public_description', 'episode_set', 'gender')

class BuzzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buzz
        fields = ('pk', 'title', 'body', 'image')

class BuzzViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuzzView
        fields = ('pk', 'viewer', 'buzz', 'off_date')
