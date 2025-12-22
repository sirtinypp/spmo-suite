from django.shortcuts import render

def admin_portal(request):
    # This view doesn't need database queries, it just renders the launchpad
    apps = [
        {
            'name': 'Virtual Store',
            'description': 'Office Supplies & Inventory',
            'url': 'http://localhost:8003/', 
            'admin_url': 'http://localhost:8003/admin/',
            'icon': 'bi-cart4',
            'color': 'text-emerald-600',
            'bg': 'bg-emerald-50',
            'port': '8003'
        },
        {
            'name': 'GFA Portal',
            'description': 'Flight Bookings (PAL/Cebu Pac)',
            'url': 'http://localhost:8002/',
            'admin_url': 'http://localhost:8002/admin/',
            'icon': 'bi-airplane-engines',
            'color': 'text-blue-600',
            'bg': 'bg-blue-50',
            'port': '8002'
        },
        {
            'name': 'GAMIT System',
            'description': 'Property & Asset Management',
            'url': 'http://localhost:8001/',
            'admin_url': 'http://localhost:8001/admin/',
            'icon': 'bi-building-gear',
            'color': 'text-amber-600',
            'bg': 'bg-amber-50',
            'port': '8001'
        },
    ]
    return render(request, 'portal.html', {'apps': apps})