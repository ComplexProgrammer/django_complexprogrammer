from django.db import models
from django.utils.translation import gettext_lazy as _


class Room(models.Model):
	number = models.CharField(max_length=50, unique=True, verbose_name=_('Xona raqami'))

	class Meta:
		verbose_name = _('Xona')
		verbose_name_plural = _('Xonalar')
		ordering = ['number']

	def __str__(self) -> str:
		return self.number


class Cabinet(models.Model):
	number = models.CharField(max_length=50, unique=True, verbose_name=_('Shkaf raqami'))

	class Meta:
		verbose_name = _('Shkaf')
		verbose_name_plural = _('Shkaflar')
		ordering = ['number']

	def __str__(self) -> str:
		return self.number


class ArchiveType(models.Model):
	name = models.CharField(max_length=100, unique=True, verbose_name=_('Turi'))

	class Meta:
		verbose_name = _('Arxiv turi')
		verbose_name_plural = _('Arxiv turlari')
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class ArchiveStatus(models.Model):
	name = models.CharField(max_length=100, unique=True, verbose_name=_('Holati'))

	class Meta:
		verbose_name = _('Holat')
		verbose_name_plural = _('Holatlar')
		ordering = ['name']

	def __str__(self) -> str:
		return self.name


class ArchiveItem(models.Model):
	room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='archive_items', verbose_name=_('Xona'))
	cabinet = models.ForeignKey(Cabinet, on_delete=models.PROTECT, related_name='archive_items', verbose_name=_('Shkaf'))
	cabinet_floor = models.CharField(max_length=50, verbose_name=_('Shkaf qavati'))
	type = models.ForeignKey(ArchiveType, on_delete=models.PROTECT, related_name='archive_items', verbose_name=_('Turi'))
	register_number = models.CharField(max_length=100, verbose_name=_('Reyestr raqami'))
	request_number = models.CharField(max_length=100, verbose_name=_('Talabnoma raqami'))
	patent_number = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Patent raqami'))
	status = models.ForeignKey(ArchiveStatus, on_delete=models.PROTECT, related_name='archive_items', verbose_name=_('Holati'))
	document = models.FileField(upload_to='arxiv/documents/', null=True, blank=True, verbose_name=_('Hujjat'))
	is_public = models.BooleanField(default=True, verbose_name=_('Foydalanuvchilar ko\'ra oladi'))
	created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Yaratilgan vaqt'))

	class Meta:
		verbose_name = _('Arxiv yozuvi')
		verbose_name_plural = _('Arxiv yozuvlari')
		ordering = ['-created_at']

	def __str__(self) -> str:
		return f"{self.register_number}"
