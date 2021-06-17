from django.db import models

# Create your models here.
class Info(models.Model):

	body       = models.TextField()
	updated_at = models.DateTimeField(auto_now = True)
	created_at = models.DateTimeField(auto_now_add = True)

	def peak_body(self):
		return self.body[0:30] + "..."

	def __str__(self):
		return self.peak_body()

class PatchNote(models.Model):

	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now     = True)
	version    = models.CharField(max_length       = 10)
	notes      = models.TextField()



"""
Hi everyone, welcome to my website! I have a Masters in Physics and, if you know me personally, you know I love to code. A little project of mine has been to build my own website from scratch. I have done this using Python with the Django Web framework.

The goal is to create a simple blogging website where I can talk about the things that interest me such as science, technology, my personal experiences, and anything else that, I and hopefully you, may find interesting to talk about.
"""