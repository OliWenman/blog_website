from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime    

class Subscriber(models.Model):

	email        = models.EmailField(unique          = True)
	conf_num     = models.CharField(max_length       = 15)
	confirmed    = models.BooleanField(default       = False)
	joined_at	 = models.DateTimeField(auto_now_add = True)
	confirmed_at = models.DateTimeField(null         = True)

	def __str__(self):
		return self.email + " (" + ("not " if not self.confirmed else "") + "confirmed)"


class Newsletter(models.Model):

	created_at   = models.DateTimeField(auto_now_add = True)
	updated_at   = models.DateTimeField(auto_now     = True)
	subject      = models.CharField(max_length       = 150)
	contents     = models.FileField(upload_to        = 'uploaded_newsletters/')
	sent_already = models.BooleanField(default       = False)
	sent_date    = models.DateTimeField(null         = True)

	def __str__(self):
		return self.subject + " " + self.created_at.strftime("%B %d, %Y")

	def send(self, request):
		
		if self.sent_already:
			messages.error(request, "You have already sent this newsletter out to your subscribers.")
			return request

		contents = self.contents.read().decode('utf-8')
		subscribers = Subscriber.objects.filter(confirmed=True)

		sub_list = []
		for sub in subscribers:
			sub_list.append(sub.email)


		for sub in subscribers:
			send_mail(from_email     = settings.EMAIL_HOST_USER,
					  recipient_list = [sub],
					  subject        = self.subject,
					  message        = '',
					  html_message   = contents + '<br><a href="{}/delete/?email={}&conf_num={}">Unsubscribe</a>.'.format(request.build_absolute_uri('/newsletter'), sub.email, sub.conf_num),
			    	  fail_silently  = False)

		self.sent_already = True
		self.sent_date    = datetime.now()
		self.save()

		messages.info(request, "Successfully sent to your subscribers.")
		return request

		