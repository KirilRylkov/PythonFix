from datetime import datetime
from multiprocessing.dummy import Pool
from multiprocessing.dummy import Process, Manager, Queue
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, SendEmailForm
from django.core.mail import send_mail
from mySite.settings import EMAIL_HOST

import logging

messages = Queue()
logger = logging.getLogger()

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Ваш акаунт юыд создан')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/registerPage.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Вашь аккаунт обновлён')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'user/profile.html', context)



def confirm(request, uidb64):
    uid = force_text(urlsafe_base64_decode(uidb64))

    user = User.objects.get(email=uid)
    if not user.profile.verified:
        user.profile.verified = True
        user.save()
        messages.success(request, f'Пользователь подтверждён')
        logger.warning("Пользователь подтверждён")
    return redirect('article-home')

def send_verification(user, data):
    token = urlsafe_base64_encode(force_bytes(user.user.email))
    msg = render_to_string('user/emailPage.html', {'name': user.user.username, 'id': token, 'msg': data[1]})
    msg = data[1] + '\n' + msg + '\n' + str(data[2])
    send_mail(data[0], msg, settings.EMAIL_HOST_USER, [user, user.user.email])


def read_query(request, data):
    while not messages.empty():
        user = messages.get()
        p = Process(target=send_verification, args=(user,data))
        p.start()
        p.join()


def send_message(request):
    form = SendEmailForm(request.POST)
    if form.is_valid():
        subject = form.cleaned_data.get('subject')
        text = form.cleaned_data.get('message')
        date = datetime.now()
        users = form.cleaned_data['users']
        data = (subject, text, date)
        #messages.success(request, f'Сообщение отправлено!')
        for item in users:
            messages.put(item)
            user = item.user
        p = Process(target=read_query, args=(request, data))
        p.start()
        p.join()

        return redirect('/admin/user/profile/')
