from django.contrib import admin
from django.shortcuts import render

from .forms import SendEmailForm
from .models import Profile


class MessageAdmin(admin.ModelAdmin):
    ordering = ['user']
    actions = ['send_message']

    def send_message(self, request, queryset):
        return render(request, 'user/send_message.html', {'form': SendEmailForm(initial={'users': queryset})})

    send_message.short_description = "Отправить собщение выбранным профилям"
    send_message.allow_tags = True


admin.site.register(Profile, MessageAdmin)
