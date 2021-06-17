from django.contrib import admin
from .models import Entry, Category
from django.utils.html import format_html

# Register your models here.
class AdminEntry(admin.ModelAdmin):
	
	def _thumbnail(self, obj):
		return obj.display_thumbnail()

	def _image_file(self, obj):
		return obj.thumb_nail

	_image_file.short_description = "Image file"

	def get_form(self, request, obj=None, **kwargs):

		form = super(AdminEntry, self).get_form(request, obj, **kwargs)
		form.base_fields['body'].widget.attrs['style'] = 'height: 500%;'
		return form
		
	class Media:
		js = (
			'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js', # jquery
			'/static/blog/myscript.js',       # project static folder
			#'app/js/myscript.js',   # app static folder
		)

	readonly_fields = [
						"updated_at", 
						"created_at", 
						"total_views", 
						"views_per_day", 
						'display_thumbnail' 
					]
	
	fields = (
				('title', 'is_live'), 
				'body',
				('display_thumbnail', 'thumb_nail', 'thumb_nail_x_position', 'thumb_nail_y_position'),
				'category',
				'created_at', 
				'updated_at', 
			)
	

	list_display = [
					'title', 
					'is_live',
					'total_views',
					'created_at', 
					'updated_at', 
					'_thumbnail',
				]

	filter_horizontal = ('category', )

class CategoryEntry(admin.ModelAdmin):
	fields = ('name', 'colour')

admin.site.register(Entry, AdminEntry)
admin.site.register(Category, CategoryEntry)