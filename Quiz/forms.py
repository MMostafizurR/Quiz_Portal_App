from django import forms
from django.contrib.auth.models import User
from .models import Option, Participant, Question, Quiz


class UserRegistrationForm(forms.ModelForm):
  password = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control'})
  )
  confirm_password = forms.CharField(
      widget=forms.PasswordInput(attrs={'class': 'form-control'})
  )

  ROLE_CHOICES = (
      ('participant', 'Quiz Participant'),
      ('creator', 'Quiz Creator / Admin'),
  )
  role = forms.ChoiceField(
      choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'})
  )

  class Meta:
    model = User
    fields = ['username', 'email', 'password']
    help_texts = {
        'username': None,
        'email': None,
        'password': None,
    }
    widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }

  def clean(self):
    cleaned_data = super().clean()
    password = cleaned_data.get('password')
    confirm_password = cleaned_data.get('confirm_password')
    if password and confirm_password and password != confirm_password:
      raise forms.ValidationError("Passwords do not match!")
    return cleaned_data


class ParticipantForm(forms.ModelForm):

  class Meta:
    model = Participant
    fields = ['Name', 'Class', 'Age', 'Gender', 'Institution']
    widgets = {
        'Name': forms.TextInput(attrs={'class': 'form-control'}),
        'Class': forms.TextInput(attrs={'class': 'form-control'}),
        'Age': forms.NumberInput(attrs={'class': 'form-control'}),
        'Gender': forms.Select(attrs={'class': 'form-select'}),
        'Institution': forms.TextInput(attrs={'class': 'form-control'}),
    }


class QuizCreateForm(forms.ModelForm):

  class Meta:
    model = Quiz
    fields = ['title', 'description']
    widgets = {
        'title': forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter quiz title'}
        ),
        'description': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description',
            }
        ),
    }


class QuestionCreateForm(forms.ModelForm):

  class Meta:
    model = Question
    fields = ['question']
    widgets = {
        'question': forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Enter question text',
            }
        ),
    }