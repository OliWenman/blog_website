from django.contrib import admin
from .models import Subscriber, Newsletter

class AdminSubscriber(admin.ModelAdmin):
	readonly_fields = ['joined_at', 'confirmed_at']
	pass
admin.site.register(Subscriber, AdminSubscriber)

class AdminNewsletter(admin.ModelAdmin):

	def send_newsletter(modeladmin, request, queryset):
		for newsletter in queryset:
			newsletter.send(request)

	send_newsletter.short_description = "Send selected Newsletters to all subscribers"

	actions         = [send_newsletter]
	readonly_fields = ['updated_at', 'created_at', 'sent_already', 'sent_date']
	list_display    = ('subject', 'created_at', 'updated_at', 'sent_already')
	exclude         = ['sent_date']

admin.site.register(Newsletter, AdminNewsletter)