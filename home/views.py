from django.shortcuts import render
from .models import Info
from blog.models import Entry

# Create your views here.
def home(request):

	info = Info.objects.all()

	#blog_entry   = Entry.objects.filter(is_live = True).first()

	blog_snippet_list = Entry.objects.filter(is_live = True).order_by('created_at').reverse()[:2]

	"""
	try:
		blog_snippet_list = blog_entry.get_more_recent_posts()
	except(AttributeError):
		blog_snippet_list = []
	"""
	print(blog_snippet_list[0].calculate_size())



	return render(request, 'home/home.html', {'information' : info, 'blog_snippet_list' : blog_snippet_list})
