import random
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ParticipantForm, QuestionCreateForm, QuizCreateForm, UserRegistrationForm
from .models import Option, Participant, Question, Quiz


def register_view(request):
  if request.method == 'POST':
    user_form = UserRegistrationForm(request.POST)
    participant_form = ParticipantForm(request.POST)
    if user_form.is_valid() and participant_form.is_valid():
      user = user_form.save(commit=False)
      user.set_password(user_form.cleaned_data['password'])

      if user_form.cleaned_data.get('role') == 'creator':
        user.is_staff = True  
      user.save()

      participant = participant_form.save(commit=False)
      participant.user = user
      participant.save()

      login(request, user)
      return redirect('dashboard')
  else:
    user_form = UserRegistrationForm()
    participant_form = ParticipantForm()

  return render(
      request,
      'register.html',
      {'user_form': user_form, 'participant_form': participant_form},
  )


def login_view(request):
  if request.method == 'POST':
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      return redirect('dashboard')
  else:
    form = AuthenticationForm()
  return render(request, 'login.html', {'form': form})


def logout_view(request):
  logout(request)
  return redirect('login')


@login_required
def dashboard_view(request):
  quizzes = Quiz.objects.all()
  participant = (
      request.user.participant
      if hasattr(request.user, 'participant')
      else None
  )
  return render(
      request,
      'dashboard.html',
      {'quizzes': quizzes, 'participant': participant},
  )


@login_required
def take_quiz_view(request, quiz_id):
  quiz = get_object_or_404(Quiz, id=quiz_id)
  questions = list(quiz.question_set.all())
  random.shuffle(questions)  

  quiz_data = []
  for q in questions:
    options = list(q.option_set.all())
    random.shuffle(options)  
    quiz_data.append({'question': q, 'options': options})

  if request.method == 'POST':
    score = 0
    total_questions = len(questions)

    for q in questions:
      selected_option_id = request.POST.get(str(q.id))
      if selected_option_id:
        try:
          opt = Option.objects.get(id=selected_option_id)
          if opt.is_correct:
            score += 1
        except Option.DoesNotExist:
          pass

    return render(
        request,
        'result.html',
        {'quiz': quiz, 'score': score, 'total_questions': total_questions},
    )

  return render(
      request, 'take_quiz.html', {'quiz': quiz, 'quiz_data': quiz_data}
  )


@staff_member_required
def create_quiz_view(request):
  if request.method == 'POST':
    form = QuizCreateForm(request.POST)
    if form.is_valid():
      quiz = form.save()
      return redirect('add_question', quiz_id=quiz.id)
  else:
    form = QuizCreateForm()
  return render(request, 'create_quiz.html', {'form': form})


@staff_member_required
def add_question_view(request, quiz_id):
  quiz = get_object_or_404(Quiz, id=quiz_id)

  if request.method == 'POST':
    question_text = request.POST.get('question')
    correct_option_num = request.POST.get('correct_option')

    if question_text and correct_option_num:
      question = Question.objects.create(quiz=quiz, question=question_text)

      for i in range(1, 5):
        opt_text = request.POST.get(f'option_{i}')
        if opt_text:
          is_correct = str(i) == correct_option_num
          Option.objects.create(
              question=question, option=opt_text, is_correct=is_correct
          )

      if 'add_another' in request.POST:
        return redirect('add_question', quiz_id=quiz.id)
      return redirect('dashboard')

  return render(request, 'add_question.html', {'quiz': quiz})