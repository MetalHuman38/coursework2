"""
This module contains all view functions for the app.
"""

from django.shortcuts import render


# Create your views here.
def home(request):
    """
    Home page view
    """

    return render(request, "home")
