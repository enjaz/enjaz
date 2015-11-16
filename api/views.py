from datetime import datetime

from django.db.models import Sum
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.views import APIView
from activities.models import Activity

from accounts.utils import get_user_college
from api.serializers import ActivitySerializer, ClubSerializer, BuzzSerializer, BuzzViewSerializer, CodeSerializer
from clubs.models import Club
from media.models import Buzz, BuzzView
from niqati.models import Code

class ActivityList(generics.ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        queryset = Activity.objects.current_year().approved()

        # By default, we should display activities happening today
        # onwards.
        since_date_object = timezone.now().date()
        since_date = self.request.query_params.get('since_date', None)
        if since_date:
            try:
                since_date_object = datetime.strptime(since_date, "%Y-%m-%d").date()
            except ValueError: # If the date is malformatted.
                pass
        queryset = queryset.filter(episode__start_date__gte=since_date_object)
        
        # By default, we should display activities until the end of
        # time.
        until_date = self.request.query_params.get('until_date', None)
        if until_date:
            try:
                until_date_object = datetime.strptime(until_date, "%Y-%m-%d").date()
                queryset = queryset.filter(episode__start_date__lte=until_date_object)
            except ValueError: # If the date is malformatted.
                pass

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
        
        return queryset.distinct()

class ActivityDetail(generics.RetrieveAPIView):
    serializer_class = ActivitySerializer
    queryset = Activity.objects.approved().current_year()

class ClubList(generics.ListAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.current_year().visible()

class ClubDetail(generics.RetrieveAPIView):
    serializer_class = ClubSerializer
    queryset = Club.objects.current_year()


# Based on the class rest_framework/authtoken/views.py.
class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'ar_first_name': user.common_profile.ar_first_name,
                         'ar_middle_name': user.common_profile.ar_middle_name,
                         'ar_last_name': user.common_profile.ar_last_name,
                         'en_first_name': user.common_profile.en_first_name,
                         'en_middle_name': user.common_profile.en_middle_name,
                         'en_last_name': user.common_profile.en_last_name,
                         'city': user.common_profile.city,
                         'college': user.common_profile.college.name,
                         'gender': user.common_profile.college.name,
                         'section': user.common_profile.college.section})

class BuzzList(generics.ListAPIView):
    serializer_class = BuzzSerializer
    def get_queryset(self):
        queryset = Buzz.objects.published()
        user_college = get_user_college(self.request.user)
        if user_college:
            queryset = queryset.filter(colleges=user_college)
        return queryset

class BuzzViewCreate(generics.CreateAPIView):
    serializer_class = BuzzViewSerializer
    queryset = BuzzView.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        buzz_pk = self.kwargs.get('buzz_pk', None)
        buzz = get_object_or_404(Buzz, pk=buzz_pk)
        serializer.save(viewer=self.request.user, buzz=buzz)

class BuzzViewUpdate(generics.UpdateAPIView):
    serializer_class = BuzzViewSerializer
    queryset = BuzzView.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_update(self, serializer):
        serializer.save(off_date=timezone.now())

class CodeList(generics.ListAPIView):
    serializer_class = CodeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Code.objects.current_year().filter(user=self.request.user).order_by('-redeem_date')

class CodeSum(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        return Response(request.user.code_set.current_year().aggregate(niqati_sum=Sum('points')))

