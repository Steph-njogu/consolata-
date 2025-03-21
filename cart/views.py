from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from library.models import EBook


# Add product to cart
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(EBook, id=product_id)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']

        # Prevents 0 or negative quantities
        if quantity <= 0:
            cart.remove(product)
            messages.error(request, "Quantity must be at least 1.")
            return redirect ('library:category_list')  
        else:
            cart.add(product=product, quantity=quantity, override_quantity=cd['override'])
            messages.success(request, f"Added {quantity}x {product.title} to your cart!")
    else:
        messages.error(request, "Invalid input. Please try again!")

    return redirect('cart:cart_detail')


# Remove product from cart
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    try:
        product = get_object_or_404(EBook, id=product_id)
        cart.remove(product)
        messages.info(request, f"Removed {product.title} from your cart.")
    except:
        messages.error(request, "Error removing product!")

    # Redirect to category list if cart is empty
    if len(cart) == 0:
        messages.info(request, "Your cart is now empty.")
        return redirect('library:category_list')

    return redirect('cart:cart_detail')


# Cart details page
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )

    return render(request, 'cart/cart_detail.html', {'cart': cart})


# Product detail page
def product_detail(request, id, slug):
    product = get_object_or_404(EBook, id=id, slug=slug)
    cart_product_form = CartAddProductForm()

    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }

    return render(request, 'library/ebook_detail_form.html', context)