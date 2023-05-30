from django.contrib import admin

from messaging.models import MessageModel as Messages, ThreadModel as Thread

admin.site.register(Messages)
admin.site.register(Thread)