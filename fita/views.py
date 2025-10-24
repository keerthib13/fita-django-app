from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant

# ---------- HOME PAGE ----------
def home(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'home.html', {'restaurants': restaurants})

# ---------- REGISTER RESTAURANT ----------
def register(request):
    message = None
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            rating = float(request.POST.get('rating'))
            city = request.POST.get('city')
            category = request.POST.get('category')

            Restaurant.objects.create(
                name=name, 
                rating=rating, 
                city=city, 
                category=category
            )
            message = f"{name} added successfully!"
        except Exception as e:
            message = f"Error: {str(e)}"
            print(f"Registration Error: {e}")  # Debug in console

    return render(request, 'register.html', {'message': message})

# ---------- SENTIMENT PREDICTION PAGE ----------
def predict_page(request):
    return render(request, 'index.html')

# ---------- SENTIMENT PREDICTION API ----------
def predict(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')

        if any(word in text.lower() for word in ['good', 'excellent', 'great', 'awesome', 'amazing']):
            sentiment = 'Positive 😊'
        elif any(word in text.lower() for word in ['bad', 'poor', 'terrible', 'worst', 'awful']):
            sentiment = 'Negative 😞'
        else:
            sentiment = 'Neutral 😐' 

        return JsonResponse({'sentiment': sentiment})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


