from django.shortcuts import render, redirect
from .models import Order, OrderItem
from .forms import OrderForm
from cart.cart import Cart


def order_create(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart(request)

        if request.method == 'POST':
            form = OrderForm(request.POST)

            # Validates form before accessing cleaned data
            if form.is_valid():
                order = Order(
                    user=user,
                    address=form.cleaned_data['address'],
                    city=form.cleaned_data['city']
                )
                order.save()

                # Creates OrderItems from cart content
                for item in cart:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

                # Clears cart after order creation
                cart.clear()

                return render(request, 'order/created.html', {'order': order})
            else:
                # If form is invalid, show errors
                return render(request, 'order/create.html', {'form': form, 'cart': cart})

        else:
            # Pre-fills form with user data
            form = OrderForm()
            form.load_from_user(user)

        return render(request, 'order/create.html', {'form': form, 'cart': cart})

    else:
        # Redirect to login if user isn't authenticated
        return redirect('users:login')
