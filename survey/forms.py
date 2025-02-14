from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Survey, Question, Choice, Response, Answer
from django.contrib.auth.models import User

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['survey', 'text', 'question_type']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'text']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['survey']

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['response', 'question', 'choice', 'text_answer']

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
