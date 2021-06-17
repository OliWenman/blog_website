from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Entry, HitCount, UrlHit

from datetime import datetime
import re

# Create your views here.
def entry_list_page(request, current_page):

	#Get the entries
	entries = Entry.objects.filter(is_live = True).order_by('created_at').reverse()
	
	#Change number of items you want displayed on one page
	items_per_page = 3

	#Calculate the needed number of pages
	no_of_pages = len(entries) // items_per_page
	if (len(entries) % items_per_page != 0):
		no_of_pages += 1

	pages = []
	for i in range(no_of_pages):
		pages.append(i + 1)

	start_pos = 0 if current_page == 1 else items_per_page * (current_page - 1)
	item_list = entries[start_pos: start_pos + items_per_page]

	next_page = current_page + 1
	prev_page = current_page - 1
	
	try:
		n_pages   = pages[-1]
	except(IndexError):
		n_pages = 1

	page_lim = 2

	mask = []
	
	for i in pages:

		if i < current_page - page_lim and  i != 1 :
			pass
		
		elif i > current_page + page_lim and i != n_pages:
			pass
		
		else:
			mask.append(i)

	return render(request, 
				  'blog/entry_list_page.html', 
				  {
						'blog_snippet_list': item_list, 
				  		'pages' : mask, 
				  		'current_page' : current_page, 
				  		'next_page': next_page, 
				  		'prev_page' : prev_page, 
				  		'n_pages':n_pages
				  }
			)

def blog_entry(request, name):
	"""
	def get_client_ip(request):
	    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	    if x_forwarded_for:
	        ip = x_forwarded_for.split(',')[-1].strip()
	    else:
	        ip = request.META.get('REMOTE_ADDR')
	    return ip

	entries = Entry.objects.filter()
	ip = get_client_ip(request)
	"""

	"""
	def hit_count(request):

		def get_client_ip(request):
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			return ip

		if not request.session.session_key:
			request.session.save()
		s_key = request.session.session_key
		ip = get_client_ip(request)
		url, url_created = UrlHit.objects.get_or_create(url=request.path)

		if url_created:
			track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
			if created:
				url.increase()
				request.session[ip] = ip
				request.session[request.path] = request.path
		else:
			if ip and request.path not in request.session:
				track, created = HitCount.objects.get_or_create(url_hit=url, ip=ip, session=s_key)
				if created:
					url.increase()
					request.session[ip] = ip
					request.session[request.path] = request.path
		return url.hits

	print(hit_count(request))
	"""
	title   = name.replace("-", " ")
	entry   = Entry.objects.get(title = title, is_live = True)
	request = entry.increaseviews(request)

	blog_snippet_list = entry.get_more_recent_posts()

	return render(request, 'blog/blog_entry.html', {'entry': entry, 'blog_snippet_list': blog_snippet_list})
