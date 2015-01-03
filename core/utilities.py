from constance import config
from django.contrib.auth.models import User

FVP_EMAIL = User.objects.get(username=config.FVP_USERNAME).email
MVP_EMAIL = User.objects.get(username=config.MVP_USERNAME).email
DHA_EMAIL = User.objects.get(username=config.DHA_USERNAME).email
