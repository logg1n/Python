from django.shortcuts import render, redirect
from .models import NewsPost
from .forms import NewsForm

# Create your views here.
def home(request):
    news = NewsPost.objects.all()
    return render(request, 'DJ03/news.html', {'news': news})

def add(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()  # <-- вот здесь сохраняются данные в БД, включая дату
            return redirect('news_home')
    else:
        form = NewsForm()

    return render(request, 'DJ03/news_add.html', {'form': form})
