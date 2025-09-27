from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import HttpResponseRedirect

def index(request):
    return render(request, 'home.html')

def Datasent(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        email_message = EmailMessage(
            'USER DATA SUBMISSION',
            f'Name: {name}\nSubject: {subject}\nEmail: {email}\nMessage: {message}',
            settings.DEFAULT_FROM_EMAIL,
            ['yuvrajsoni9192@gmail.com'],
            headers={'Reply-To': email}
        )


        email_message.send(fail_silently=False)

        return render(request, 'thankyou.html', {'name': name})
    else:
        return HttpResponseRedirect('/')


def certification(request):
    return render(request,'certifications.html')