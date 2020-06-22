import pytest
from django.contrib.auth.models import User
from mixer.backend.django import mixer

from article.models import Article
from django.contrib.auth.models import User, AnonymousUser

from user.models import Profile
from news.models import News
from mixer.backend.django import mixer
import pytest

@pytest.fixture
def profile(request, db):
    return mixer.blend(Profile)

@pytest.fixture
def news(request, db):
    return mixer.blend(News)


@pytest.fixture
def user(db):
    return mixer.blend(User)

#@pytest.mark.django_db
def test_user_model(news):
    assert news.search == " "

#def test_profile_model(profile):
 #   assert profile.verified == False

def test_name_label(user):
    us = user
    field_label = us._meta.get_field('username').verbose_name
    assert field_label == 'имя пользователя'

def test_email_label(user):
    us = user
    field_label = us._meta.get_field('password').verbose_name
    assert field_label == 'пароль'
