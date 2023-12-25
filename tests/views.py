import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from tests.models import Answers, Books, Groups, Questions, Topics, Types

def tests(request):
    data=[]
    type='type'
    type_data=[]
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    topic_id = request.GET.get('topic_id', False)
    question_id = request.GET.get('question_id', False)
    if type_id is False and group_id is False and book_id is False and topic_id is False and question_id is False:
        data=Types.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        if type_id is not False:
            type='group'
            type_data=Types.objects.filter(is_deleted=False, id=type_id).values().first()
            data=Groups.objects.filter(is_deleted=False, type_id=type_id).order_by('sort_order').values()
        if group_id is not False:
            type='book'
            type_data=Groups.objects.filter(is_deleted=False, id=group_id).values().first()
            data=Books.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').values()
        if book_id is not False:
            type='topic'
            type_data=Books.objects.filter(is_deleted=False, id=book_id).values().first()
            data=Topics.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
        if topic_id is not False:
            type='question'
            type_data=Topics.objects.filter(is_deleted=False, id=topic_id).values().first()
            data=Questions.objects.filter(is_deleted=False, topic_id=topic_id).order_by('sort_order').values()
        if question_id is not False:
            type='answer'
            type_data=Questions.objects.filter(is_deleted=False, id=question_id).values().first()
            data=Answers.objects.filter(is_deleted=False, question_id=question_id).order_by('sort_order').values() # type: ignore
    context={
        'data': data,
        'type': type,
        'type_data':json.dumps(type_data, default=serialize_datetime),
    }
    print(data)
    return render(request, 'tests/index.html', context=context)
def serialize_datetime(obj): 
    if isinstance(obj, datetime.datetime): 
        return obj.isoformat() 
    raise TypeError("Type not serializable") 

def GetTypes(request):
    data=Types.objects.filter(is_deleted=False).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 

def GetGroups(request):
    type_id = request.GET.get('type_id', False)
    if type_id is False:
        data=Groups.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Groups.objects.filter(is_deleted=False, type_id=type_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 

def GetBooks(request):
    group_id = request.GET.get('group_id', False)
    if group_id is False:
        data=Books.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Books.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').values()
    return JsonResponse(list(data.values('id', 'name_en_us', 'name_ru_ru', 'name_uz_crl', 'name_uz_uz', 'type__image', 'group_id')), safe=False) 


def GetTopics(request):
    book_id = request.GET.get('book_id', False)
    if book_id is False:
        data=Topics.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Topics.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 
    

def GetQuestions(request):
    topic_id = request.GET.get('topic_id', False)
    if topic_id is False:
        data=Questions.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Questions.objects.filter(is_deleted=False, topic_id=topic_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 
    

def GetAnswers(request):
    question_id = request.GET.get('question_id', False)
    if question_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, question_id=question_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False)