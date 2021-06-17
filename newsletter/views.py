from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from .forms import SubscriberForm
from .models import Subscriber
from django.db import IntegrityError
import random
from datetime import datetime 

# Create your views here.
def random_digits():
	return "%0.12d" % random.randint(0, 999999999999)

def new(request):
	if request.method == 'POST':

		save = True

		if Subscriber.objects.filter(email = request.POST['email']).exists():

			sub = Subscriber.objects.get(email = request.POST['email'])
			save = False
		else:

			while True:
				num = random_digits()
				if Subscriber.objects.filter(conf_num = num).exists() is not True:
					break

			sub = Subscriber(email = request.POST['email'], conf_num = num)

		if save:
			sub.save()


		send_mail(subject        = 'Newsletter Confirmation',
				  message        = '',
				  from_email     = settings.EMAIL_HOST_USER,
				  recipient_list = [sub.email],
				  html_message   = 'Thank you for signing up for my email newsletter! \
		    					    Please complete the process by \
		    					    <a href="{}/confirm/?email={}&conf_num={}"> clicking here to \
		    					    confirm your registration</a>.'.format(request.build_absolute_uri('/newsletter'), sub.email, sub.conf_num),
		    	  fail_silently  = True)

		print (sub.email)
		
		return render(request, 'newsletter/index.html', {'email': sub.email, 'action': 'added', 'form': SubscriberForm()})
	else:
		return render(request, 'newsletter/index.html', {'form': SubscriberForm()})

def confirm(request):

	sub = Subscriber.objects.get(email=request.GET['email'])

	if sub.conf_num == request.GET['conf_num']:

		sub.confirmed    = True
		sub.confirmed_at = datetime.now()
		sub.save()
		return render(request, 'newsletter/index.html', {'email': sub.email, 'action': 'confirmed'})
	
	else:
		return render(request, 'newsletter/index.html', {'email': sub.email, 'action': 'denied'})

def delete(request):

	sub = Subscriber.objects.get(email=request.GET['email'])
	
	if sub.conf_num == request.GET['conf_num']:
		sub.delete()
		return render(request, 'newsletter/index.html', {'email': sub.email, 'action': 'unsubscribed'})
	else:
		return render(request, 'newsletter/index.html', {'email': sub.email, 'action': 'denied'})