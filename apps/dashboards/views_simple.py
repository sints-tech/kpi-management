"""
Simple test view untuk debug - tidak menggunakan database
"""
from django.http import HttpResponse
from django.views import View


class SimpleTestView(View):
    """Simple test view untuk memastikan routing berfungsi"""
    
    def get(self, request):
        return HttpResponse("OK - Routing works! Django is running correctly.")


class DashboardSimpleView(View):
    """Simple dashboard view tanpa database query"""
    
    def get(self, request):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Dashboard - IBGADGETSTORE</title>
        </head>
        <body>
            <h1>Dashboard KPI</h1>
            <p>Dashboard is loading...</p>
            <p>If you see this, routing is working but dashboard view may need database migrations.</p>
        </body>
        </html>
        """
        return HttpResponse(html)

