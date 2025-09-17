from .models import CartItem

def cart_summary(request):
    count = 0
    total = 0
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        items = CartItem.objects.filter(user=user).select_related("product")
        count = sum(i.quantity for i in items)
        total = sum(i.line_total for i in items)
    return {"cart_count": count, "cart_total": total}