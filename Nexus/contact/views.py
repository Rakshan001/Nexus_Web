from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import ContactFormForm

def submit_form(request):
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('form_success')  # Redirect to a success page after submission
    else:
        form = ContactFormForm()
    return render(request, 'contact/contact_form.html', {'form': form})



from django.shortcuts import render

def form_success(request):
    return render(request, 'contact/form_success.html')
