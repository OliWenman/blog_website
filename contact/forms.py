from django import forms
from django.core.validators import ValidationError

class ContactForm(forms.Form):

	def clean(self):

		cleaned_data = super(ContactForm, self).clean()

		#Make sure the email and confirm_email are the same, if not raise a validation error.
		if cleaned_data.get('confirm_email') != cleaned_data.get('email'):
			raise ValidationError({'confirm_email': ['Email is not the same.']})


	name          = forms.CharField(label='Name', max_length=100)
	subject       = forms.CharField(label='Subject', max_length=100)
	message       = forms.CharField(widget=forms.Textarea)
	email         = forms.EmailField(label='Email')
	confirm_email = forms.EmailField(label='Confirm Email')

