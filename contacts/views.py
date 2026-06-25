from django.shortcuts import render


def contacts(request):
    return render(request, 'contacts/contact.html')
