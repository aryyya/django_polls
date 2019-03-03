from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Question

def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request, 'polls/index.html', {
        'question_list': question_list
    })

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {
        'question': question
    })

def results(request, question_id):
    return HttpResponse(f'You are looking at the results of question {question_id}')

def vote(request, question_id):
    return HttpResponse(f'You are voting on question {question_id}')
