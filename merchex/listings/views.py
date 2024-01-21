from django.http import HttpResponse
from listings.models import Band
from listings.models import Listing
from listings.forms import ContactUsForm, BandForm, ListingForm
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import redirect

# Create your views here.
def band_list(request):
    bands = Band.objects.all()
    return render(request,
                  'listings/band_list.html',
                  {'bands': bands})

def band_detail(request, id):
    try:
        band = Band.objects.get(id=id)
        return render(request,
            'listings/band_detail.html',
            {'band': band})
    except ObjectDoesNotExist:
        return HttpResponse('''
        <h1>Could not find this band</h1>
        ''')

def band_create(request):
    if request.method == 'POST':
        form = BandForm(request.POST)
        if form.is_valid():
            band = form.save()
            return redirect('band-detail', band.id)
    else:
        form = BandForm()
    
    return render(request,
                  'listings/band_create.html',
                  {'form': form})

def band_update(request, id):
    band = Band.objects.get(id=id)
    if request.method == 'POST':
        form = BandForm(request.POST, instance=band)
        if form.is_valid():
            form.save()
            return redirect('band-detail', band.id)
    else:
        form = BandForm(instance=band)

    return render(request,
                  'listings/band_update.html',
                  {'form': form})

def band_delete(request, id):
    band = Band.objects.get(id=id)

    if request.method == 'POST':
        band.delete()
        return redirect('band-list')

    return render(request,
                  'listings/band_delete.html',
                  {'band': band})

def about(request):
    return render(request, 'listings/about.html')

def listings_list(request):
    l = Listing.objects.all()
    return render(request,
                  'listings/listings_list.html',
                  {'listings': l})

def listings_detail(request, id):
    try:
        listing = Listing.objects.get(id=id)
        return render(request,
                  'listings/listings_detail.html',
                  {'listings': listing})
    except ObjectDoesNotExist:
        return HttpResponse('''
        <h1>Could not find this listing</h1>
        ''')

def listings_create(request):
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save()
            return redirect('listings-detail', listing.id)
    else:
        form = ListingForm()
    
    return render(request,
                  'listings/listings_create.html',
                  {'form': form})

def listings_update(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        form = ListingForm(request.POST, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('listings-detail', listing.id)
    else:
        form = ListingForm(instance=listing)
        
    return render(request,
                  'listings/listings_update.html',
                  {'form': form})

def listings_delete(request, id):
    listing = Listing.objects.get(id=id)

    if request.method == 'POST':
        listing.delete()
        return redirect('listings-list')

    return render(request,
                  'listings/listings_delete.html',
                  {'listings': listing})

def contact(request):
    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonymous"} via MerchEx Contact Us form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@merchex.xyz']
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request,
                  'listings/contact.html',
                  {'form': form})

def email_sent(request):
    return render(request, 'listings/email_sent.html')