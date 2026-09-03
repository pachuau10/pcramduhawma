from django.shortcuts import render, redirect
from django.contrib import messages
from django_ratelimit.decorators import ratelimit
from .models import GuestbookEntry
from .forms import GuestbookForm


@ratelimit(key='ip', rate='5/h', block=False)
def guestbook_list(request):
    entries = GuestbookEntry.objects.filter(is_approved=True)
    form = GuestbookForm()

    if request.method == 'POST':
        if getattr(request, 'limited', False):
            messages.error(request, 'Slow down! You can only sign the guestbook 5 times per hour.')
            return redirect('guestbook:guestbook_list')
        form = GuestbookForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.ip_address = request.META.get('REMOTE_ADDR')
            entry.save()
            messages.success(request, 'Your message has been submitted and will appear after moderation.')
            return redirect('guestbook:guestbook_list')
        else:
            messages.error(request, 'Please correct the errors below.')

    context = {
        'entries': entries,
        'form': form,
        'page_title': 'Guestbook',
    }
    return render(request, 'guestbook/guestbook_list.html', context)
