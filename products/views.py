from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Product, Category
from .constants import BASE_SIZE_LABEL

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.db.models import Q

from .models import ProductReview
from .forms import ProductReviewForm


def ping(request):
    return HttpResponse("Products route OK")


def products_list(request):
    products = (
        Product.objects
        .select_related("category")
        .order_by("name")
    )
    teaser_products = Product.objects.order_by("?")[:10]

    categories = Category.objects.order_by("friendly_name", "name")

    category = request.GET.get("category", "").strip()
    q = request.GET.get("q", "").strip()
    focus = request.GET.get("focus", "").strip()

    active_category = None
    if category:
        category_exists = Category.objects.filter(name=category).exists()
        if category_exists:
            active_category = category
            products = products.filter(category__name=category)
        else:
            products = products.none()

    if q:
        products = products.filter(
            Q(name__icontains=q)
            | Q(description__icontains=q)
            | Q(category__name__icontains=q)
            | Q(category__friendly_name__icontains=q)
        )

    has_filters = bool(category) or bool(q)
    no_results = has_filters and not products.exists()

    show_search = bool(q) or (focus == "1")

    context = {
        "products": products,
        "teaser_products": teaser_products,
        "categories": categories,
        "active_category": active_category,
        "no_results": no_results,
        "show_search": show_search,
        "search_query": q,
        "autofocus_search": (focus == "1"),
    }
    return render(request, "products/list.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = (
        product.reviews
        .select_related("user")
        .all()
    )
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(
            user=request.user
        ).first()

    teaser_products = (
        Product.objects
        .exclude(pk=product.pk)
        .order_by("?")[:10]
    )

    context = {
        "product": product,
        "base_size": BASE_SIZE_LABEL,
        "teaser_products": teaser_products,
        "reviews": reviews,
        "user_review": user_review,
    }
    return render(request, "products/detail.html", context)


# Reviews CRUD (DB + Frontend)
@login_required
def review_create(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    existing = (
        ProductReview.objects
        .filter(product=product, user=request.user)
        .first()
    )
    if existing:
        messages.info(
            request,
            "You already reviewed this product. You can edit your review."
        )
        return redirect(
            "products:review_edit",
            review_id=existing.id
        )

    if request.method == "POST":
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(
                request,
                "Review added successfully."
            )
            return redirect(
                "products:detail",
                pk=product.id
            )
    else:
        form = ProductReviewForm()

    context = {
        "product": product,
        "form": form,
        "mode": "create",
    }
    return render(
        request,
        "products/reviews/review_form.html",
        context
    )


@login_required
def review_edit(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    if review.user != request.user:
        messages.error(
            request,
            "You don't have permission to edit this review."
        )
        return redirect(
            "products:detail",
            pk=review.product.id
        )

    if request.method == "POST":
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Review updated successfully."
            )
            return redirect(
                "products:detail",
                pk=review.product.id
            )
    else:
        form = ProductReviewForm(instance=review)

    context = {
        "product": review.product,
        "form": form,
        "mode": "edit",
    }
    return render(
        request,
        "products/reviews/review_form.html",
        context
    )


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(ProductReview, pk=review_id)

    if review.user != request.user:
        messages.error(
            request,
            "You don't have permission to delete this review."
        )
        return redirect(
            "products:detail",
            pk=review.product.id
        )

    if request.method != "POST":
        messages.info(
            request,
            "Confirm deletion from the product page."
        )
        return redirect(
            "products:detail",
            pk=review.product.id
        )

    product_id = review.product.id
    review.delete()
    messages.success(
        request,
        "Review deleted successfully."
    )
    return redirect(
        "products:detail",
        pk=product_id
    )
