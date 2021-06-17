from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe

from datetime import datetime

import re
import html
import os
import ckeditor_uploader
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

class Category(models.Model):

	def __str__(self):
		return self.name

	class Meta: 
		verbose_name = "Category"
		verbose_name_plural = "Categories"

	name = models.CharField(max_length = 40)
	colour = models.CharField(max_length = 5)

# Create your models here.
class Entry(models.Model):
	
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return self.title.replace(" ", "-")

	def increaseviews(self, request):
		if request.session.get('last_visit'):
			# The session has a value for the last visit
			last_visit_time = request.session.get('last_visit')
			visits = request.session.get('visits', 0)

			if (datetime.now() - datetime.strptime(last_visit_time[:-7], "%Y-%m-%d %H:%M:%S")).days > 0:
				request.session['visits'] = visits + 1
				request.session['last_visit'] = str(datetime.now())
				self.total_views += 1
		else:
			# The get returns None, and the session does not have a value for the last visit.
			request.session['last_visit'] = str(datetime.now())
			request.session['visits']     = visits = 1
			self.total_views += 1
	
		self.save()

		return request

	def display_thumbnail(self):

		width = 'width:320px;'
		height = 'height:240px;'
		_id = "id_image_" + self.title.replace(' ', '_') 
		print(_id)
		object_fit = 'object-fit:cover;'
		position = 'object-position: ' + str(self.thumb_nail_x_position) + "% " + str(self.thumb_nail_y_position) + "%;"
		style = object_fit + width + height + position

		if self.has_thumbnail():

			html = '<img style="' + style + '" src="' + self.thumb_nail.url + '" id="' + _id +'"/>'

		else:
			bg_colour   = 'background: black;'
			text_colour = 'color: white;'

			object_fit = 'object-fit:cover;'
			position = 'object-position: ' + str(self.thumb_nail_x_position) + "% " + str(self.thumb_nail_y_position) + "%;"
			style = object_fit + width + height + position + text_colour + bg_colour

			html = '<img src="" style="' + style + '" id="' + _id +'"/>'

		return mark_safe(html)
	
	def has_thumbnail(self):
		return self.thumb_nail.name is not ""

	def peak_text(self):

		text = re.sub('<[^<]+?>', '', self.body)
		text = html.unescape(text)
		return text[0:200] + "..."

	
	#Override save method to delete old images if they are changed
	def save(self, *args, **kwargs):
		try:
			this = Entry.objects.get(id=self.id)

			if this.thumb_nail != self.thumb_nail:
				this.thumb_nail.delete()
		except: 
			pass
			
		super(Entry, self).save(*args, **kwargs)

	def get_more_recent_posts(self, n_posts = 2):

		entries = Entry.objects.all().order_by('created_at').reverse()
	
		for i in entries:
			if self == i:
				entries = entries.exclude(title = i.title)

		recent_posts = entries[:n_posts]

		return recent_posts

	def calculate_size(self):
		import re
		import os

		string = self.body

		regex = r"""<ima?ge?(?=\s|>)(?=(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*?\ssrc=(['"]?)(.*?)\1(?:\s|>))(?:[^>=]|='[^']*'|="[^"]*"|=[^'"][^\s>]*)*>""";

		image_list = []

		total_mem = 0

		for matchObj in re.finditer( regex, string, re.M|re.I|re.S):
			
			path = os.path.join(settings.BASE_DIR, matchObj.group(2)[:0]) 

			total_mem = total_mem + os.stat(path).st_size

		print(total_mem)
	
	title         = models.CharField(max_length = 100, unique = True, help_text = "Title of each entry")

	created_at    = models.DateTimeField(auto_now_add = True)
	updated_at    = models.DateTimeField(auto_now = True)
	
	thumb_nail            = models.ImageField(upload_to='uploads/%Y/%m/%d', null = True, blank = True)
	thumb_nail_x_position = models.IntegerField(default = 50)
	thumb_nail_y_position = models.IntegerField(default = 50)
	
	body          = RichTextUploadingField(blank=True)

	total_views   = models.PositiveIntegerField(default = 0)
	views_per_day = models.PositiveIntegerField(default = 0)

	is_live       = models.BooleanField(default = False)

	category = models.ManyToManyField(Category, blank=True)

	    
class ViewsPerDay(models.Model): 
	entry = models.ForeignKey(Entry, editable=False, on_delete=models.CASCADE)
	views = models.PositiveIntegerField(default = 0)
	date  = models.DateTimeField()


class UrlHit(models.Model):
	url     = models.URLField()
	hits    = models.PositiveIntegerField(default=0)

	def __str__(self):
		return str(self.url)

	def increase(self):
		self.hits += 1
		self.save()


class HitCount(models.Model):
	url_hit = models.ForeignKey(UrlHit, editable=False, on_delete=models.CASCADE)
	ip      = models.CharField(max_length=40)
	session = models.CharField(max_length=40)
	date    = models.DateTimeField(auto_now=True)

	    
