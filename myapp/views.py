import os
from .models import AnimalRecord
import numpy as np
from PIL import Image

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.conf import settings
#model
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array

from django.db.models import Avg
from .models import AnimalRecord

#-------------------------------------
# Load model once
# project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load model once
model_path = os.path.join(settings.BASE_DIR, "model", "best_model.h5")
model = load_model(model_path)

# Classes
classes = ['Buffalo', 'Cow']

#-------------------------------------
#about/help

def about(request):
    return render(request, 'about.html')

@login_required
def profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        profile_pic = request.FILES.get('profile_pic')

        user.first_name = name
        user.username = username
        user.email = email
        user.save()

        if profile_pic:
            profile.profile_pic = profile_pic
            profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    # -------- Statistics --------
    total_uploads = AnimalRecord.objects.filter(user=user).count()

    cow_predictions = AnimalRecord.objects.filter(
        user=user, prediction__iexact="cow"
    ).count()

    buffalo_predictions = AnimalRecord.objects.filter(
    user=user, prediction__iexact="buffalo"
).count()

    avg_confidence = AnimalRecord.objects.filter(user=user).aggregate(
        Avg('confidence')
    )['confidence__avg']

    # Recent predictions
    recent_predictions = AnimalRecord.objects.filter(
        user=user
    ).order_by('-created_at')[:5]

    context = {
        "profile": profile,
        "total_uploads": total_uploads,
        "cow_predictions": cow_predictions,
        "buffalo_predictions": buffalo_predictions,
        "avg_confidence": avg_confidence,
        "recent_predictions": recent_predictions,
    }

    return render(request, "profile.html", context)
#------------------------------------
#AppSettings
@login_required
def appsettings_view(request):
    profile = request.user.userprofile
    if request.method == 'POST':
        theme = request.POST.get('theme')
        notifications = request.POST.get('notifications') == 'on'
        language = request.POST.get('language')

        profile.theme = theme
        profile.notifications = notifications
        profile.language = language
        profile.save()

        messages.success(request,"Settings updated successfully")

        return redirect('appsettings')  # redirect after POST

    context = {'profile': profile}
    return render(request, 'appsettings.html', context)

#-------------------------------------
#signup
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')   # Redirect to home page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
#-------------------------------------
#login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.GET.get('next') or 'index'
            return redirect(next_url)   # Redirect to next page or home
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#-------------------------------------
# Home page
def index(request):
    return render(request, 'index.html')
#-------------------------------------
#logout 
def logout_view(request):
    auth_logout(request)
    return redirect('login')

#-------------------------------------
# Classification page
@login_required
def new_classification(request):
    return render(request, "newclassification.html")


# -------------------------------------
# Prediction
@login_required
def predict(request):

    if request.method == "POST" and request.FILES.get("image"):

        img = Image.open(request.FILES["image"]).convert("RGB")

        img = img.resize((224, 224))

        img_array = img_to_array(img)
        img_array = img_array / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)

        prob = prediction[0][0]

        if prob > 0.5:
            result = "Cow"
            confidence = prob
        else:
            result = "Buffalo"
            confidence = 1 - prob

        # Save record to DB
        record = AnimalRecord.objects.create(
            user=request.user,
            image=request.FILES["image"],
            prediction=result,
            confidence=round(confidence * 100, 2)
        )

        context = {
            "result": result,
            "confidence": round(confidence * 100, 2)
        }

        return render(request, "newclassification.html", context)

    return redirect("new_classification")


#------------------------------------
#records of animals
@login_required
def records(request):
    user_records = AnimalRecord.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'records.html', {'records': user_records})