from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Meep


def home(request):
    if request.user.is_authenticated:
        meeps = Meep.objects.all().order_by("-created_at")
    return render(request, 'home.html', {"meeps":meeps})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles":profiles})
    else:
        messages.success(request, ("You need to log in."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meep.objects.filter(user_id=pk).order_by("-created_at")
        if request.method == "POST":
            current_user_profile = request.user.profile
            action = request.POST['follow']
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            current_user_profile.save()

        return render(request, "profile.html", {"profile":profile, "meeps":meeps})
    else:
        messages.success(request, ("You need to log in."))
        return redirect('home')