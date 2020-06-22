import pytest
from django.urls import reverse, resolve


def make_reverse(str):
    return reverse(str, kwargs={'pk': '1'})


@pytest.mark.parametrize("test_input, expected", [(make_reverse('confirm-page'), 'confirm-page'),(make_reverse('article-detail'), 'article-detail'),(make_reverse('comment-detail'), 'comment-detail')])
def test_detail_url(test_input, expected):
    assert resolve(test_input).view_name == expected

class TestUrls:


    def test_register_url(self):
        path = reverse('register')
        assert resolve(path).view_name == 'register'

    def test_profile_url(self):
        path = reverse('profile')
        assert resolve(path).view_name == 'profile'

    def test_login_url(self):
        path = reverse('login')
        assert resolve(path).view_name == 'login'

    def test_logout_url(self):
        path = reverse('logout')
        assert resolve(path).view_name == 'logout'

    def test_send_message_url(self):
        path = reverse('send_message-page')
        assert resolve(path).view_name == 'send_message-page'
