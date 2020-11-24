from typing import Dict, Any

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question,Choice

def index(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    latest_question_list = Question.objects.order_by('-pub_date')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
# Create your views here.
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id,winner_choiceid):
    question = get_object_or_404(Question, pk=question_id)
    event=get_object_or_404(Choice,id=winner_choiceid)
    print("hello"+event)
    return render(request, 'polls/results.html', {'question': question ,'event' : event})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        all_choice=question.choice_set.all()
        temp = {}
        for x in all_choice :
            temp[all_choice.get(choice_text=x)] = all_choice.get(choice_text=x).votes
        winner_choice = max(temp, key=temp.get)
        #print("Event created : " + winner_choice.choice_text + "\t( vote = ", winner_choice.votes,")")

        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        #return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        return render(request, 'polls/results.html', {'question': question, 'event': winner_choice})