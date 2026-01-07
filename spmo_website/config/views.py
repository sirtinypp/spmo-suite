from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import NewsPost  # Ensure models.py is in the same directory

# ---------------------------------------------------------
# PUBLIC VIEW (The Main Government Portal)
# ---------------------------------------------------------
def home(request):
    """
    Renders the public facing 'index.html' with dynamic News data.
    """
    # Fetch the 3 latest published news items, newest first
    # This prevents the page from breaking if the database is empty
    try:
        news_list = NewsPost.objects.filter(is_published=True).order_by('-date_posted')[:3]
    except:
        news_list = []

    context = {
        'title': 'UP SPMO | Official Public Portal',
        'news_list': news_list,
    }
    return render(request, 'index.html', context)


# ---------------------------------------------------------
# PRIVATE VIEW (The Internal Dashboard/Launchpad)
# ---------------------------------------------------------
@login_required(login_url='login')
def admin_portal(request):
    """
    The secure dashboard for SPMO Staff.
    Only accessible after logging in.
    """
    apps = [
        {
            'name': 'GAMIT System',
            'description': 'Property & Asset Management',
            'url': 'http://10.10.2.197:8001/', 
            'admin_url': 'http://10.10.2.197:8001/admin/',
            'icon': 'bi-building-gear',
            'color': 'text-amber-600',
            'bg': 'bg-amber-50',
            'port': '8001'
        },
        {
            'name': 'Virtual Store',
            'description': 'Office Supplies & Inventory',
            'url': 'http://10.10.2.197:8003/', 
            'admin_url': 'http://10.10.2.197:8003/admin/',
            'icon': 'bi-cart4',
            'color': 'text-emerald-600',
            'bg': 'bg-emerald-50',
            'port': '8003'
        },
        {
            'name': 'GFA Portal',
            'description': 'Flight Bookings (PAL/Cebu Pac)',
            'url': 'http://10.10.2.197:8002/',
            'admin_url': 'http://10.10.2.197:8002/admin/',
            'icon': 'bi-airplane-engines',
            'color': 'text-blue-600',
            'bg': 'bg-blue-50',
            'port': '8002'
        },
    ]

    context = {
        'apps': apps,
        'user': request.user,
    }
    
    return render(request, 'portal.html', context)