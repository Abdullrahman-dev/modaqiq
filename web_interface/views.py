from django.shortcuts import render
from legal_engine.models import Case

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def judge_dashboard(request):
    # Fetch all cases, optimized with related party info and validation result
    cases = Case.objects.select_related('plaintiff', 'validation_result').order_by('-submission_date')
    return render(request, 'judge_dashboard.html', {'cases': cases})
