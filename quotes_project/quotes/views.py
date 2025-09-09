from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
import random
from .models import Quote
from .forms import QuoteForm

# Главная страница с случайной цитатой
def index(request):
    quote = get_random_quote()
    if not quote:
        return render(request, 'quotes/no_quotes.html')
    return render(request, 'quotes/index.html', {'quote': quote})

# Получение случайной цитаты
def get_random_quote():
    quotes = Quote.objects.all()
    if not quotes.exists():
        return None
    
    total_weight = sum(q.weight for q in quotes)
    rand_num = random.uniform(0, total_weight)
    
    cumulative_weight = 0
    for quote in quotes:
        cumulative_weight += quote.weight
        if rand_num <= cumulative_weight:
            quote.increment_views()
            return quote
    return quotes.first()

# Обработка лайка
def like_quote(request, quote_id):
    try:
        quote = get_object_or_404(Quote, id=quote_id)
        quote.add_like()
        new_quote = get_random_quote()
        return JsonResponse({
            'likes': quote.likes,
            'dislikes': quote.dislikes,
            'new_quote': {
                'id': new_quote.id,
                'text': new_quote.text,
                'source': new_quote.source,
                'views': new_quote.views,
                'likes': new_quote.likes,
                'dislikes': new_quote.dislikes
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Обработка дизлайка
def dislike_quote(request, quote_id):
    try:
        quote = get_object_or_404(Quote, id=quote_id)
        quote.add_dislike()
        new_quote = get_random_quote()
        return JsonResponse({
            'likes': quote.likes,
            'dislikes': quote.dislikes,
            'new_quote': {
                'id': new_quote.id,
                'text': new_quote.text,
                'source': new_quote.source,
                'views': new_quote.views,
                'likes': new_quote.likes,
                'dislikes': new_quote.dislikes
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Страница популярных цитат
def popular_quotes(request):
    quotes = Quote.objects.all().order_by('-likes')[:10]  # Топ-10 популярных
    return render(request, 'quotes/popular.html', {'quotes': quotes})

# Форма добавления новой цитаты
def submit_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Цитата успешно добавлена!')
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'quotes/submit.html', {'form': form})

# Страница случайной цитаты
def random_quote(request):
    quote = get_random_quote()
    if not quote:
        return render(request, 'quotes/no_quotes.html')
    return render(request, 'quotes/random_quote.html', {'quote': quote})