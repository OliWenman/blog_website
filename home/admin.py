from django.contrib import admin
from .models import Info, PatchNote

# Register your models here.
class AdminInfo(admin.ModelAdmin):

	readonly_fields = ["updated_at"]
	list_display = ('peak_body', 'updated_at')

admin.site.register(Info, AdminInfo)

class AdminPatchNote(admin.ModelAdmin):
	pass

admin.site.register(PatchNote, AdminPatchNote)
