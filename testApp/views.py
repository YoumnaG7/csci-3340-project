from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "home.html")

@login_required
def schedule(request):
    events = request.user.events.order_by("day", "start_time")
    return render(request, "schedule.html", {"events": events})
    