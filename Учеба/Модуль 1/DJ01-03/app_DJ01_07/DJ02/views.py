from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
	return render(request, 'DJ02/index.html', {'title': "Главная"})

def about(request):
	return render(request, 'DJ02/about.html', {'title': "О Нас"})

def feedback(request):
	return render(request, 'DJ02/feedback.html', {'title': "Обратная Связь"})
