from django.shortcuts import render

# Create your views here.
def key_auth_page(request):
    return render(request, 'user_auth/key_auth_page.html')