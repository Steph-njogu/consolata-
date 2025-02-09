from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibraryUserRegistrationForm
from django.db.models import Q
from .models import EBook, LibraryUser, EBookLoan, Category, EBookHistory, EBookDownload, BookRecommendation
from django.utils import timezone


# The registration form for the library users
def register(request):
    if request.method == 'POST':
        form = LibraryUserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = LibraryUserRegistrationForm()
    return render(request, 'register.html', {'form': form})


# Detail view for a specific category
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    ebooks_in_category = EBook.objects.filter(category=category)
    return render(request, 'categories/category_detail.html', {'category': category, 'ebooks': ebooks_in_category})


# Detail view for a specific eBook
def ebook_detail(request, slug):
    ebook = get_object_or_404(EBook, slug=slug)
    return render(request, 'ebooks/ebook_detail.html', {'ebook': ebook})
   


# Profile of the logged-in user
def user_profile(request):
    user_profile = get_object_or_404(LibraryUser, user=request.user)
    return render(request, 'users/user_profile.html', {'user_profile': user_profile})




# List all recommendations for the logged-in user
def book_recommendation_list(request):
    recommendations = BookRecommendation.objects.filter(user=request.user.libraryuser)
    return render(request, 'recommendations/recommendation_list.html', {'recommendations': recommendations})




# List all downloads for the logged-in user
def ebook_download_list(request):
    downloads = EBookDownload.objects.filter(user=request.user.libraryuser)
    return render(request, 'downloads/ebook_download_list.html', {'downloads': downloads})



# List all reading history for the logged-in user
def ebook_history_list(request):
    history = EBookHistory.objects.filter(user=request.user.libraryuser)
    return render(request, 'history/ebook_history_list.html', {'history': history})



# The search view
def search_books(request):
    query = request.GET.get('q', '')
    books = EBook.objects.filter(
        Q(title__icontains=query) | 
        Q(author__name__icontains=query) |
        Q(category__name__icontains=query) 
    ).distinct()
    return render(request, 'search_results.html', {'books': books})




























# views.py

def borrow_book(request, ebook_id):
    ebook = get_object_or_404(EBook, id=ebook_id)
    if request.user.is_authenticated:
        due_date = timezone.now().date() + timezone.timedelta(days=7)  # Loan for 7 days
        loan = EBookLoan.objects.create(user=request.user.libraryuser, ebook=ebook, due_date=due_date)
        return redirect('loan_details', loan_id=loan.id)
    else:
        return redirect('login')



# List all loans
def ebook_loan_list(request):
    loans = EBookLoan.objects.filter(user=request.user)
    return render(request, 'loans/loan_list.html', {'loans': loans})


# Mark ebook as returned and calculate late fees
def return_ebook(request, loan_id):
    loan = get_object_or_404(EBookLoan, id=loan_id)
    loan.returned = True
    loan.return_date = timezone.now().date()
    loan.calculate_late_fee()
    loan.save()
    return redirect('ebook_loan_list')
