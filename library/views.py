from django.shortcuts import render, redirect, get_object_or_404
from .forms import LibraryUserRegistrationForm
from django.db.models import Q
from .models import EBook, EBookLoan, Category, EBookHistory, EBookDownload, Note, Department
from django.utils import timezone
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from cart.forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

# Home page
def home(request):
    return render(request, 'library/home.html')

#Index page for the library
def index(request):
    return render(request, 'library/index.html')

# The registration form for the library users
@login_required
def register(request):
    if request.method == 'POST':
        form = LibraryUserRegistrationForm(request.POST, initial={'user': request.user})
        if form.is_valid():
            library_user = form.save(user=request.user)
            return redirect('library:home')  
    else:
        form = LibraryUserRegistrationForm(initial={'user': request.user})

    return render(request, 'library/register.html', {'form': form})


# Detail view for a specific category
def category_list(request, template_name='library/category_list.html'):
    category_slug = request.GET.get('category', None)

    if category_slug == 'all':
        books = EBook.objects.all()
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = EBook.objects.filter(category=category)
    else:
        books = EBook.objects.all()

    categories = Category.objects.all()

    return render(request, template_name, {
        'categories': categories,
        'books': books,
    })


# Detail view for a specific eBook
@login_required
def ebook_detail(request, slug):
    ebook = get_object_or_404(EBook, slug=slug)
    category = ebook.category
    ebook_tags = ebook.tags.all()
    cart_product_form = CartAddProductForm()
    
    
    recommended_books = EBook.objects.filter(tags__in=ebook_tags).exclude(id=ebook.id).distinct()
    downloads = EBookDownload.objects.filter(user=request.user.libraryuser)
    context = {
        'ebook': ebook,'category':category,
        'recommended_books': recommended_books, 
        'downloads': downloads, 
        'cart_product_form':cart_product_form
    }
    return render(request, 'library/ebook_detail.html', context)
   

# List all reading history for the logged-in user
def ebook_download(request, ebook_id):
    # Get the eBook object by its ID
    ebook = get_object_or_404(EBook, id=ebook_id)
    
    # Assuming you already have the user from the request (authenticated user)
    user = request.user.libraryuser  
    
    # Record the download action in EBookHistory
    EBookHistory.objects.create(
        action='Downloaded',
        ebook=ebook,
        user=user
    )

    if not ebook.e_book_file:
        return HttpResponse("File not found.", status=404)

    # Return the actual eBook file for download
    response = HttpResponse(ebook.e_book_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{ebook.title}.pdf"'
    return response


@staff_member_required
def ebook_history_list(request):
    history = EBookHistory.objects.filter(user=request.user.libraryuser, action='Downloaded').order_by('-date_added')
    return render(request, 'library/ebook_history_list.html', {'history': history})




def search_books(request):
    query = request.GET.get('q', '')
    
    if query:
        books = EBook.objects.filter(
            Q(title__icontains=query) | 
            Q(author__name__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()
    else:
        books = EBook.objects.none()  


    # Pagination
    paginator = Paginator(books, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'library/search_books.html', {
        'books': books,
        'page_obj': page_obj,
        'query': query  
    })


# students notes lists uploaded by lecturers
def notes_list(request):
    department_slug = request.GET.get('department', None)

    if department_slug == 'all':
        notes = Note.objects.filter(approved=True)
    elif department_slug:
        department = get_object_or_404(Department, slug=department_slug)
        notes = Note.objects.filter(department = department)
    else:    
        notes = Note.objects.all()

    departments = Department.objects.all()

    return render(request, 'library/notes_list.html', {
        'departments': departments,
        'notes': notes,
    })

# Notes detail for each note uploaded per course
def notes_detail(request, id, slug):
    note = get_object_or_404(Note, id=id, slug=slug)
    return render (request, 'library/notes_detail.html', {'note', note})

    


























def borrow_book(request, ebook_id):
    ebook = get_object_or_404(EBook, id=ebook_id)
    
    if request.user.is_authenticated:
        due_date = timezone.now().date() + timezone.timedelta(days=7)  # Loan for 7 days
        loan = EBookLoan.objects.create(user=request.user.libraryuser, ebook=ebook, due_date=due_date)
        return redirect('loan_details', loan_id=loan.id)
    else:
        return redirect('login')

# List all loans for the logged-in user
def ebook_loan_list(request):
    loans = EBookLoan.objects.filter(user=request.user)
    return render(request, 'loans/loan_list.html', {'loans': loans})

# Mark ebook as returned and calculate late fees
def return_ebook(request, loan_id):
    loan = get_object_or_404(EBookLoan, id=loan_id)
    
    # Ensure the book is not already returned
    if loan.returned:
        return HttpResponse("This book has already been returned.", status=400)

    loan.returned = True
    loan.return_date = timezone.now().date()
    loan.calculate_late_fee()
    loan.save()
    
    return redirect('ebook_loan_list')