import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader

from tests.models import Answers, Books, Groups, Questions, Topics

def tests(request):
    data=[]
    type='group'
    type_id=0
    type_data=[]
    group_id = request.GET.get('group_id', False)
    book_id = request.GET.get('book_id', False)
    topic_id = request.GET.get('topic_id', False)
    question_id = request.GET.get('question_id', False)
    if group_id is False and book_id is False and topic_id is False and question_id is False:
        data=Groups.objects.all().values()
    else:
        if group_id is not False:
            type='book'
            type_id=group_id
            type_data=Groups.objects.filter(id=group_id).values().first()
            data=Books.objects.filter(group_id=group_id).values()
        if book_id is not False:
            type='topic'
            type_id=book_id
            type_data=Books.objects.filter(id=book_id).values().first()
            data=Topics.objects.filter(book_id=book_id).values()
        if topic_id is not False:
            type='question'
            type_id=topic_id
            type_data=Topics.objects.filter(id=topic_id).values().first()
            data=Questions.objects.filter(topic_id=topic_id).values()
        if question_id is not False:
            type='answer'
            type_id=question_id
            type_data=Questions.objects.filter(id=question_id).values().first()
            data=Answers.objects.filter(question_id=question_id).values() # type: ignore
    context={
        'data': data,
        'type': type,
        'type_data':type_data,
        'type_id':type_id
    }
    return render(request, 'tests/index.html', context=context)

def GetGroups(request):
    data=Groups.objects.all().values()
    return JsonResponse(list(data), safe=False) 

def GetBooks(request):
    group_id = request.GET.get('group_id', False)
    if group_id is False:
        return None
    else:
        data=Books.objects.filter(group_id=group_id).values()
        return JsonResponse(list(data), safe=False) 


def GetTopics(request):
    book_id = request.GET.get('book_id', False)
    if book_id is False:
        return None
    else:
        data=Topics.objects.filter(book_id=book_id).values()
        return JsonResponse(list(data), safe=False) 
    

def GetQuestions(request):
    topic_id = request.GET.get('topic_id', False)
    if topic_id is False:
        return None
    else:
        data=Questions.objects.filter(topic_id=topic_id).values()
        return JsonResponse(list(data), safe=False) 
    

def GetAnswers(request):
    question_id = request.GET.get('question_id', False)
    if question_id is False:
        return None
    else:
        data=Answers.objects.filter(question_id=question_id).values()
        return JsonResponse(list(data), safe=False) 
    
def test_item(request, type, id):
    if type == 'group':
        data=Groups.objects.all().values()
    if type == 'book':
        group_id = request.GET.get('group_id', False)
        if group_id is False:
            return None
        else:
            data=Books.objects.filter(group_id=group_id).values()
    context={
        'data': range(1, 109),
        'type': type
    }
    return render(request, 'tests/index.html', context=context)