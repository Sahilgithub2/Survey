import json
import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from survey.forms import SurveyForm, QuestionForm, ChoiceForm, ResponseForm, AnswerForm, SignUpForm
from survey.models import Survey, Question, Choice, Response, Answer

def home(request):
    surveys = Survey.objects.all()
    return render(request, 'home.html', {'surveys': surveys})

@login_required
def survey_detail(request, survey_id):
    survey = Survey.objects.get(id=survey_id)
    questions = survey.questions.all()  # Ensure questions are fetched

    if request.method == 'POST':
        response = Response.objects.create(user=request.user, survey=survey)

        for question in questions:
            answer_data = request.POST.get(f'question_{question.id}')
            if question.question_type == 'choice' and answer_data:
                choice = Choice.objects.get(id=answer_data)
                Answer.objects.create(response=response, question=question, choice=choice)
            elif answer_data:  # If it's a text answer
                Answer.objects.create(response=response, question=question, text_answer=answer_data)

        return redirect('dashboard')

    return render(request, 'survey_detail.html', {'survey': survey, 'questions': questions})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in after signup
            return redirect('home')  # Redirect to surveys page
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def dashboard(request):
    responses = Response.objects.filter(user=request.user)
    
    # Prepare data for the line chart
    survey_data = {}
    
    for response in responses:
        survey_title = response.survey.title
        if survey_title not in survey_data:
            survey_data[survey_title] = 0
        survey_data[survey_title] += 1  # Count responses per survey
    
    context = {
        'survey_labels': list(survey_data.keys()),  
        'survey_counts': list(survey_data.values()),  
        'responses': responses
    }
    
    return render(request, 'dashboard.html', context)


@login_required
def download_feedback(request):
    responses = Response.objects.filter(user=request.user)

    # Create the HTTP response with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback.csv"'

    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['Survey', 'Question', 'Answer'])

    for response_obj in responses:
        for answer in response_obj.answers.all():
            answer_text = answer.choice.text if answer.choice else answer.text_answer
            writer.writerow([response_obj.survey.title, answer.question.text, answer_text])

    return response