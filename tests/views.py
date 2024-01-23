import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.db.models.functions import Concat
from django.db.models import F
from tests.models import Answers, Books, Groups, Questions, Topics, Types

def tests(request):
    data=[]
    _type='type'
    type_data=[]
    type_id = request.GET.get('type_id', 0)
    group_id = request.GET.get('group_id', 0)
    book_id = request.GET.get('book_id', 0)
    topic_id = request.GET.get('topic_id', 0)
    question_id = request.GET.get('question_id', 0)
    if type_id is 0 and group_id is 0 and book_id is 0 and topic_id is 0 and question_id is 0:
        data=Types.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        if type_id != 0:
            _type='group'
            type_data=Types.objects.filter(is_deleted=False, id=type_id).values().first()
            data=Groups.objects.filter(is_deleted=False, type_id=type_id).order_by('sort_order').values()
        if group_id != 0:
            _type='book'
            type_data=Groups.objects.filter(is_deleted=False, id=group_id).values().first()
            data=Books.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order')
            data=data.annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).values()    
        if book_id != 0:
            _type='topic'
            type_data=Books.objects.filter(is_deleted=False, id=book_id).annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).values().first()
            data=Topics.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
        if topic_id != 0:
            _type='question'
            type_data=Topics.objects.filter(is_deleted=False, id=topic_id).values().first()
            data=Questions.objects.filter(is_deleted=False, topic_id=topic_id).order_by('sort_order').values()
        if question_id != 0:
            _type='answer'
            type_data=Questions.objects.filter(is_deleted=False, id=question_id).values().first()
            data=Answers.objects.filter(is_deleted=False, question_id=question_id).order_by('sort_order').values() # type: ignore
    
    context={
        'data': data,
        'type': _type,
        'type_data':json.dumps(type_data, default=serialize_datetime),
    }
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
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    if type_id is False:
        data=Books.objects.filter(is_deleted=False).order_by('sort_order').annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).values()
    else:
        data=Books.objects.filter(is_deleted=False, type_id=type_id).annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).order_by('sort_order').values()
    if group_id is False:
        data=Books.objects.filter(is_deleted=False).order_by('sort_order').annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).values()
    else:
        data=Books.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').annotate(name_en_us=F('book_type__name_en_us'), name_ru_ru=F('book_type__name_ru_ru'), name_uz_crl=F('book_type__name_uz_crl'), name_uz_uz=F('book_type__name_uz_uz'), image=F('book_type__image')).values()
    return JsonResponse(list(data), safe=False) 


def GetTopics(request):
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    if type_id is False:
        data=Topics.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Topics.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data=Topics.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Topics.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').values()
    if book_id is False:
        data=Topics.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Topics.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 
    

def GetQuestions(request):
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    topic_id = request.GET.get('topic_id', False)
    if type_id is False:
        data=Questions.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Questions.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data=Questions.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Questions.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').values()
    if book_id is False:
        data=Questions.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Questions.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
    if topic_id is False:
        data=Questions.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Questions.objects.filter(is_deleted=False, topic_id=topic_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False) 
    

def GetAnswers(request):
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    topic_id = request.GET.get('topic_id', False)
    question_id = request.GET.get('question_id', False)
    if type_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, type_id=type_id).values()
    if group_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, group_id=group_id).order_by('sort_order').values()
    if book_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, book_id=book_id).order_by('sort_order').values()
    if topic_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, topic_id=topic_id).order_by('sort_order').values()
    if question_id is False:
        data=Answers.objects.filter(is_deleted=False).order_by('sort_order').values()
    else:
        data=Answers.objects.filter(is_deleted=False, question_id=question_id).order_by('sort_order').values()
    return JsonResponse(list(data), safe=False)

def GetCounts(request):
    type_id = request.GET.get('type_id', False)
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    topic_id = request.GET.get('topic_id', False)
    question_id = request.GET.get('question_id', False)
    types_count=Types.objects.filter(is_deleted=False).count()
    if type_id is False:
        groups_count=Groups.objects.filter(is_deleted=False).count()
        books_count=Books.objects.filter(is_deleted=False).count()
        topics_count=Topics.objects.filter(is_deleted=False).count()
        questions_count=Questions.objects.filter(is_deleted=False).count()
        answers_count=Answers.objects.filter(is_deleted=False).count()
    else:
        groups_count=Groups.objects.filter(is_deleted=False, type_id=type_id).count()
        books_count=Books.objects.filter(is_deleted=False, type_id=type_id).count()
        topics_count=Topics.objects.filter(is_deleted=False, type_id=type_id).count()
        questions_count=Questions.objects.filter(is_deleted=False, type_id=type_id).count()
        answers_count=Answers.objects.filter(is_deleted=False, type_id=type_id).count()
    
    context={
        'types_count': types_count,
        'groups_count': groups_count,
        'books_count': books_count,
        'topics_count': topics_count,
        'questions_count': questions_count,
        'answers_count': answers_count,
        
    }
    return JsonResponse(context, safe=False) 