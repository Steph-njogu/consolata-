from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, NewsArticle, Subscriber
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import NewsForm
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib import messages




# Create your views here.

def news_home(request):
    categories = Category.objects.all()

    latest_news = NewsArticle.objects.all().order_by('-date_added')

    paginator = Paginator(latest_news, 3)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)
    canonical_url = request.build_absolute_uri(request.path)
    if page.has_next() or page.has_previous():
        canonical_url = f"{request.build_absolute_uri(request.path)}?page={page.number}"

    # Pass data to the template
    context = {
        'categories': categories,
        'latest_news': page,
        'canonical_url': canonical_url,
    }

    return render(request, 'blogs/news_home.html', context)



def category_news(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = NewsArticle.objects.filter(category=category).order_by('-date_added')
    context = {'category': category, 'articles': articles}
    return render(request, 'blogs/category_news.html', context)

def news_detail(request, news_slug):
    article = get_object_or_404(NewsArticle, slug=news_slug)
    article_tags = article.tags.all()
    article_category = article.category
    similar_articles = NewsArticle.objects.filter(tags__in = article_tags).filter(category=article_category).exclude(
        id = article.id
    ).distinct()
    canonical_url = request.build_absolute_uri(request.path)
    context = {'article':article, 'similar_articles':similar_articles, 'canonical_url': canonical_url}
    return render (request, 'blogs/news_detail.html', context)


def subscribe_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:subscribed')
    else:
        form = NewsForm()
    return render (request, 'blogs/subscribe_view.html', {'form':form})




def subscribed(request):
    return render(request, 'blogs/subscribed.html')



def send_newsletter():
    subscribers = Subscriber.objects.all()
    latest_news = NewsArticle.objects.latest('date_added')
    subject = 'Latest Consolata News'
    message = f"Check out our latest news: {latest_news.title}"
    html_message = f"<p>Check out our latest news: <strong>{latest_news.title}</strong></p>"

    # Prepare emails for mass sending
    mail_list = [
        (subject, strip_tags(html_message), 'admin@seminary.com', [subscriber.email])
        for subscriber in subscribers
    ]

    try:
        # Use send_mass_mail to send to all subscribers at once
        send_mass_mail(mail_list)
    except Exception as e:
        print(f"Error sending email: {e}")
