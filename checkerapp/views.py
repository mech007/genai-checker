from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MakerEntryForm
from .models import MakerFormEntry
from .llm_service import validate_form_with_llm  # <-- AI logic

@login_required
def maker_form_view(request):
    if request.method == 'POST':
        form = MakerEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.maker = request.user
            entry.save()

            decision = validate_form_with_llm(entry)
            entry.ai_decision = decision
            entry.save()

            return render(request, 'checkerapp/maker_success.html', {'entry': entry, 'ai_result': decision})
    else:
        form = MakerEntryForm()
    return render(request, 'checkerapp/maker_form.html', {'form': form})

# ✅ New view to show AI-powered checker review
@login_required
def checker_view(request):
    entries = MakerFormEntry.objects.all()
    for entry in entries:
        result = validate_form_with_llm(str(entry))  # You can customize prompt logic
        entry.ai_decision = result
        entry.save()
    return render(request, 'checkerapp/checker.html', {'entries': entries})
