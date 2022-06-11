from django.core.paginator import Paginator
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Story



# def index(request):
#     return render(request, 'base.html')

def index(request):
    story_all = Story.objects.all()
    story = {'story_all':story_all}
    # for i in story_kr:
    #     print("제목 : ",i)
    return render(request, 'aesop/main.html', story)    

def page1(request, story_id):
    context = {}
    story = get_object_or_404(Story, id=story_id)
    context['story'] = story
    return render(request, 'aesop/page1.html', context)

def page2(request):
    return render(request, 'aesop/page2.html')

# def page2(request, story_id):
#     context = {}
#     story = get_object_or_404(Story, id=story_id)
#     context['story'] = story
#     return render(request, 'aesop/page2.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'aesop/question_detail.html', context)


def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('aesop:detail', question_id=question.id)
    else:
        return HttpResponseNotAllowed('Only POST is possible.')
    context = {'question': question, 'form': form}
    return render(request, 'aesop/question_detail.html', context)


def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.create_date = timezone.now()
            question.save()
            return redirect('aesop:index')
    else:
        form = QuestionForm()
    context = {'form': form}
    return render(request, 'aesop/question_form.html', context)

def main_1(request):
    return render(request,'aesop/main.html') 

def recode(request):
    return render(request, 'aesop/recode.html')

def creat_text(request):
    return render(request, 'aesop/creat_text.html')

def creat_image(request):
    return render(request, 'aesop/creat_image.html')