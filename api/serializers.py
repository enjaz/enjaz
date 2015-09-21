from rest_framework import serializers
from activities.models import Activity, Episode
from activities.models import Category as ActivityCategory
from clubs.models import Club
from media.models import Buzz, BuzzView
from niqati.models import Code, Category, Code_Collection, Code_Order

class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('pk', 'start_datetime', 'end_datetime')

class ClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = ('pk', 'name', 'english_name', 'email', 'coordinator', 'gender', 'city')

class ActivityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityCategory
        fields = ('pk', 'ar_name')

class ActivitySerializer(serializers.ModelSerializer):
    primary_club = ClubSerializer(read_only=True)
    category = ActivityCategorySerializer(read_only=True)
    secondary_clubs = ClubSerializer(many=True, read_only=True)
    episode_set = EpisodeSerializer(many=True, read_only=True)
    class Meta:
        model = Activity
        fields = ('pk', 'name', 'primary_club', 'secondary_clubs', 'public_description', 'episode_set', 'gender', 'category')

class BuzzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buzz
        fields = ('pk', 'title', 'body', 'image', 'is_push')

class BuzzViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuzzView
        fields = ('pk', 'viewer', 'buzz', 'off_date')

class NiqatiActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('name',)


class NiqatiEpisodeSerializer(serializers.ModelSerializer):
    activity = NiqatiActivitySerializer(read_only=True)
    class Meta:
        model = Episode
        fields = ('activity',)

class OrderSerializer(serializers.ModelSerializer):
    episode = NiqatiEpisodeSerializer(read_only=True)
    class Meta:
        model = Code_Order
        fields = ('episode',)

class NiqatiCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('ar_label',)

class CollectionSerializer(serializers.ModelSerializer):
    parent_order = OrderSerializer(read_only=True)
    code_category = NiqatiCategorySerializer(read_only=True)
    class Meta:
        model = Code_Collection
        fields = ('code_category', 'parent_order')

class CodeSerializer(serializers.ModelSerializer):
    collection = CollectionSerializer(read_only=True)
    class Meta:
        model = Code
        fields = ('pk', 'points', 'redeem_date', 'collection')
