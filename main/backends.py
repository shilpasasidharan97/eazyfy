from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model, login
import random
import string
from .models import PhoneOTP
from django.core.exceptions import ValidationError
