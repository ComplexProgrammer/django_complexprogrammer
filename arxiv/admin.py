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
	list_display = ('register_number', 'request_number', 'patent_number', 'room', 'cabinet', 'cabinet_floor', 'type', 'status', 'created_at')
	list_filter = ('room', 'cabinet', 'type', 'status')
	search_fields = ('register_number', 'request_number', 'patent_number')
	autocomplete_fields = ('room', 'cabinet', 'type', 'status')
