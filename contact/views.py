from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.shortcuts import render
from .forms import ContactForm

# Create your views here.
def contact(request):

	contactform = ContactForm()
	context = {}

	if request.method == 'POST':

		contactform = ContactForm(request.POST)

		if contactform.is_valid():

			email   = request.POST['email']
			subject = request.POST['subject']
			name    = request.POST['name']
			message = request.POST['message']

			#Alert me of message
			
			send_mail(subject, 
					  "Email recieved from " + name + '\n\nInquiry: \n\n"' + message + '"' + "\n\nReply here: " + email,
					  settings.EMAIL_HOST_USER, 
					  [settings.EMAIL_HOST_USER], 
					  fail_silently=False)
			
			message_recieved = email

			messages.success(request, email)

			return HttpResponseRedirect(request.path)
			
	context.update({'contactform' : contactform})

	return render(request, 'contact/contact.html', context)

