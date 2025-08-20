from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import ArchiveItem, Room, Cabinet, ArchiveType, ArchiveStatus


def archive_list(request):
	queryset = ArchiveItem.objects.select_related('room', 'cabinet', 'type', 'status').all()

	room_id = request.GET.get('room')
	cabinet_id = request.GET.get('cabinet')
	type_id = request.GET.get('type')
	status_id = request.GET.get('status')
	register_number = request.GET.get('register_number')
	request_number = request.GET.get('request_number')
	patent_number = request.GET.get('patent_number')

	if room_id:
		queryset = queryset.filter(room_id=room_id)
	if cabinet_id:
		queryset = queryset.filter(cabinet_id=cabinet_id)
	if type_id:
		queryset = queryset.filter(type_id=type_id)
	if status_id:
		queryset = queryset.filter(status_id=status_id)
	if register_number:
		queryset = queryset.filter(register_number__icontains=register_number)
	if request_number:
		queryset = queryset.filter(request_number__icontains=request_number)
	if patent_number:
		queryset = queryset.filter(patent_number__icontains=patent_number)

	# Pagination qo'shish
	page = request.GET.get('page', 1)
	paginator = Paginator(queryset, 50)  # Har sahifada 50 ta yozuv
	
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)

	context = {
		'items': items,
		'paginator': paginator,
		'rooms': Room.objects.all(),
		'cabinets': Cabinet.objects.all(),
		'types': ArchiveType.objects.all(),
		'statuses': ArchiveStatus.objects.all(),
	}
	return render(request, 'arxiv/index.html', context)
