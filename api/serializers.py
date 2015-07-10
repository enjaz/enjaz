from rest_framework import serializers
from activities.models import Activity, Episode
from clubs.models import Club

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('start_datetime', 'end_datetime')

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
