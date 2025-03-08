from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, NewsArticle, Subscriber
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .forms import NewsForm
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.utils.html import strip_tags
from django.contrib import messages


# Function to get categories for reuse
def get_categories():
    return Category.objects.all()

# Latest news display at the home page


# Latest news display at the news page
def news_home(request):
    categories = get_categories()
    latest_news = NewsArticle.objects.all().order_by('-date_added')  # Get all articles ordered by date

    # Check if we're on the homepage (show 6 latest news)
    if request.path == '/':  # Homepage (home/home.html)
        latest_news = latest_news[:6]  # Limit to 6 latest news articles
        paginator = None  # No pagination for homepage
        
    else:  # News page with pagination (blogs/news_page.html)
        paginator = Paginator(latest_news, 10)  # 10 articles per page for the news page
        page_number = request.GET.get('page')
        try:
            page = paginator.get_page(page_number)
        except PageNotAnInteger:
            page = paginator.get_page(1)  # Default to first page if not a valid integer
        except EmptyPage:
            page = paginator.get_page(paginator.num_pages)  # Handle empty page
    
    # Canonical URL for SEO purposes
    canonical_url = request.build_absolute_uri(request.path)
    if paginator and (page.has_next() or page.has_previous()):
        canonical_url = f"{request.build_absolute_uri(request.path)}?page={page.number}"

    # Pass data to templates
    context = {
        'categories': categories,
        'latest_news': page if paginator else latest_news,  # Use page object for paginated news
        'canonical_url': canonical_url,
    }

    # Render the appropriate template based on the request path
    if request.path == '/':
        return render(request, 'home/home.html', context)  
    else:
        return render(request, 'blogs/news_home.html', context) 



# News articles by category
def category_news(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    articles = NewsArticle.objects.filter(category=category).order_by('-date_added')
    context = {'category': category, 'articles': articles}
    return render(request, 'blogs/category_news.html', context)


# Detailed news article view
def news_detail(request, news_slug):
    article = get_object_or_404(NewsArticle, slug=news_slug)
    article_tags = article.tags.all()
    article_category = article.category
    similar_articles = NewsArticle.objects.filter(tags__in=article_tags).filter(category=article_category).exclude(
        id=article.id).distinct()
    
    canonical_url = request.build_absolute_uri(request.path)
    
    context = {'article': article, 'similar_articles': similar_articles, 'canonical_url': canonical_url}
    return render(request, 'blogs/news_detail.html', context)


# Subscribe view for the newsletter
def subscribe_view(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:subscribed')
    else:
        form = NewsForm()
    
    return render(request, 'blogs/subscribe_view.html', {'form': form})


# Subscribed confirmation page
def subscribed(request):
    return render(request, 'blogs/subscribed.html')


# Send newsletter to all subscribers
def send_newsletter():
    subscribers = Subscriber.objects.all()
    
    # Get the latest news article
    try:
        latest_news = NewsArticle.objects.latest('date_added')
    except NewsArticle.DoesNotExist:
        print("No news articles available.")
        return

    subject = 'Latest Consolata News'
    message = f"Check out our latest news: {latest_news.title}"
    html_message = f"<p>Check out our latest news: <strong>{latest_news.title}</strong></p>"

    # Prepare the email list
    mail_list = [
        (subject, strip_tags(html_message), 'admin@seminary.com', [subscriber.email])
        for subscriber in subscribers
    ]

    # Send emails in bulk
    try:
        send_mass_mail(mail_list)
        print("Newsletter sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")
