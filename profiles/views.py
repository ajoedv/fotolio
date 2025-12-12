from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import render, redirect

from .forms import ProfileForm
from .models import Profile


@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    context = {
        "profile": profile,
        # "orders": profile.orders.all(),
    }
    return render(request, "profiles/profile.html", context)


@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile,
        )
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profiles:profile")
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile": profile,
    }
    return render(request, "profiles/edit.html", context)


@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(
            request,
            "Your account has been deleted successfully.",
        )
        return redirect("home")

    return render(request, "profiles/delete_confirm.html")
