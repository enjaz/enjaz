from datetime import datetime
from rest_framework import generics
from rest_framework.response import Response
from activities.models import Activity
from clubs.models import Club
from api.serializers import ActivitySerializer, ClubSerializer

class ActivityList(generics.ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.current_year().approved()

        # By default, we should display activities since the beginning
        # of time.
        since_date = self.request.query_params.get('since_date', None)
        if since_date:
            try:
                since_date_object = datetime.strptime(since_date, "%Y-%m-%d").date()
                queryset = queryset.filter(episode__start_date__gte=since_date_object)
            except ValueError: # If the date is malformatted.
                pass

        # By default, we should display activities until today.
        until_date_object = datetime.today().date()
        until_date = self.request.query_params.get('until_date', None)
        if until_date:
            try:
                until_date_object = datetime.strptime(until_date, "%Y-%m-%d").date()
            except ValueError: # If the date is malformatted.
                pass
        queryset = queryset.filter(episode__start_date__lte=until_date_object)

        # By default, we should display activities in the user's city.
        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(primary_club__city=city)
        else:
            queryset = queryset.for_user_city(self.request.user)

        # By default, we should display activities for the user's
        # gender.
        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
        else:
            queryset = queryset.for_user_gender(self.request.user)
        
        return queryset

class ActivityDetail(generics.RetrieveAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.approved().current_year()

class ClubList(generics.ListAPIView):
    serializer_class = ClubSerializer

    def get_queryset(self):
        queryset = Club.objects.current_year().visible()

        city = self.request.query_params.get('city', None)
        if city:
            queryset = queryset.filter(city=city)
        else:
            queryset = queryset.for_user_city(self.request.user)

        gender = self.request.query_params.get('gender', None)
        if gender:
            queryset = queryset.filter(gender=gender)
        else:
            queryset = queryset.for_user_gender(self.request.user)
        
        return queryset

class ClubDetail(generics.RetrieveAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.current_year()
