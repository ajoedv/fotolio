from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ProfileForm
from django.contrib.auth import logout

@login_required
def profile_view(request):
    profile = getattr(request.user, "profile", None)  # يجيب بروفايل المستخدم
    return render(request, "profiles/profile.html", {"profile": profile})

@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ بيانات البروفايل بنجاح.")
            return redirect("profiles:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "profiles/edit.html", {"form": form, "profile": profile})

@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete() 
        messages.success(request, "Your account has been deleted successfully.")
        return redirect("home")
    return render(request, "profiles/delete_confirm.html")