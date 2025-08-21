from django.contrib import admin
from .models import Room, Cabinet, ArchiveType, ArchiveStatus, ArchiveItem


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('number',)
	search_fields = ('number',)


@admin.register(Cabinet)
class CabinetAdmin(admin.ModelAdmin):
	list_display = ('number',)
	search_fields = ('number',)


@admin.register(ArchiveType)
class ArchiveTypeAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(ArchiveStatus)
class ArchiveStatusAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)


@admin.register(ArchiveItem)
class ArchiveItemAdmin(admin.ModelAdmin):
	list_display = ('register_number', 'request_number', 'patent_number', 'room', 'cabinet', 'cabinet_floor', 'type', 'status', 'is_public', 'document_link', 'created_at')
	list_filter = ('room', 'cabinet', 'type', 'status', 'is_public')
	search_fields = ('register_number', 'request_number', 'patent_number')
	autocomplete_fields = ('room', 'cabinet', 'type', 'status')
	list_editable = ('is_public',)
	readonly_fields = ('created_at',)
	list_per_page = 25  # Har sahifada 25 ta hujjat
	
	def document_link(self, obj):
		if obj.document:
			return f'<a href="{obj.document.url}" target="_blank" class="btn btn-sm btn-outline-primary"><i class="fas fa-eye"></i> Hujjatni ko\'rish</a>'
		return 'Hujjat yo\'q'
	document_link.short_description = 'Hujjat'
	document_link.allow_tags = True
	
	fieldsets = (
		('Asosiy ma\'lumotlar', {
			'fields': ('room', 'cabinet', 'cabinet_floor', 'type', 'status')
		}),
		('Hujjat ma\'lumotlari', {
			'fields': ('register_number', 'request_number', 'patent_number', 'document')
		}),
		('Ruxsatlar', {
			'fields': ('is_public',),
			'description': 'Foydalanuvchilar bu hujjatni ko\'ra oladimi yoki yo\'qmi'
		}),
		('Vaqt ma\'lumotlari', {
			'fields': ('created_at',),
			'classes': ('collapse',)
		}),
	)
	
	actions = ['make_public', 'make_private']
	
	def make_public(self, request, queryset):
		updated = queryset.update(is_public=True)
		self.message_user(request, f'{updated} ta hujjat foydalanuvchilar ko\'rishiga ochildi')
	make_public.short_description = 'Tanlangan hujjatlarni public qilish'
	
	def make_private(self, request, queryset):
		updated = queryset.update(is_public=False)
		self.message_user(request, f'{updated} ta hujjat foydalanuvchilar ko\'rishidan yashirildi')
	make_private.short_description = 'Tanlangan hujjatlarni private qilish'
	
	def get_queryset(self, request):
		"""Admin panelida barcha hujjatlarni ko'rsatish (public va private)"""
		return super().get_queryset(request)
	
	def get_list_display(self, request):
		"""Admin panelida qo'shimcha ma'lumotlarni ko'rsatish"""
		list_display = list(super().get_list_display(request))
		if 'is_public' in list_display:
			# is_public maydonini yaxshiroq ko'rsatish
			list_display[list_display.index('is_public')] = 'is_public'
		return list_display
	
	class Media:
		css = {
			'all': ('admin/css/archive_admin.css',)
		}
	
	def save_model(self, request, obj, form, change):
		"""Hujjat saqlanganda xabar berish"""
		if change and 'is_public' in form.changed_data:
			if obj.is_public:
				self.message_user(request, f'"{obj.register_number}" hujjati foydalanuvchilar ko\'rishiga ochildi')
			else:
				self.message_user(request, f'"{obj.register_number}" hujjati foydalanuvchilar ko\'rishidan yashirildi')
		super().save_model(request, obj, form, change)
	
	def get_actions(self, request):
		"""Admin panelida action tugmalarini ko'rsatish"""
		actions = super().get_actions(request)
		if not actions:
			actions = {}
		return actions
	
	def changelist_view(self, request, extra_context=None):
		"""Admin panelida qo'shimcha ma'lumotlarni ko'rsatish"""
		extra_context = extra_context or {}
		extra_context['total_public'] = str(ArchiveItem.objects.filter(is_public=True).count())
		extra_context['total_private'] = str(ArchiveItem.objects.filter(is_public=False).count())
		extra_context['total_documents'] = str(ArchiveItem.objects.filter(document__isnull=False).count())
		return super().changelist_view(request, extra_context)
	
	def get_list_filter(self, request):
		"""Admin panelida filterlarni ko'rsatish"""
		list_filter = list(super().get_list_filter(request))
		return list_filter
	
	def get_search_results(self, request, queryset, search_term):
		"""Admin panelida qidirish natijalarini ko'rsatish"""
		queryset, use_distinct = super().get_search_results(request, queryset, search_term)
		return queryset, use_distinct
	
	def get_ordering(self, request):
		"""Admin panelida tartiblash"""
		return ['-created_at']
	

	def get_readonly_fields(self, request, obj=None):
		"""Admin panelida readonly maydonlarni ko'rsatish"""
		readonly_fields = list(super().get_readonly_fields(request, obj))
		return readonly_fields
