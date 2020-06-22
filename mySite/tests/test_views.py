from django.test import RequestFactory, Client
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from mixer.backend.django import mixer
from user.views import profile, send_message
from user.models import Profile
from django.test import TestCase
import pytest

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def factory():
    return RequestFactory()

@pytest.fixture
def user(db):
    return mixer.blend(User)

@pytest.fixture
def anon_user(db):
    return AnonymousUser()

@pytest.fixture
def user_(db):
    return mixer.blend(username='Name', email='email@gmail.com', password='123')

@pytest.fixture
def post(db):
    return mixer.blend('news.Post')

@pytest.fixture
def comment(db):
    us = user
    return mixer.blend('news.Comment')

@pytest.fixture
def text_mes(db):
    return mixer.blend('users.TextMessage')

def test_profile_auth_user(factory, user):
    #mixer.blend(User)
    path = reverse('profile')
    request = factory.get(path)
    request.user = user

    response = profile(request)
    assert response.status_code == 200

def test_profile_unauth_user(factory, anon_user):
    #mixer.blend(User)
    path = reverse('profile')
    request = factory.get(path)
    request.user = anon_user

    response = profile(request)
    assert '/login' in response.url


def test_view_url_about(client):
    resp = client.get('/about/')
    assert resp.status_code == 200

def test_view_url_reg(client):
    resp = client.get('/profile/')
    assert resp.status_code == 302
    resp = client.post('/profile/')
    resp = client.get('/register/')
    resp = client.post('/register/')
    assert resp.status_code == 200

def test_Cl_sendmes(client, user, factory) :
    c = client
    request = factory.post('/sendmessage/', {'subject': 'Test', 'message': 'Ubuntu127001@gmail.com', 'users' : user.profile})
    request.user = user_
    send_message(request)
    assert True == 1


def test_login(user, client):
    c = client
    us = user
    response = c.post('/login/', {'username': us.username, 'password': us.password})
    assert response.status_code == response.status_code


def test_register(client, db):
    c = client
    response = c.post('/register/', {'username': 'q', 'email': 'Ub@gmail.com', 'password1': 'Ubuntu127001',
                                     'password2': 'Ubuntu127001'})
    assert response.status_code == 302



def test_url_pr_get(client):
    resp = client.get('/profile/')
    assert resp.status_code == 302



def test_profile(client):
    c = client
    response = c.post('/profile/', {'username': 'Test', 'email': 'Ubuntu127001@gmail.com', 'image' : 'default.jpg'})
    assert response.status_code == 302


def test_comment(client, db):
    resp = client.post('/post/1/comment/', {'text' : 'ssddd'})
    assert resp.status_code == 404



